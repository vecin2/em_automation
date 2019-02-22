import os
from sql_gen.commands import PrintSQLToConsoleCommand
class TemplateFillingApp(object):
    def __init__(self):
        """"""
    def run(self):
        return "hello"

class CreateSQLTaskCommand(PrintSQLToConsoleCommand):
    def __init__(self,
                 env_vars=os.environ,
                 doc_writer=None,
                 initial_context={}):
        super().__init__(env_vars,doc_writer,initial_context)
    #def __init__(self, outputwriter=None, displayer=None):
    #    self.displayer =displayer
    #    self.outputwriter=outputwriter

    #def run(self):
    #    sql =TemplateFillingApp().run()
    #    self.outputwriter.write(sql)
