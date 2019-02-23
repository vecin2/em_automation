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

class CreateSQLTaskCommand(object):
    def __init__(self,
                 env_vars=os.environ,
                 initial_context={},
                 svn_client= None,
                 path=None):
        self.path=path
        self.svn_client=svn_client
        self.env_vars=env_vars
        self.initial_context=initial_context

    def run(self):
        self.sqltask =SQLTask(self.path,self.svn_client);
        self.doc_creator = CreateDocumentFromTemplateCommand(
                            self.env_vars,
                            self.sqltask,
                            self.initial_context
                        )
        self.doc_creator.run()


class SQLTask(object):
    def __init__(self,
                 path =None,
                 svn_client=None):
        self.path=path
        self.svn_client=svn_client

    def write(self,text):
        self.table_data=text
        update_sequence_no=int(self.svn_client.current_rev_no())+1
        self.update_sequence="PROJECT $Revision: "+\
                            str(update_sequence_no)
        os.makedirs(self.path)
        with open(os.path.join(self.path,"tableData.sql"),"w") as f:
            f.write(self.table_data)
        with open(os.path.join(self.path,"update.sequence"),"w") as f:
            f.write(self.update_sequence)
