import os
import re
import sys
from io import StringIO
from pathlib import Path

import pytest
import yaml

from ccdev import ProjectHome
from ccdev.command_factory import CommandFactory
from ccdev.command_line_app import CommandLineSQLTaskApp
from sql_gen.app_project import AppProject
from sql_gen.commands.run_sql_cmd import RunSQLDisplayer
from sql_gen.commands.verify_templates_cmd import FillTemplateAppRunner
from sql_gen.emproject import EMSvn
from sql_gen.sqltask_jinja.context import ContextBuilder
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder


class FakeLogger(object):
    def debug(self):
        """"""

    def info(self):
        """"""

    def error(self):
        """"""


class AppRunner(FillTemplateAppRunner):
    def __init__(self, fs=None):
        super().__init__()
        self.fs = fs
        self.env_vars = {}
        self.templates_path = None
        self.template_API = {}
        self.context_values = {}
        self.command = None
        self._app_project = None
        self.emproject_path = None
        self.emproject = None
        self.app = None

    def add_template(self, filepath, content):
        dirname = os.path.dirname(filepath)
        name = os.path.basename(filepath)
        path = self.templates_path
        full_dir = os.path.join(path, dirname)
        self._create_file(os.path.join(full_dir, name), content)
        return self

    def from_current_dir(self, cwd):
        os.chdir(cwd)
        return self

    def and_prj_built_under(self, path):
        FakeEMProjectBuilder(self.fs, root=path).make_valid_em_folder_layout()
        return self

    def with_emproject(self, emproject):
        self.emproject_path = emproject.root
        self.emprj_path = emproject.root
        self.emproject = emproject
        os.chdir(emproject.root)
        return self

    def build_app(self):
        self.app = CommandLineSQLTaskApp(
            project_home=ProjectHome(os.getcwd(), self.env_vars),
            args_factory=CommandFactory(ProjectHome(os.getcwd(), self.env_vars)),
            logger=FakeLogger(),
        )
        return self.app

    def with_emproject_under(self, emproject_path):
        self.env_vars["EM_CORE_HOME"] = emproject_path
        self.emproject_path = emproject_path
        return self

    def with_app_config(self, config):
        self._create_file(self._app_path("core_config"), self._dict_to_str(config))
        return self

    def appconfig(self):
        return self.app_project().config

    def _em_path(self, key):
        return self.app_project().emproject.paths[key].path

    def _app_path(self, key):
        return self.app_project().paths[key].path

    def app_project(self):
        if not self._app_project:
            self._app_project = AppProject(emprj_path=self.emproject_path)
        return self._app_project

    def _dict_to_str(self, config):
        return "\n".join("{!s}={!s}".format(key, val) for (key, val) in config.items())

    def _create_file(self, path, content):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, "w") as f:
            f.write(content)

    def using_templates_under(self, templates_path):
        self.env_vars["SQL_TEMPLATES_PATH"] = templates_path
        self.templates_path = templates_path
        self.fs.create_dir(templates_path)
        return self

    def with_template_API(self, template_API):
        self.template_API.update(template_API)
        return self

    @property
    def context_builder(self):
        context_builder = ContextBuilder()
        context_builder.template_API = self.template_API
        context_builder.context_values = self.context_values
        return context_builder

    def _run(self, args, app=None):
        sys.argv = args
        sys.stdin = StringIO(self._user_input_to_str())

        if not app:
            app = CommandLineSQLTaskApp(
                args_factory=self._make_command_factory(), logger=FakeLogger()
            )
        app.run()

    def _user_input_to_str(self):
        result = "\n".join([input for input in self.inputs])
        self.inputs.clear()  # so if runs again it doe not repit inputs
        return result

    def assert_rendered_sql(self, expected_sql):
        assert expected_sql == self.command.sql_printed()
        return self

    def assert_printed_sql(self, expected_sql):
        assert expected_sql == self.app.last_command_run.sql_printed()
        return self

    def assert_all_input_was_read(self):
        with pytest.raises(EOFError) as excinfo:
            test = input()
            print("Unexpected input: " + test)
        assert "EOF" in str(excinfo.value)
        return self


class CommandTestFactory(CommandFactory):
    def __init__(
        self,
        print_to_console_command=None,
        create_sqltask_command=None,
        test_sql_templates_commmand=None,
        run_sql_command=None,
    ):
        self.print_to_console_command = print_to_console_command
        self.create_sqltask_command = create_sqltask_command
        self.test_sql_templates_commmand = test_sql_templates_commmand
        self.run_sql_command = run_sql_command

    def make_print_sql_to_console_command(self):
        return self.print_to_console_command

    def make_create_sqltask_command(self, args):
        self.create_sqltask_command.path = args["<directory>"]
        self.create_sqltask_command.template_name = args["--template"]
        return self.create_sqltask_command

    def make_test_sql_templates_command(self, args):
        self.test_sql_templates_commmand.test_group = args["--tests"]
        self.test_sql_templates_commmand.test_name = args["--test-name"]
        return self.test_sql_templates_commmand

    def make_run_sql_command(self, env_vars):
        return self.run_sql_command


