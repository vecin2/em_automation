import sys
from io import StringIO

import pytest

from sql_gen.command_line_app import CommandLineSQLTaskApp
from sql_gen.command_factory import CommandFactory
from sql_gen.commands import PrintSQLToConsoleCommand
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand,TemplateSelector,TemplateFiller, SelectTemplateLoader,SelectTemplateDisplayer

class FakeSQLRenderer(object):
    def __init__(self):
        self.rendered_sql=""

    def render_sql(self,sql_string):
        self.rendered_sql+=sql_string

class CommandTestFactory(CommandFactory):
    def __init__(self,
                 sql_renderer=FakeSQLRenderer(),
                 select_template_loader=SelectTemplateLoader()):
        self.sql_renderer = sql_renderer
        self.select_template_loader=select_template_loader

    def _make_print_to_console_displayer(self):
        return self.sql_renderer

class AppRunner():
    def with_user_inputs(self,user_inputs):
        self.user_inputs =user_inputs
        self.sql_renderer = FakeSQLRenderer()
        return self

    def run_print_SQL_to_console(self):
        self.run(['.'])
        return self

    def run(self,args):
        sys.argv=args
        sys.stdin = StringIO(self._user_input_to_str())
        app_test_factory = CommandTestFactory(self.sql_renderer)
        app = CommandLineSQLTaskApp(app_test_factory)
        app.run()

    def _user_input_to_str(self):
        str_input_lines=""
        for user_input in self.user_inputs.values():
            if str_input_lines is not "":
                str_input_lines+="\n"
            str_input_lines += user_input
        return str_input_lines

    def assert_rendered_sql(self,expected_sql):
        assert expected_sql == self.sql_renderer.rendered_sql



def test_returns_empty_when_no_template_selected():
    AppRunner().with_user_inputs({'template':'x'})\
              .run_print_SQL_to_console()\
              .assert_rendered_sql("")

