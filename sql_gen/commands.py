
class PrintSQLToConsoleCommand(object):
    """"""
    def __init__(self, doc_creator=None, displayer=None):
        self.doc_creator = doc_creator
        self.displayer = displayer
    def run(self):
        output = self.doc_creator.run()
        self.displayer.render_sql(output)

class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""
    def render_sql(self,sql_to_render):
        print(sql_to_render)

