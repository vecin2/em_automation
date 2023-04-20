from sql_gen.app_project import AppProject
from sql_gen.database.sql_runner import SQLRunner
from sql_gen.docugen.render_template_handler import RenderTemplateHandler
from sql_gen.docugen.template_filler import TemplateFiller
from sql_gen.help import DisplayTemplateTestHandler
from sql_gen.main_menu import (ExitHandler, InputParser, MainMenu,
                               MainMenuDisplayer, MainMenuHandler, MenuOption)
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv


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
        project_root=None
    ):
        self.templates_path = templates_path
        self.context_builder = context_builder
        self.context = None
        self.listener = listener

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

        main_menu = self.build_main_menu()
        main_menu.run()
        # pyperclip.copy(self.sql_printed())
        self.get_sql_runner().on_finish()

    def build_main_menu(self):
        loader = EMTemplatesEnv(self.templates_path)

        self.console_printer = PrintSQLToConsoleDisplayer()

        template_renderer = TemplateFiller(initial_context=self.context)
        render_template_handler = RenderTemplateHandler(
            template_renderer,
            loader=loader,
            listener=self,
        )
        exit_handler = ExitHandler()
        # display_template_test_handler = DisplayTemplateTestHandler(self.app_project.library())
        menu_handler = MainMenuHandler(
            [render_template_handler,  exit_handler]
        )

        displayer = MainMenuDisplayer()
        return MainMenu(
            displayer=displayer,
            options=MenuOption.to_options(loader.list_visible_templates()),
            input_event_parser=InputParser(),
            handler=menu_handler,
            max_no_trials=10,
        )

    def write(self, content, template=None):
        self.console_printer.write(content)
        self.sql_runner = self.get_sql_runner()
        result = self.sql_runner.write(content, template)
        if self.listener:
            self.listener.on_written(content, template)
        return result

    def get_sql_runner(self):
        if not self.sql_runner:
            self.sql_runner = SQLRunner(
                self.context, self.run_on_db, self.commit_changes
            )
        return self.sql_runner

    def _db(self):
        return self.context["_database"]

    def sql_printed(self):
        return self.console_printer.rendered_sql
