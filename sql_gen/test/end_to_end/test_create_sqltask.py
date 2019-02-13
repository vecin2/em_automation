import sys
import os

from io import StringIO

import pytest

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleCommandBuilder
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv

class FakeSQLRenderer(object):
    def __init__(self):
        self.rendered_sql=""

    def render_sql(self,sql_string):
        self.rendered_sql+=sql_string

class CommandTestFactory(CommandFactory):
    def __init__(self, print_sql_to_console_command=None):
        self.print_sql_to_console_command=print_sql_to_console_command

    def make_print_sql_to_console_command(self):
        return self.print_sql_to_console_command

class DummyEnvironment(object):
    def list_templates(self):
        return []

class AppRunner():
    def __init__(self):
        self.inputs=[]
        self.original_stdin = sys.stdin
        self.template_path=""
        self.environment =DummyEnvironment()

    def user_inputs(self,description, user_input):
        #description is used only for test readability
        self.inputs.append(user_input)
        self.sql_renderer = FakeSQLRenderer()
        return self

    def using_templates_under(self, templates_path):
        env_vars={'SQL_TEMPLATES_PATH':templates_path}
        self.environment = EMTemplatesEnv().get_env(env_vars)
        return self


    def run_print_SQL_to_console(self):
        self._run(['.'])
        return self

    def _run(self,args):
        sys.argv=args
        sys.stdin = StringIO(self._user_input_to_str())
        app_test_factory = CommandTestFactory(
                            self._make_test_print_sql_to_console_command())
        app = CommandLineSQLTaskApp(app_test_factory)
        app.run()

    def _make_test_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommandBuilder().\
                  with_sql_renderer(self.sql_renderer).\
                  with_environment(self.environment).\
                  build()

    def _make_emsqltemplate_env(self):
        return EMTemplatesEnv().get_env(self.env_vars)

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
    app_runner.user_inputs('template','x')\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("")

def test_asks_for_template_until_valid_entry(app_runner):
    app_runner.user_inputs('template','abc')\
               .user_inputs('template','x')\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("")\
               .assert_all_input_was_read()

def test_select_and_render_no_vals_template(app_runner,fs):
    fs.create_file("/templates/say_hello.sql", contents="hello!")

    app_runner.using_templates_under("/templates")\
               .user_inputs('template','1. say_hello.sql')\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello!")\
               .assert_all_input_was_read()

def test_select_and_render_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.using_templates_under("/templates")\
               .user_inputs('template','1. greeting.sql')\
               .user_inputs('name','David')\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello David!")\
               .assert_all_input_was_read()
