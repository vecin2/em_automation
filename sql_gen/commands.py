from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand,TemplateSelector,TemplateFiller,SelectTemplateLoader,SelectTemplateDisplayer

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

class PrintSQLToConsoleCommandBuilder(object):
    def __init__(self):
        self._sql_renderer=""
    def sql_renderer(self):
        if self._sql_renderer:
            return self._sql_renderer
        else:
            return PrintSQLToConsoleDisplayer()

    def with_sql_renderer(self,sql_renderer):
        self._sql_renderer = sql_renderer
        return self

    def build(self):
        return PrintSQLToConsoleCommand(
                    CreateDocumentFromTemplateCommand(
                            TemplateSelector(
                                    SelectTemplateLoader(),
                                    SelectTemplateDisplayer()),
                            TemplateFiller()),
                    self.sql_renderer())
