import sys
import os

from io import StringIO

import pytest

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleCommandBuilder, PrintSQLToConsoleDisplayer,PrintSQLToConsoleProdConfig
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv

class PrintSQLToConsoleTestConfig(PrintSQLToConsoleProdConfig):
    def __init__(self, sql_renderer):
        self.sql_renderer = sql_renderer

    def _make_doc_writer(self):
        return self.sql_renderer

class DummyEnvironment(object):
    def list_templates(self):
        return []

class AppRunner():
    def __init__(self):
        self.inputs=[]
        self.original_stdin = sys.stdin
        self.template_path=""
        self.environment =DummyEnvironment()
        self.env_vars=os.environ

    def saveAndExit(self):
        self.user_inputs("","x")
        return self

    def select_template(self, template_option,values):
        self.user_inputs("",template_option)
        for value in values.values():
            self.user_inputs("",value)
        return self

    def user_inputs(self,description, user_input):
        #description is used only for test readability
        self.inputs.append(user_input)
        self.sql_renderer = PrintSQLToConsoleDisplayer()
        return self

    def using_templates_under(self, templates_path):
        self.env_vars={'SQL_TEMPLATES_PATH':templates_path}
        return self


    def run_print_SQL_to_console(self):
        self._run(['.'])
        return self

    def _run(self,args):
        sys.argv=args
        sys.stdin = StringIO(self._user_input_to_str())

        test_config= PrintSQLToConsoleTestConfig(self.sql_renderer)
        command_factory = CommandFactory(test_config)
        app = CommandLineSQLTaskApp(command_factory)
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

@pytest.fixture
def app_runner():
    app_runner = AppRunner()
    yield app_runner
    app_runner.teardown()


def test_returns_empty_when_no_template_selected(app_runner):
    app_runner.saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("")

def test_asks_for_template_until_valid_entry(app_runner):
    app_runner.select_template('abc',{})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("")\
               .assert_all_input_was_read()

def test_select_and_render_no_vals_template(app_runner,fs):
    fs.create_file("/templates/say_hello.sql", contents="hello!")
    app_runner.using_templates_under("/templates")\
               .select_template('1. say_hello.sql',{})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello!")\
               .assert_all_input_was_read()

def test_select_and_render_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello David!")\
               .assert_all_input_was_read()


def test_fills_two_templates_combines_output(app_runner,fs):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('hello.sql',{'name':'John'})\
               .select_template('bye.sql',{'name':'Mark'})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello John!\nbye Mark!")\
               .assert_all_input_was_read()
