import os
import sys
from io import StringIO

import pytest
import pyperclip

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleDisplayer,PrintSQLToConsoleCommand,CreateSQLTaskCommand, TestTemplatesCommand,RunSQLCommand
from sql_gen.commands.verify_templates_cmd import FillTemplateAppRunner
from sql_gen.app_project import AppProject
from sql_gen.emproject.em_project import emproject_home
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.database.sqlparser import SQLParser

class FakeLogger(object):
    def debug(self):
        """"""
    def info(self):
        """"""
    def error(self):
        """"""
class AppRunner(FillTemplateAppRunner):
    def __init__(self,fs=None):
        super().__init__()
        self.fs=fs
        self.env_vars={}
        self.initial_context={}
        self.command=None

    def add_template(self, name, content):
        path = EMTemplatesEnv().get_templates_path(self.env_vars)
        self.fs.create_file(os.path.join(path,name), contents=content)
        return self

    def from_current_dir(self, cwd):
        os.chdir(cwd)
        return self

    def and_prj_built_under(self, path):
        FakeEMProjectBuilder(self.fs,root=path).make_valid_em_folder_layout()
        return self

    def with_emproject_under(self,emproject_path):
        self.env_vars['EM_CORE_HOME']=emproject_path
        return self

    def with_app_config(self, config):
        self._create_file(self._app_path('core_config'),
                          self._dict_to_str(config))
        return self

    def _em_path(self,key):
        return AppProject(env_vars=self.env_vars).emproject.paths[key].path

    def _app_path(self,key):
        return AppProject(env_vars=self.env_vars).paths[key].path

    def _dict_to_str(self,config):
        return '\n'.join("{!s}={!s}".format(key,val) for (key,val) in config.items())

    def _create_file(self,path,content):
        dirname=os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path,"w") as f:
            f.write(content)

    def using_templates_under(self, templates_path):
        self.env_vars['SQL_TEMPLATES_PATH']=templates_path
        return self

    def with_initial_context(self, initial_context):
        self.initial_context=initial_context
        return self

    def _run(self,args,app=None):
        sys.argv=args
        sys.stdin = StringIO(self._user_input_to_str())
        if not app:
            app = CommandLineSQLTaskApp(self._make_command_factory(),
                                        logger=FakeLogger())
        app.run()

    def _user_input_to_str(self):
        return "\n".join([input for input in self.inputs])

    def assert_rendered_sql(self,expected_sql):
        assert expected_sql == self.command.sql_printed()
        return self

    def assert_all_input_was_read(self):
        with pytest.raises(EOFError) as excinfo:
            input("check")
        assert "EOF" in str(excinfo.value)
        return self

class DummyEnvironment(object):
    def list_templates(self):
        return []

class CommandTestFactory(CommandFactory):
    def __init__(self,
            print_to_console_command=None,
            create_sqltask_command=None,
            test_sql_templates_commmand=None,
            run_sql_command=None):
        self.print_to_console_command=print_to_console_command
        self.create_sqltask_command=create_sqltask_command
        self.test_sql_templates_commmand=test_sql_templates_commmand
        self.run_sql_command = run_sql_command

    def make_print_sql_to_console_command(self):
        return self.print_to_console_command

    def make_create_sqltask_command(self,args):
        self.create_sqltask_command.path = args['<directory>']
        return self.create_sqltask_command

    def make_test_sql_templates_command(self,args):
        self.test_sql_templates_commmand.test_group=args['--tests']
        return self.test_sql_templates_commmand

    def make_run_sql_command(self,env_vars):
        return self.run_sql_command



class PrintSQLToConsoleAppRunner(AppRunner):
    def __init__(self,fs=None):
        super().__init__(fs=fs)

    def run(self,app =None):
        self._run(['.','print-sql'],app=app)
        return self

    def run_prod(self):
        self.run(CommandLineSQLTaskApp(CommandFactory(self.env_vars),
                 logger=FakeLogger()))
        return self

    def _make_command_factory(self):
        self.command = PrintSQLToConsoleCommand(
                                env_vars=self.env_vars,
                                initial_context=self.initial_context)
        return CommandTestFactory(
                print_to_console_command=self.command)

class FakeSvnClient(object):
    def __init__(self, rev_no):
        self.rev_no =rev_no

    def revision_number(self):
        if type(self.rev_no).__name__ =="str":
            return self.rev_no
        raise self.rev_no

