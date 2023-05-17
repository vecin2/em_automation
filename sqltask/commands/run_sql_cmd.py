from sqltask.main.main_menu_builder import RunSQLConfig


class RunSQLCommand:
    def __init__(self, project=None):
        self.project = project

    def run(self):
        main_menu = self.build_main_menu()
        main_menu.run()

    def build_main_menu(self):
        builder = RunSQLConfig().get_builder(self.project)
        return builder.build()
