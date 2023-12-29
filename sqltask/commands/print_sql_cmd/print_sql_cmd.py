import pyperclip
from rich.console import Console
from rich.syntax import Syntax

from sqltask.database.sql_runner import (RollbackTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.shell.prompt import (ActionRegistry, Editor, EditTemplateAction,
                                  ExitAction, ProcessTemplateAction,
                                  RenderTemplateAction, ViewTemplateDocsAction,
                                  ViewTemplateInfoAction)
from sqltask.shell.shell_factory import ShellBuilder, PrintSQLToConsoleDisplayer
from sqltask.sqltask_jinja.context import ContextBuilder
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sqltask.ui.sql_styler import SQLStyler


class ClipboardCopier:
    def __init__(self):
        self.styler = SQLStyler()

    def write(self, content, template=None):
        return self.styler.append_sql(content)

    def on_finish(self):
        return pyperclip.copy(self.styler.text())



class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the output to console"""

    def __init__(self, project=None):
        self.project = project

    def sql_printed(self):
        return self.displayer.rendered_sql

    def run(self):
        self.displayer = PrintSQLToConsoleDisplayer()
        builder = ShellBuilder()
        builder.project(self.project)
        builder.displayer(self.displayer)
        shell = builder.build()
        shell.run()

