import os

from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand
from sql_gen.sqltask_jinja.context import init

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
    """Command which generates a SQL script from a template and it prints the output to console"""
    def __init__(self, env_vars=os.environ,
            initial_context=None,
            emprj_path =None,
            templates_path=None):
        if initial_context is None:
            if emprj_path:
                initial_context = init(emprj_path=emprj_path)
            else:
                initial_context=init(AppProject(env_vars=env_vars))
        if templates_path:
            self.templates_path = templates_path
        else:
            self.templates_path=EMTemplatesEnv().extract_templates_path(env_vars)
        self.initial_context =initial_context

    def run(self):
        self.doc_writer = PrintSQLToConsoleDisplayer()
        self.doc_creator = CreateDocumentFromTemplateCommand(
                            self.templates_path,
                            self.doc_writer,
                            self.initial_context
                        )
        self.doc_creator.run()

    def sql_printed(self):
        return self.doc_writer.rendered_sql