class FakeClipboard():
    def copy(self, text):
        self.text = text
    def paste(self):
        return self.text

class CreateSQLTaskAppRunner(AppRunner):
    def __init__(self):
        super().__init__()
        self.rev_no="0"
        self.taskpath=""
        self.clipboard =FakeClipboard()

    def _make_command_factory(self):
        self.command = CreateSQLTaskCommand(
                                self.env_vars,
                                self.initial_context,
                                FakeSvnClient(self.rev_no),
                                self.clipboard)
        return CommandTestFactory(
                create_sqltask_command=self.command)

    def with_svn_rev_no(self,rev_no):
        self.rev_no =rev_no
        return self

    def with_sql_modules(self, repo_modules):
        for repo_module in repo_modules:
            full_dir=os.path.join(self._em_path('sql_modules'),repo_module)
            os.makedirs(full_dir)
        return self

    def run_create_sqltask(self,taskpath=None):
        self.taskpath =taskpath
        self._run(['.','create-sql',taskpath])
        return self

    def exists(self,filepath,expected_content):
        with open(filepath) as f:
                s = f.read()
        assert expected_content == s
        return self

    def not_exists(self,filepath):
        assert not os.path.exists(filepath)
        return self

    def assert_path_copied_to_sys_clipboard(self):
        assert self.taskpath == self.clipboard.paste()
        return self

class FakePytest(object):
    def main(params,directory):
        """do nothing"""


class TemplatesAppRunner(AppRunner):
    def __init__(self,fs,capsys=None):
        super().__init__(fs=fs)
        self.capsys = capsys
        self.tests=[]

    def _make_command_factory(self):
        templates_path =EMTemplatesEnv().extract_templates_path(self.env_vars)
        emprj_path= emproject_home(self.env_vars)
        self.command = TestTemplatesCommand(
                                FakePytest(),
                                templates_path=templates_path,
                                emprj_path=emprj_path,
                                initial_context=self.initial_context)
        return CommandTestFactory(
                test_sql_templates_commmand=self.command)

    def make_test_dir(self):
        path =self._app_path("test_templates")
        self.fs.create_dir(path)
        return self

    def add_test(self, name, template_vars, content):
        self.tests.append({"name": name,
                           "template_vars":template_vars,
                           "content": content})
        path =self._app_path("test_templates")
        test_content="-- "+str(template_vars)+'\n'+content
        self.fs.create_file(os.path.join(path,name), contents=test_content)
        return self
    def run_test_render_sql(self):
        self._run(['.','test-sql','--tests=expected-sql'])
        return self

    def run_test_with_db(self):
        self._run(['.','test-sql','--tests=run-on-db'])
        return self

    def run_test_all(self):
        self._run(['.','test-sql','--tests=all'])
        return self

    def run(self):
        self._run(['.','test-sql'])
        return self

    def assert_no_of_gen_tests(self,expected_no_of_tests):
        path =self._app_path("test_templates_tmp")
        number_of_tests =len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        assert expected_no_of_tests == number_of_tests

    def assert_message_printed(self,expected):
        captured = self.capsys.readouterr()
        assert expected == captured.out
        return self

    def generates_no_test(self):
        assert not os.path.exists(self.command.generated_test_filepath())

    def assert_generated_tests(self, expected_source):
        testfile =open(self.command.generated_test_filepath())
        test_content=testfile.read()
        testfile.close()
        assert expected_source.to_string() ==test_content


class FakeDB(object):
    def __init__(self):
        self.executed_sql=""
    def execute(self,sql,commit=None):
        self.executed_sql+=sql

class RunSQLAppRunner(PrintSQLToConsoleAppRunner):
    """"""
    def __init__(self,fs):
        super().__init__(fs=fs)
        self.fakedb = FakeDB()

    def assert_sql_executed(self,sql):
        assert sql == self.fakedb.executed_sql
        return self
    def confirmRun(self):
        self.user_inputs("y")
        return self

    def run(self,app =None):
        self.initial_context["_database"]=self.fakedb
        self._run(['.','run-sql'],app=app)
        return self

    def _make_command_factory(self):
        self.command = RunSQLCommand(
                                env_vars=self.env_vars,
                                initial_context=self.initial_context)
        return CommandTestFactory(
                run_sql_command=self.command)
