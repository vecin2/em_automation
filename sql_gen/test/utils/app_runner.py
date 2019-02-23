import sys
from io import StringIO

import pytest

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleDisplayer,PrintSQLToConsoleCommand,CreateSQLTaskCommand

class AppRunner():
    def __init__(self):
        self.inputs=[]
        self.original_stdin = sys.stdin
        self.environment = DummyEnvironment()
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

    def using_templates_under(self, templates_path):
        self.env_vars['SQL_TEMPLATES_PATH']=templates_path
        return self

    def with_initial_context(self, initial_context):
        self.initial_context=initial_context
        return self

    def _run(self,args):
        sys.argv=args
        sys.stdin = StringIO(self._user_input_to_str())
        app = CommandLineSQLTaskApp(self._make_command_factory())
        app.run()

    def _user_input_to_str(self):
        return "\n".join([input for input in self.inputs])

    def assert_rendered_sql(self,expected_sql):
        assert expected_sql == self.sql_renderer.rendered_sql
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
        self.sql_renderer = PrintSQLToConsoleDisplayer()

    def run(self):
        self._run(['.'])
        return self

    def _make_command_factory(self):
        command = PrintSQLToConsoleCommand(
                                self.env_vars,
                                self.sql_renderer,
                                self.initial_context)
        return CommandTestFactory(
                print_to_console_command=command)

class FakeSvnClient(object):
    def __init__(self, rev_no):
        self.rev_no =rev_no

    def current_rev_no(self):
        return self.rev_no

class CreateSQLTaskAppRunner(AppRunner):
    def __init__(self):
        super().__init__()
        self.command =None

    def _make_command_factory(self):
        self.command = CreateSQLTaskCommand(
                                self.env_vars,
                                self.initial_context,
                                FakeSvnClient(self.rev_no))
        return CommandTestFactory(
                create_sqltask_command=self.command)

    def with_svn_rev_no(self,rev_no):
        self.rev_no =rev_no
        return self

    def run_create_sqltask(self,taskpath):
        self._run(['.','-d',taskpath])
        return self

    def exist(self,filepath,expected_content):
        with open(filepath) as f:
                s = f.read()
        assert expected_content == s
        return self

