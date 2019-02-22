import os
from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.context import init
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand

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

class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the ouput to console"""
    def __init__(self, env_vars=os.environ,
                       doc_writer=PrintSQLToConsoleDisplayer(),
                       initial_context=init(AppProject())):
        self.doc_creator = CreateDocumentFromTemplateCommand(
                            env_vars,
                            doc_writer,
                            initial_context
                        )

    def run(self):
        self.doc_creator.run()

    def sql_printed(self):
        return self.doc_creator.generated_doc()

class CreateSQLTaskCommand(PrintSQLToConsoleCommand):
    def __init__(self,
                 env_vars=os.environ,
                 doc_writer=None,
                 initial_context={}):
        self.doc_writer =doc_writer
        super().__init__(env_vars,doc_writer,initial_context)
        self.path = ""

    def run(self):
        self.doc_writer.path = self.path
        super().run()


