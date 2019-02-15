import os
from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.sqltask_jinja.context import init
from sql_gen.create_document_from_template_command import TemplateSelector,SelectTemplateLoader,MultipleTemplatesDocGenerator,CreateDocumentFromTemplateCommand
class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the ouput to console"""
    def __init__(self, doc_creator):
        self.doc_creator = doc_creator

    def run(self):
        self.doc_creator.run()

    def sql_printed(self):
        return self.doc_creator.generated_doc()

class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""
    def __init__(self):
        self.rendered_sql=""

    def write(self,content):
        self.render_sql(content)

    def render_sql(self,sql_to_render):
        print(sql_to_render)
        self._append_rendered_text(sql_to_render)

    def _append_rendered_text(self,text):
        if self.rendered_sql is not "" and\
            text is not "":
           self.rendered_sql+="\n"
        self.rendered_sql+=text

    def current_text(self):
        return self.rendered_text

class PrintSQLToConsoleCommandFactory(object):
    def make(self, env_vars=os.environ):
        self.env_vars = env_vars
        return PrintSQLToConsoleCommandBuilder().\
                    with_action_seletor(self._make_action_selector()).\
                    with_doc_writer(self._make_doc_writer()).\
                    build()

    def _make_action_selector(self):
        return TemplateSelector(self._make_template_selector())

    def _make_template_selector(self):
        return SelectTemplateLoader(self._make_template_env(),
                                    self._make_initial_context())

    def _make_template_env(self):
        return EMTemplatesEnv().get_env(self.env_vars)

    def _make_doc_writer(self):
        return PrintSQLToConsoleDisplayer()

    def _make_initial_context(self):
        app = AppProject()
        return init(app)
        logger = app.setup_logger()
        logger.info("Initializing app which is pointing currently to '"+app.emproject.root+"'")
        


class PrintSQLToConsoleCommandBuilder(object):
    def __init__(self):
        self.sql_renderer=None
        self.action_selector =None
        self.doc_writer =None

    def with_action_seletor(self,action_selector):
        self.action_selector=action_selector
        return self

    def with_doc_writer(self,doc_writer):
        self.doc_writer =doc_writer
        return self

    def build(self):
        return PrintSQLToConsoleCommand(
                    MultipleTemplatesDocGenerator(
                        CreateDocumentFromTemplateCommand(
                            self.action_selector,
                            self.doc_writer
                        )
                    ),
                )
