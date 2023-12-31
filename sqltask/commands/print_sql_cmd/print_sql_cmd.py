import pyperclip

from sqltask.shell.shell_factory import InteractiveSQLTemplateRunnerBuilder
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
        builder = InteractiveSQLTemplateRunnerBuilder.default(self.project)
        clipboard_copier = ClipboardCopier()
        builder.append_template_rendered_listener(clipboard_copier)
        builder.append_exit_listener(clipboard_copier)
        shell = builder.build()
        self.displayer = builder.displayer
        shell.run()
