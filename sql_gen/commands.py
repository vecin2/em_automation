from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand,TemplateSelector,SelectTemplateLoader

class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the ouput to console"""
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
    def __init__(self,
                 sql_renderer=PrintSQLToConsoleDisplayer(),
                 env_vars=None):
        self.sql_renderer=sql_renderer
        self.environment =None
        #self.environment=EMTemplatesEnv.get_env(env_vars)

    def with_sql_renderer(self,sql_renderer):
        self.sql_renderer = sql_renderer
        return self

    def with_environment(self,environment):
        self.environment = environment
        return self

    def build(self):
        return PrintSQLToConsoleCommand(
                    CreateDocumentFromTemplateCommand(
                            TemplateSelector(
                                    SelectTemplateLoader(self.environment))),
                    self.sql_renderer)
