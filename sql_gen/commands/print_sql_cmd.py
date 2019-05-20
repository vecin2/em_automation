import os

from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand
from sql_gen.sqltask_jinja.context import ContextBuilder

class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""
    def __init__(self):
        self.rendered_sql=""

    def write(self,content):
        self.render_sql(content)

    def render_sql(self,sql_to_render):
        print("\n")
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
    """Command which generates a SQL script from a template and it prints the output to console"""
    def __init__(self, env_vars=os.environ,
            context_builder=None,
            emprj_path =None,
            templates_path=None):
        if context_builder is None:
            if emprj_path:
                context_builder = ContextBuilder(emprj_path=emprj_path)
            else:
                context_builder=ContextBuilder(AppProject(env_vars=env_vars))
        if templates_path:
            self.templates_path = templates_path
        else:
            self.templates_path=EMTemplatesEnv().extract_templates_path(env_vars)
        self.context_builder =context_builder

    def run(self):
        self.doc_writer = PrintSQLToConsoleDisplayer()
        self.doc_creator = CreateDocumentFromTemplateCommand(
                            self.templates_path,
                            self.doc_writer,
                            self.context_builder.build()
                        )
        self.doc_creator.run()

    def sql_printed(self):
        return self.doc_writer.rendered_sql

