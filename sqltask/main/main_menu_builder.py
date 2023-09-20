from sqltask.app_project import AppProject
from sqltask.database.sql_runner import (CommitTransactionExitListener,
                                         RollbackTransactionExitListener,
                                         SQLRunner)
from sqltask.docugen.render_template_handler import RenderTemplateHandler
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.main_menu import (ExitHandler, InputParser, MainMenu,
                               MainMenuDisplayer, MainMenuHandler, MenuOption)
from sqltask.sqltask_jinja.context import ContextBuilder
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv


class RendererBuilder(object):
    def __init__(self):
        self.listeners = []
        # self.context_builder = None
        self.context = None
        self.loader = None

    def append_listener(self, listener):
        self.listeners.append(listener)
        return self

    def with_loader(self, loader):
        self.loader = loader

    def build(self):
        template_renderer = TemplateFiller(initial_context=self.get_context())
        for listener in self.listeners:
            template_renderer.append_listener(listener)
        render_template_handler = RenderTemplateHandler(
            template_renderer,
            loader=self.loader,
        )
        return render_template_handler

    def with_context(self, context):
        self.context = context

    def get_context(self):
        if not self.context:
            self.context = self.context_builder.build()
        return self.context


class MainMenuBuilder(object):
    def __init__(self):
        self.template_renderer_listeners = []
        self.loader = None
        self.context_builder = None
        self.context = None
        self.exit_handler_listener = None
        # self.renderer_builder = RendererBuilder()
        self.options = None
        self.handlers = []

    @staticmethod
    def base_setup(project, templates_path):
        builder = MainMenuBuilder()
        return builder

    def register_render_listener(self, listener):
        self.renderer_builder.append_listener(listener)
        return self

    def get_context(self):
        if not self.context:
            self.context = self.context_builder.build()
        return self.context

    def with_loader(self, loader):
        self.loader = loader

    def get_exit_listeners(self, listener):
        self.exit_handler_listener = listener

    def append_handler(self, handler):
        self.handlers.append(handler)

    def build(self):
        menu_handler = MainMenuHandler(self.handlers)

        displayer = MainMenuDisplayer()
        return MainMenu(
            displayer=displayer,
            options=self.options,
            input_event_parser=InputParser(),
            handler=menu_handler,
            max_no_trials=10,
        )


class PrintToConsoleConfig(object):
    def __init__(self):
        """"""

    def get_builder(self, project):
        templates_path = project.library().templates_path
        loader = EMTemplatesEnv(templates_path)
        context = ContextBuilder(project).build()

        self.template_filler = TemplateFiller(initial_context=context)
        render_template_handler = RenderTemplateHandler(
            self.template_filler,
            loader=loader,
        )
        self.console_printer = PrintSQLToConsoleDisplayer()
        self.template_filler.append_listener(self.console_printer)

        sql_runner = SQLRunner(project)
        self.append_other_renderer_listeners(sql_runner)
        self.builder = MainMenuBuilder()
        self.builder.append_handler(render_template_handler)
        exit_handler = ExitHandler()
        self.append_exit_handler(exit_handler, sql_runner)
        self.builder.append_handler(exit_handler)
        self.builder.options = MenuOption.to_options(loader.list_visible_templates())

        return self.builder

    def get_renderer_handler_builder(self, loader, context, sql_runner):
        self.append_other_renderer_listeners(sql_runner)
        return self.renderer_builder

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

    def get_exit_listeners(self, sql_runner):
        #we do not want to commit when printing SQL
        return [RollbackTransactionExitListener(sql_runner)]


class RunSQLConfig(PrintToConsoleConfig):
    def __init__(self):
        super().__init__()

    def get_exit_listeners(self, sql_runner):
        return [CommitTransactionExitListener(sql_runner)]


class CreateSQLConfig(PrintToConsoleConfig):
    def __init__(self, update_seq_writer):
        super().__init__()
        self.update_seq_writer = update_seq_writer

    def get_exit_listeners(self, sql_runner):
        return [RollbackTransactionExitListener(sql_runner), self.update_seq_writer]

    def append_other_renderer_listeners(self, sql_runner):
        super().append_other_renderer_listeners(sql_runner)
        self.template_filler.append_listener(self.update_seq_writer)
        return self.template_filler


class VerifySQLConfig(PrintToConsoleConfig):
    def __init__(self):
        super().__init__()

    def append_other_renderer_listeners(self, project):
        """"""
        # Not run on db because we are only testing one template a time

    def append_exit_handler(self, exit_handler, sql_runner):
        """"""


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
