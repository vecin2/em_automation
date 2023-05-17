from sqltask.main.main_menu_builder import PrintToConsoleConfig


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
