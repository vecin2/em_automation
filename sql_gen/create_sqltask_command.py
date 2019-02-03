class TemplateFillingApp(object):
    def __init__(self):
        """"""
    def run(self):
        return "hello"

class CreateSQLTaskCommand(object):
    def __init__(self, outputwriter=None, displayer=None):
        self.displayer =displayer
        self.outputwriter=outputwriter

    def run(self):
        sql =TemplateFillingApp().run()
        self.outputwriter.write(sql)
