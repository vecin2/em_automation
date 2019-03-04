import os
import sys
from io import StringIO

import pytest
import pyperclip

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleDisplayer,PrintSQLToConsoleCommand,CreateSQLTaskCommand
from sql_gen.app_project import AppProject

class AppRunner():
    def __init__(self):
        self.original_stdin = sys.stdin
        self.inputs=[]
        self.env_vars={}
        self.initial_context={}

    def saveAndExit(self):
        self.user_inputs("x")
        return self

    def select_template(self, template_option,values):
        self.user_inputs(template_option)
        for value in values.values():
            self.user_inputs(value)
        return self

    def user_inputs(self, user_input):
        self.inputs.append(user_input)
        return self

    def with_emproject_under(self,emproject_path):
        self.env_vars['EM_CORE_HOME']=emproject_path
        return self

    def with_app_config(self, config):
        self._create_file(self._app_path('core_config'),
                          self._dict_to_str(config))
        return self

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
            app = CommandLineSQLTaskApp(self._make_command_factory())
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

    def teardown(self):
        sys.stdin = self.original_stdin

class DummyEnvironment(object):
    def list_templates(self):
        return []

class CommandTestFactory(CommandFactory):
    def __init__(self,
            print_to_console_command=None,
            create_sqltask_command=None):
        self.print_to_console_command=print_to_console_command
        self.create_sqltask_command=create_sqltask_command

    def make_print_sql_to_console_command(self):
        return self.print_to_console_command

    def make_create_sqltask_command(self,path):
        self.create_sqltask_command.path =path
        return self.create_sqltask_command

class PrintSQLToConsoleAppRunner(AppRunner):
    def __init__(self):
        super().__init__()

    def run(self,app =None):
        self._run(['.'],app=app)
        return self

    def run_prod(self):
        self.run(CommandLineSQLTaskApp(CommandFactory(self.env_vars)))
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

    def current_rev_no(self):
        return self.rev_no

class FakeClipboard():
    def copy(self, text):
        self.text = text
    def paste(self):
        return self.text

class CreateSQLTaskAppRunner(AppRunner):
    def __init__(self):
        super().__init__()
        self.command =None
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

    def run_create_sqltask(self,taskpath):
        self.taskpath =taskpath
        self._run(['.','-d',taskpath])
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

