import os

import pyperclip

from sql_gen.ui.utils import select_item
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.app_project import AppProject
from sql_gen.emproject.emsvn import EMSvn
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
            initial_context=None):
        if initial_context is None:
            initial_context=init(AppProject(env_vars=env_vars))
        self.templates_path=EMTemplatesEnv().extract_templates_path(env_vars)
        self.initial_context =initial_context
        self.env_vars = env_vars

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

class CreateSQLTaskDisplayer(object):
    def ask_to_override_task(self,path):
        text= "Are you sure you want to override the task '"+ path + "' (y/n): "
        return select_item(text,['y','n'])

    def display_sqltask_created_and_path_in_clipboard(self,filepath):
        print("\nSQL task created under '"+filepath+"' and path copied to clipboard\n")

    def unable_to_rev_no_svn_not_installed(self,rev_no):
        message="Looks like SVN command line tool is not installed,\
 without it 'update.sequence' can not be computed and it is default to\
 'PROJECT $Revision: "+rev_no+" $'. Make sure you update it manually!!"
        print(message)
    def computing_rev_no(self):
        print ("Computing 'update.sequence' from current SVN number...")

class CreateSQLTaskCommand(object):
    def __init__(self,
                 env_vars=os.environ,
                 initial_context=None,
                 svn_client= None,
                 clipboard= pyperclip,
                 path=None):
        if initial_context is None:
            app_project=AppProject(env_vars=env_vars)
            initial_context = init(app_project)
        if svn_client is None:
            svn_client = EMSvn()
        self.path=path
        self.svn_client=svn_client
        self.env_vars=env_vars
        self.initial_context=initial_context
        self.displayer = CreateSQLTaskDisplayer()
        self.clipboard = clipboard

    def run(self):
        if os.path.exists(self.path) and not\
                self._user_wants_to_override():
            return

        sqltask = SQLTask(self.path)
        document=self._create_sql()
        sqltask.update_sequence_no= self._compute_update_seq_no()
        sqltask.write(document)
        self.clipboard.copy(self.path)
        self.displayer.display_sqltask_created_and_path_in_clipboard(self.path)
    def _user_wants_to_override(self):
        return self.displayer.ask_to_override_task(self.path) != "n"

    def _create_sql(self):
        displayer = PrintSQLToConsoleDisplayer()
        templates_path=EMTemplatesEnv().extract_templates_path(self.env_vars)
        self.doc_creator = CreateDocumentFromTemplateCommand(
                            templates_path,
                            displayer,
                            self.initial_context)
        self.doc_creator.run()
        return displayer.rendered_sql

    def _compute_update_seq_no(self):
        self.displayer.computing_rev_no()
        try:
            revision_no =int(self.svn_client.revision_number())
        except Exception:
            self.displayer.unable_to_rev_no_svn_not_installed("-1")
            return -1
        app_config =AppProject(env_vars=self.env_vars).config
        rev_no_offset = app_config.get('svn.rev.no.offset','0')
        return revision_no+ 1 + int(rev_no_offset)


class SQLTask(object):
    def __init__(self, path =None,update_sequence_no=None):
        self.path=path
        self.update_sequence_no = update_sequence_no

    def write(self,text):
        self.table_data=text
        self.update_sequence="PROJECT $Revision: "+\
                            str(self.update_sequence_no) +" $"
        if not os.path.exists(self.path):
                os.makedirs(self.path)
        with open(os.path.join(self.path,"tableData.sql"),"w") as f:
            f.write(self.table_data)
        with open(os.path.join(self.path,"update.sequence"),"w") as f:
            f.write(self.update_sequence)
