import sys
from io import StringIO

import pytest

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleCommandBuilder
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand,TemplateSelector,TemplateFiller, SelectTemplateLoader,SelectTemplateDisplayer

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

class AppRunner():
    def with_user_inputs(self,user_inputs):
        self.user_inputs =user_inputs
        self.sql_renderer = FakeSQLRenderer()
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
                  build()

    def _user_input_to_str(self):
        return "\n".join([user_input for user_input in self.user_inputs.values()])

    def assert_rendered_sql(self,expected_sql):
        assert expected_sql == self.sql_renderer.rendered_sql



def test_returns_empty_when_no_template_selected():
    AppRunner().with_user_inputs({'template':'x'})\
              .run_print_SQL_to_console()\
              .assert_rendered_sql("")

def test_returns_empty_when_no_template_selected():
    AppRunner().with_user_inputs({'template':'x'})\
              .run_print_SQL_to_console()\
              .assert_rendered_sql("")

