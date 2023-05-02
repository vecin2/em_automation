from sqltask.app_project import AppProject
from sqltask.database.sql_runner import SQLRunner
from sqltask.docugen.render_template_handler import RenderTemplateHandler
from sqltask.docugen.template_filler import TemplateFiller
from sqltask.main_menu import (ExitHandler, InputParser, MainMenu,
                               MainMenuDisplayer, MainMenuHandler, MenuOption)
from sqltask.sqltask_jinja.sqltask_env import EMTemplatesEnv


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


class MainMenuBuilder(object):
    def __init__(self):
        self.displayer = None
        self.handler = None

    def with_displayer(self, displayer):
        self.displayer = displayer
        return self

    def with_handler(self, handler):
        self.handler = handler
        return self


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


class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the output to console"""

    def __init__(
        self,
        context_builder=None,
        templates_path=None,
        run_on_db=True,
        listener=None,
        project_root=None,
        main_menu=None,
    ):
        self.templates_path = templates_path
        self.context_builder = context_builder
        self.context = None
        self.listener = listener
        self.main_menu = main_menu

        # If we are printing two templates, running the sql
        # allow the second template to see the modification made
        # by the first template  (kenyames, entities inserted, etc)
        self.run_on_db = run_on_db
        self.sql_runner = None
        self.commit_changes = False
        self.project_root = project_root
        self._app_project = None

    @property
    def app_project(self):
        if not self._app_project:
            self._app_project = AppProject(emprj_path=self.project_root)
        return self._app_project

    def run(self):
        if not self.context:
            self.context = self.context_builder.build()

        self.console_printer = PrintSQLToConsoleDisplayer()

        self.main_menu = self.build_main_menu()
        self.main_menu.run()
        # pyperclip.copy(self.sql_printed())
        # self.get_sql_runner().on_finish()

    def write(self, content, template=None):
        if self.listener:
            self.listener.write(content, template)

    def build_main_menu(self):
        loader = EMTemplatesEnv(self.templates_path)

        template_renderer = TemplateFiller(initial_context=self.context)
        template_renderer.append_listener(self.get_sql_runner())
        template_renderer.append_listener(self.console_printer)
        render_template_handler = RenderTemplateHandler(
            template_renderer,
            loader=loader,
            listener=self,
        )
        exit_handler = ExitHandler(self.get_sql_runner())
        # display_template_test_handler = DisplayTemplateTestHandler(self.app_project.library())
        menu_handler = MainMenuHandler([render_template_handler, exit_handler])

        displayer = MainMenuDisplayer()
        return MainMenu(
            displayer=displayer,
            options=MenuOption.to_options(loader.list_visible_templates()),
            input_event_parser=InputParser(),
            handler=menu_handler,
            max_no_trials=10,
        )

    def get_sql_runner(self):
        if not self.sql_runner:
            self.sql_runner = SQLRunner(
                self.context, self.run_on_db, self.commit_changes
            )
        return self.sql_runner

    def sql_printed(self):
        return self.console_printer.rendered_sql
