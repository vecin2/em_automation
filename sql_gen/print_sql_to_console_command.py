from sql_gen.fill_composed_template_command import FillComposedTemplateCommand

class PrintSQLToConsoleCommand(object):
    """"""
    def __init__(self, displayer=None):
        self.displayer = displayer
    def run(self):
        output = FillComposedTemplateCommand().run()
        self.displayer.render_sql(output)

class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""
    def render_sql(self,sql_to_render):
        print(sql_to_render)

