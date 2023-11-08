from sqltask.commands.print_sql_cmd import PrintToConsoleConfig,PrintSQLToConsoleDisplayer
from sqltask.database.sql_runner import (CommitTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.render_template_handler import RenderTemplateHandler
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.main.main_menu_builder import MainMenuBuilder
from sqltask.main_menu import ExitHandler, MenuOption
from sqltask.sqltask_jinja.context import ContextBuilder
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv


class RunSQLCommand:
    def __init__(self, project=None):
        self.project = project

    def run(self):
        main_menu = self.build_main_menu()
        main_menu.run()

    def build_main_menu(self):
        builder = RunSQLConfig().get_builder(self.project)
        return builder.build()


class RunSQLConfig(PrintToConsoleConfig):
    def __init__(self):
        super().__init__()

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

    def get_exit_listeners(self, sql_runner):
        return [CommitTransactionExitListener(sql_runner)]

    def append_other_renderer_listeners(self, sql_runner):
        # If we are printing two templates, sql_runner
        # allows the second template to see the modification made
        # by the first template  (kenyames, entities inserted, etc)
        # builder.register_handler(ExitHandler())
        self.register_render_listener(sql_runner)
