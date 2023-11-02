from sqltask.commands.print_sql_cmd import PrintToConsoleConfig
from sqltask.database.sql_runner import CommitTransactionExitListener


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

    def get_exit_listeners(self, sql_runner):
        return [CommitTransactionExitListener(sql_runner)]

    def append_other_renderer_listeners(self, sql_runner):
        # If we are printing two templates, sql_runner
        # allows the second template to see the modification made
        # by the first template  (kenyames, entities inserted, etc)
        # builder.register_handler(ExitHandler())
        self.register_render_listener(sql_runner)
