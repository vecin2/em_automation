import pyperclip

from sqltask.database.sql_runner import (RollbackTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.render_template_handler import RenderTemplateHandler
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.main.main_menu_builder import MainMenuBuilder
from sqltask.main_menu import ExitHandler, MenuOption
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
        print(sql_to_render)
        self._append_rendered_text(sql_to_render)

    def _append_rendered_text(self, text):
        if self.rendered_sql != "" and text != "":
            self.rendered_sql += "\n"
        self.rendered_sql += text

    def current_text(self):
        return self.rendered_text


class RenderTemplateHandlerBuilder(object):
    def __init__(self):
        self.displayer = None
        self.renderer = None
        self.context_builder = None
        self.loader = None

    def with_template_renderer(self, renderer):
        self.renderer = renderer
        return self

    def with_context_builder(self, context_builder):
        self.context_builder = context_builder
        return self

    def with_template_loader(self, loader):
        self.loader = loader
        return self


class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the output to console"""

    def __init__(self, project=None):
        self.project = project

    def run(self):
        main_menu = self.build_main_menu()
        main_menu.run()

    def build_main_menu(self):
        config = PrintToConsoleConfig()
        builder = config.get_builder(self.project)
        self.console_printer = config.console_printer
        return builder.build()

    def sql_printed(self):
        return self.console_printer.rendered_sql


class PrintToConsoleConfig(object):
    def __init__(self):
        """"""

    def get_builder(self, project, context_builder=None):
        loader = EMTemplatesEnv(project.library())

        self.builder = MainMenuBuilder()
        self.builder.options = MenuOption.to_options(loader.list_visible_templates())

        self.template_filler = self.make_template_filler(project, context_builder)
        self.console_printer = PrintSQLToConsoleDisplayer()
        self.template_filler.append_listener(self.console_printer)

        sql_runner = SQLRunner(project.db)
        self.append_other_renderer_listeners(sql_runner)
        self.builder.append_handler(
            self.make_template_renderer_handler(self.template_filler, loader)
        )
        exit_handler = ExitHandler()
        self.append_exit_handler(exit_handler, sql_runner)
        self.builder.append_handler(exit_handler)

        return self.builder

    def make_template_filler(self, project, context_builder):
        if not context_builder:
            context_builder = ContextBuilder(project)
        context = context_builder.build()
        return TemplateFiller(initial_context=context)

    def make_template_renderer_handler(self, template_filler, loader):
        return RenderTemplateHandler(
            self.template_filler,
            loader=loader,
        )

    def append_exit_handler(self, exit_handler, sql_runner):
        exit_handler.append_listeners(self.get_exit_listeners(sql_runner))

    def register_render_listener(self, listener):
        self.template_filler.append_listener(listener)

    def append_other_renderer_listeners(self, sql_runner):
        # If we are printing two templates, sql_runner
        # allows the second template to see the modification made
        # by the first template  (kenyames, entities inserted, etc)
        # builder.register_handler(ExitHandler())
        self.register_render_listener(sql_runner)
        self.clipboard_copier = ClipboardCopier()
        self.register_render_listener(self.clipboard_copier)

    def get_exit_listeners(self, sql_runner):
        # we do not want to commit when printing SQL
        return [RollbackTransactionExitListener(sql_runner), self.clipboard_copier]
