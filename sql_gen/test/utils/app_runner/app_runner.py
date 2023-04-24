import os
import sys
from io import StringIO
from pathlib import Path

import pytest
import yaml

from ccdev.command_line_app import CommandLineSQLTaskApp
from sql_gen.app_project import AppProject
from sql_gen.commands.verify_templates_cmd import FillTemplateAppRunner
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder


class FakeLogger(object):
    def debug(self):
        """"""

    def info(self):
        """"""

    def error(self):
        """"""


class ApplicationRunner(FillTemplateAppRunner):
    def __init__(self):
        super().__init__()
        self._project = None

    def _run(self, args):

        sys.argv = args
        sys.stdin = StringIO(self._user_input_to_str())
        return self.build_app().run()

    def _user_input_to_str(self):
        result = "\n".join([input for input in self.inputs])
        self.inputs.clear()  # so if runs again it doe not repit inputs
        return result

    def build_app(self):
        self.app = CommandLineSQLTaskApp.build_app(
            self._project.emroot, logger=FakeLogger()
        )
        return self.app

    def with_project(self, project):
        self._project = project
        return self

    def assert_all_input_was_read(self):
        with pytest.raises(EOFError) as excinfo:
            test = input()
            print("Unexpected input: " + test)
        assert "EOF" in str(excinfo.value)
        return self


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

    def with_emproject(self, emproject):
        self.emproject_path = emproject.root
        self.emprj_path = emproject.root
        self.emproject = emproject
        self._app_project = AppProject(self.emprj_path)

        os.chdir(emproject.root)
        return self

    def build_app(self):
        self.app = CommandLineSQLTaskApp.build_app(
            os.getcwd(), self.env_vars, FakeLogger()
        )
        return self.app

    def _dict_to_str(self, config):
        return "\n".join("{!s}={!s}".format(key, val) for (key, val) in config.items())

    def _create_file(self, path, content):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, "w") as f:
            f.write(content)

    def with_task_library(self, library_path):
        builder = FakeEMProjectBuilder(self.fs, root=self.emprj_path)
        builder.append_to_app_config(f"\nsqltask.library.path={library_path}")
        templates_path = str(Path(library_path) / "templates")
        self.templates_path = templates_path

        self.fs.create_dir(self.templates_path)
        return self

    def _run(self, args, app=None):
        sys.argv = args
        sys.stdin = StringIO(self._user_input_to_str())
        app.run()

    def _user_input_to_str(self):
        result = "\n".join([input for input in self.inputs])
        self.inputs.clear()  # so if runs again it doe not repit inputs
        return result

    def assert_all_input_was_read(self):
        with pytest.raises(EOFError) as excinfo:
            test = input()
            print("Unexpected input: " + test)
        assert "EOF" in str(excinfo.value)
        return self


class InitAppRunner(AppRunner):
    def __init__(self, fs=None):
        super().__init__(fs=fs)

    def run(self, app=None):
        self._run([".", "init"], app=app)
        return self


class TemplatesAppRunner(ApplicationRunner):
    def __init__(self, capsys=None):
        super().__init__()
        self.capsys = capsys

    @property
    def test_template_path(self):
        return str(Path(self.templates_path).parent / "test_templates")

    def make_test_dir(self):
        self.fs.create_dir(self.test_template_path)
        return self

    def with_test_context_values(self, data):
        self.context_values = None
        filepath = self._app_project.library().test_context_values()
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
        self._run([".", "test-sql", "--tests=expected-sql"])
        return self

    def run_test_with_db(self):
        self._run([".", "test-sql", "--tests=run-on-db"])
        return self

    def run_test_all(self):
        self._run([".", "test-sql", "--tests=all"])
        return self

    def run_one_test(self, test_name):
        self._run([".", "test-sql", "--test-name=" + test_name])
        return self

    def run_assertion_test(self, assertion_type):
        self._run([".", "test-sql", "--assertion=" + assertion_type])
        return self

    def run(self, app=None):
        self._run([".", "test-sql"], self.build_app())
        return self

    def test_sql(self):
        self._run([".", "test-sql"])
        return self

    def assert_message_printed(self, expected):
        captured = self.capsys.readouterr()
        assert expected in captured.out
        return self

    def generates_no_test(self):
        assert not os.path.exists(self.app.last_command_run.generated_test_filepath())

    def assert_generated_tests(self, expected_source):
        testfile = open(self.app.last_command_run.generated_test_filepath())
        test_content = testfile.read()
        testfile.close()
        assert expected_source.to_string() == test_content
