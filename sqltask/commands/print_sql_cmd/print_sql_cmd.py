import pyperclip
from rich.console import Console
from rich.syntax import Syntax

from sqltask.database.sql_runner import (RollbackTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.shell.prompt import (ActionRegistry, ExitAction,
                                  InteractiveTaskFinder, ProcessTemplateAction,
                                  RenderTemplateAction, ViewTemplateInfoAction)
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


class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""

    def __init__(self):
        self.rendered_sql = ""

    def write(self, content, template=None):
        self.render_sql(content)

    def render_sql(self, sql_to_render):
        print("\n")
        syntax = Syntax(
            sql_to_render, "sql", theme="monokai", line_numbers=False, word_wrap=True
        )
        console = Console()
        console.print(syntax)
        print("\n")
        self._append_rendered_text(sql_to_render)

    def _append_rendered_text(self, text):
        if self.rendered_sql != "" and text != "":
            self.rendered_sql += "\n"
        self.rendered_sql += text

    def current_text(self):
        return self.rendered_text


class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the output to console"""

    def __init__(self, project=None):
        self.project = project

    def run(self):
        finder = InteractiveTaskFinder(self._create_actions_registry())
        finder.run()

    def _create_actions_registry(self):
        registry = ActionRegistry()
        library = self.project.library()
        loader = EMTemplatesEnv(library)
        context_builder = ContextBuilder(self.project)
        context = context_builder.build()
        template_filler = TemplateFiller(initial_context=context)
        sql_runner = SQLRunner(self.project.db)
        clipboard_copier = ClipboardCopier()
        template_filler.append_listener(sql_runner)
        self.console_printer = PrintSQLToConsoleDisplayer()
        template_filler.append_listener(self.console_printer)
        template_filler.append_listener(clipboard_copier)

        render_template_action = RenderTemplateAction(template_filler, loader)
        process_template_action = ProcessTemplateAction(loader, render_template_action)
        registry.register(process_template_action)
        process_template_action.register("--info", ViewTemplateInfoAction(library))
        exit_action = ExitAction()
        exit_action.append_listener(RollbackTransactionExitListener(sql_runner))
        exit_action.append_listener(clipboard_copier)
        registry.register(exit_action)

        return registry

    def sql_printed(self):
        return self.console_printer.rendered_sql
