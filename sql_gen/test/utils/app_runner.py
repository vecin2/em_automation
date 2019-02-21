import sys
from io import StringIO

import pytest

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleDisplayer,PrintSQLToConsoleCommandFactory
class PrintSQLToConsoleTestFactory(PrintSQLToConsoleCommandFactory):
    def __init__(self, sql_renderer,initial_context={}):
        self.sql_renderer = sql_renderer
        self.initial_context = initial_context

    def _make_doc_writer(self):
        return self.sql_renderer

    def _make_initial_context(self):
        return self.initial_context

class DummyEnvironment(object):
    def list_templates(self):
        return []

class AppRunner():
    def __init__(self,sql_renderer):
        self.inputs=[]
        self.original_stdin = sys.stdin
        self.environment =DummyEnvironment()
        self.env_vars={'EM_CORE_HOME':'/em/projects/pc'}
        self.sql_renderer = sql_renderer
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

    def using_templates_under(self, templates_path):
        self.env_vars={'SQL_TEMPLATES_PATH':templates_path}
        return self

    def em_prj_under(self, prj_home):
        self.env_vars={'EM_CORE_HOME':prj_home}
        return self

    def with_initial_context(self, initial_context):
        self.initial_context=initial_context
        return self

    def _run(self,args):
        sys.argv=args
        sys.stdin = StringIO(self._user_input_to_str())
        app = CommandLineSQLTaskApp(self._make_command_factory())
        app.run(self.env_vars)

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

class PrintSQLToConsoleAppRunner(AppRunner):
    def __init__(self):
        super().__init__(PrintSQLToConsoleDisplayer())

    def run(self):
        self._run(['.'])
        return self

    def _make_command_factory(self):
        printsql_factory = PrintSQLToConsoleTestFactory(
                                        self.sql_renderer,
                                        self.initial_context)
        return CommandFactory(printsql_factory)

class CreateSQLTaskTestFactory(object):
    def make(self):
        return CreateSQLTaskCommand(self.sql_renderer,
                                            self.initial_context)

class CreateSQLTaskAppRunner(AppRunner):

    def _make_specific_command_factory(self):
        return CreateSQLTaskTestFactory()

    def with_svn_rev_no(self,rev_no):
        self.rev_no=rev_no
        return self

    def run_create_sqltask(self,sqltask_location):
        self._run(['.','-d',sqltask_location])
        return self

    def _make_command_factory(self):
        printsql_factory = PrintSQLToConsoleTestFactory(
                                        self.sql_renderer,
                                        self.initial_context)
        return CommandFactory(printsql_factory)

    def assert_sqltask(files,prj_location):
        """"""

