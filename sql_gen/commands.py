from sql_gen.create_document_from_template_command import MultipleTemplatesDocGenerator,CreateDocumentFromTemplateCommand,TemplateSelector,SelectTemplateLoader

class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the ouput to console"""
    def __init__(self, doc_creator=None, displayer=None):
        self.doc_creator = doc_creator
        self.displayer = displayer
    def run(self):
        self.doc_creator.run()

class PrintSQLToConsoleDisplayer(object):
    def __init__(self):
        self.rendered_sql=""
    """Prints to console the command output"""
    def render_sql(self,sql_to_render):
        print(sql_to_render)
        self.rendered_sql+=sql_to_render

    def write(self,content):
        self.render_sql(content)


class PrintSQLToConsoleCommandBuilder(object):
    def __init__(self,
                 sql_renderer=PrintSQLToConsoleDisplayer(),
                 env_vars=None):
        self.sql_renderer=sql_renderer
        self.environment =None

    def with_sql_renderer(self,sql_renderer):
        self.sql_renderer = sql_renderer
        return self

    def with_environment(self,environment):
        self.environment = environment
        return self

    def build(self):
        action_selector=TemplateSelector(
                                SelectTemplateLoader(self.environment))
        return PrintSQLToConsoleCommand(
                    MultipleTemplatesDocGenerator(
                        CreateDocumentFromTemplateCommand(
                            action_selector,
                            self.sql_renderer
                        )
                    ),
                )