class InitAppRunner(AppRunner):
    def __init__(self, fs=None):
        super().__init__(fs=fs)

    def run(self, app=None):
        self._run([".", "init"], app=app)
        return self

    def _make_command_factory(self):
        return CommandFactory(self.env_vars)
        # self.command = PrintSQLToConsoleCommand(
        #     env_vars=self.env_vars,
        #     context_builder=self.context_builder,
        #     run_on_db=False,
        # )
        # return CommandTestFactory(print_to_console_command=self.command)


class PrintSQLToConsoleAppRunner(AppRunner):
    def __init__(self, fs=None):
        super().__init__(fs=fs)

    def print_sql(self, app=None):
        self._run([".", "print-sql"], self.build_app())
        return self


class FakeSvnClient(EMSvn):
    def __init__(self, rev_no):
        self.rev_no = rev_no

    def revision_number(self):
        if type(self.rev_no).__name__ == "str":
            return self.rev_no
        raise self.rev_no


class FakeClipboard:
    def copy(self, text):
        self.text = text

    def paste(self):
        return self.text


class CreateSQLTaskAppRunner(AppRunner):
    def __init__(self, fs=None):
        super().__init__(fs=fs)
        self.rev_no = "0"
        self.taskpath = ""
        self.clipboard = FakeClipboard()

    def create_sql(self, sqltask_path=None, template=None):
        self.taskpath = sqltask_path
        params = [".", "create-sql"]

        if sqltask_path:
            params.append(sqltask_path)
        if template:
            params.extend(["--template", template])
        self._run(params, self.build_app())
        return self

    def exists(self, filepath, expected_content):
        with open(filepath) as f:
            s = f.read()
        assert expected_content == s
        return self

    def exists_regex(self, filepath, expected_content):
        with open(filepath) as f:
            text = f.read()
        match = re.search(expected_content, text)
        assert match.group()
        return self

    def assert_path_copied_to_sys_clipboard(self):
        assert self.taskpath == self.clipboard.paste()
        return self


class TemplatesAppRunner(AppRunner):
    def __init__(self, fs, capsys=None):
        super().__init__(fs=fs)
        self.capsys = capsys

    @property
    def test_template_path(self):
        return str(Path(self.templates_path).parent / "test_templates")

    def make_test_dir(self):
        self.fs.create_dir(self.test_template_path)
        return self

    def with_test_context_values(self, data):
        self.context_values = None
        filepath = self._app_path("test_context_values")
        self._create_file(filepath, yaml.dump(data))
        return self

    def add_test(self, template_path, template_vars, content, template_vars_list=None):
        dirname = os.path.dirname(template_path)
        name = os.path.basename(template_path)
        path = os.path.join(self.test_template_path, dirname)
        test_data_object = self._get_template_vars(template_vars, template_vars_list)
        test_content = "-- " + str(test_data_object) + "\n" + content
        self._create_file(os.path.join(path, name), test_content)
        return self

    def _get_template_vars(self, template_vars, template_vars_list):
        if template_vars is not None:
            return template_vars
        else:
            return template_vars_list

    def run_test_render_sql(self):
        self._run([".", "test-sql", "--tests=expected-sql"], self.build_app())
        return self

    def run_test_with_db(self):
        self._run([".", "test-sql", "--tests=run-on-db"], self.build_app())
        return self

    def run_test_all(self):
        self._run([".", "test-sql", "--tests=all"], self.build_app())
        return self

    def run_one_test(self, test_name):
        self._run([".", "test-sql", "--test-name=" + test_name], self.build_app())
        return self

    def run_assertion_test(self, assertion_type):
        self._run([".", "test-sql", "--assertion=" + assertion_type])
        return self

    def run(self, app=None):
        self._run([".", "test-sql"], self.build_app())
        return self

    def test_sql(self):
        self._run([".", "test-sql"], self.build_app())
        return self

    def assert_message_printed(self, expected):
        captured = self.capsys.readouterr()
        assert expected == captured.out
        return self

    def generates_no_test(self):
        assert not os.path.exists(self.app.last_command_run.generated_test_filepath())

    def assert_generated_tests(self, expected_source):
        testfile = open(self.app.last_command_run.generated_test_filepath())
        test_content = testfile.read()
        testfile.close()
        assert expected_source.to_string() == test_content


class FakeRunSQLDisplayer(RunSQLDisplayer):
    def __init__(self):
        self.printed_text = ""

    def display_sqltable(self, sqltable):
        self.printed_text += str(sqltable)

    def printed_text(self):
        return self.printed_text


class RunSQLAppRunner(PrintSQLToConsoleAppRunner):
    """"""

    def __init__(self, fs):
        super().__init__(fs=fs)
        self.displayer = FakeRunSQLDisplayer()

    def assert_prints(self, expected_text):
        assert self.displayer.printed_text == expected_text
        return self

    def confirmRun(self):
        self.user_inputs("y")
        return self

    def run(self, app=None):
        self._run([".", "run-sql"], app=app)
        return self

    def run_sql(self):

        self.app = CommandLineSQLTaskApp(
            project_home=ProjectHome(os.getcwd(), self.env_vars),
            args_factory=CommandFactory(ProjectHome(os.getcwd(), self.env_vars)),
            logger=FakeLogger(),
        )
        self.run(self.app)
        return self
