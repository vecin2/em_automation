import os
from sql_gen.ui.utils import select_item
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

class CreateSQLTaskDisplayer(object):
    def ask_to_override_task(self,path):
        text= "Are you sure you want to override the task '"+ path + "' (y/n): "
        return select_item(text,['y','n'])

class SvnClient(object):
    def __init__(self, rev_no):
        self.rev_no =rev_no

    def current_rev_no(self):
        return self.rev_no

class CreateSQLTaskCommand(object):
    def __init__(self,
                 env_vars=os.environ,
                 initial_context=init(AppProject()),
                 svn_client= SvnClient("123"),
                 path=None):
        self.path=path
        self.svn_client=svn_client
        self.env_vars=env_vars
        self.initial_context=initial_context
        self.displayer = CreateSQLTaskDisplayer()

    def run(self):
        if os.path.exists(self.path) and not\
                self._user_wants_to_override():
            return

        sqltask = SQLTask(self.path,
                          self._compute_update_seq_no())
        sqltask.write(self._create_sql())

    def _user_wants_to_override(self):
        return self.displayer.ask_to_override_task(self.path) != "n"

    def _create_sql(self):
        displayer = PrintSQLToConsoleDisplayer()
        self.doc_creator = CreateDocumentFromTemplateCommand(
                            self.env_vars,
                            displayer,
                            self.initial_context)
        self.doc_creator.run()
        return displayer.rendered_sql

    def _compute_update_seq_no(self):
        rev_no_offset = AppProject(env_vars=self.env_vars).\
                                config.get('svn.rev.no.offset','0')
        return 1+ int(self.svn_client.current_rev_no())+int(rev_no_offset)


class SQLTask(object):
    def __init__(self, path =None,update_sequence_no=None):
        self.path=path
        self.update_sequence_no = update_sequence_no

    def write(self,text):
        self.table_data=text
        self.update_sequence="PROJECT $Revision: "+\
                            str(self.update_sequence_no)
        if not os.path.exists(self.path):
                os.makedirs(self.path)
        with open(os.path.join(self.path,"tableData.sql"),"w") as f:
            f.write(self.table_data)
        with open(os.path.join(self.path,"update.sequence"),"w") as f:
            f.write(self.update_sequence)
