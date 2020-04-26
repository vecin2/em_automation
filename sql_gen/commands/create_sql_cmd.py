import os

import pyperclip

from sql_gen.ui.utils import select_string_noprompt,prompt_suggestions
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.sqltask_jinja.context import ContextBuilder
from sql_gen.app_project import AppProject
from sql_gen.emproject.emsvn import EMSvn
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand
from sql_gen.commands.print_sql_cmd import PrintSQLToConsoleDisplayer,PrintSQLToConsoleCommand

class CreateSQLTaskDisplayer(object):
    def ask_to_override_task(self,path):
        text= "Are you sure you want to override the task '"+ path + "' (y/n): "
        return select_string_noprompt(text,['y','n'])

    def ask_for_sqlmodulename(self,options):
        text= "\nPlease enter the sql module name: "
        return prompt_suggestions(text,options)

    def ask_for_sqltaskname(self,options):
        text= "\nPlease enter the task name (e.g. overrideCustomer): "
        return input(text)

    def display_sqltask_created_and_path_in_clipboard(self,filepath):
        print("\nSQL task created under '"+filepath+"' and path copied to clipboard\n")

    def unable_to_rev_no_svn_not_installed(self,rev_no):
        message="Looks like SVN command line tool is not installed,\
 without it 'update.sequence' can not be computed and it is default to\
 'PROJECT $Revision: "+rev_no+" $'. Make sure you update it manually!!"
        print(message)

    def computing_rev_no(self):
        print ("Computing 'update.sequence' from current SVN number...")
    def update_seq_no_computed(self, number):
        print("update.sequence is '"+str(number)+"'")

class CreateSQLTaskCommand(object):
    def __init__(self,
                 env_vars=os.environ,
                 context_builder=None,
                 svn_client= None,
                 clipboard= pyperclip,
                 path=None,
                 template_name=None,
                 template_values={},
                 run_once=False):
        self._app_project=None
        self.env_vars=env_vars
        if context_builder is None:
            app_project=AppProject(env_vars=env_vars)
            context_builder = ContextBuilder(app_project)
        if svn_client is None:
            svn_client = EMSvn()
        self.path=path
        self.svn_client=svn_client
        self.context_builder=context_builder
        self.displayer = CreateSQLTaskDisplayer()
        self.clipboard = clipboard
        self.sqltask = None
        self.template_name= template_name
        self.template_values= template_values
        self.run_once = run_once
    @property
    def app_project(self):
        if not self._app_project:
            self._app_project=AppProject(env_vars=self.env_vars)
        return self._app_project

    def run(self):
        if not self.path:
            self.path = self._compute_path()
        if os.path.exists(self.path) and not\
                self._user_wants_to_override():
            return

        self.sqltask = SQLTask(self.path)
        document=self._create_sql()
        self.sqltask.update_sequence_no= self._compute_update_seq_no()
        self.sqltask.write("") # creates update.sequence
        self.clipboard.copy(self.path)
        self.displayer.display_sqltask_created_and_path_in_clipboard(self.path)

    @property
    def emproject(self):
        return self.app_project.emproject

    def _compute_path(self):
        prj_repo_modules_path=self.emproject.paths['sql_modules'].path
        options = self._get_modules(prj_repo_modules_path)

        module_name=self.displayer.ask_for_sqlmodulename(options)
        sqltask_name=self.displayer.ask_for_sqltaskname(options)

        release_name=self.app_project.config['db.release.version']
        return os.path.join(self.app_project.emproject.root,
                             "modules/"+module_name+"/sqlScripts/oracle/updates/"+release_name+"/"+sqltask_name)
    def _get_modules(self, key_path):
        return next(os.walk(key_path))[1]

    def _user_wants_to_override(self):
        return self.displayer.ask_to_override_task(self.path) != "n"

    def _create_sql(self):
        displayer = PrintSQLToConsoleDisplayer()
        templates_path=EMTemplatesEnv().extract_templates_path(self.env_vars)
        print_sql_cmd = PrintSQLToConsoleCommand(
                            context_builder=self.context_builder,
                            env_vars=self.env_vars,
                            listener=self,
                            template_name=self.template_name,
                            template_values=self.template_values,
                            run_once=self.run_once)
        print_sql_cmd.run()
        return print_sql_cmd.sql_printed()

    def on_written(self,content,template):
        self.sqltask.write(content)

    def _compute_update_seq_no(self):
        self.displayer.computing_rev_no()
        try:
            revision_no =int(self.svn_client.revision_number())
        except Exception:
            self.displayer.unable_to_rev_no_svn_not_installed("-1")
            return -1
        app_config =AppProject(env_vars=self.env_vars).config
        rev_no_offset = app_config.get('svn.rev.no.offset','0')
        result = revision_no+ 1 + int(rev_no_offset)
        self.displayer.update_seq_no_computed(result)
        return result


class SQLTask(object):
    def __init__(self, path =None,update_sequence_no=None):
        self.path=path
        self.update_sequence_no = update_sequence_no

    def write(self,sql):
        self._write_sql(sql)
        if self.update_sequence_no:
            self._write_update_sequence()

    def _write_sql(self,text):
        self.table_data=text
        if not os.path.exists(self.path):
                os.makedirs(self.path)
        with open(os.path.join(self.path,"tableData.sql"),"a+") as f:
            f.write(self.table_data)

    def _write_update_sequence(self):
        self.update_sequence="PROJECT $Revision: "+\
                            str(self.update_sequence_no) +" $"
        with open(os.path.join(self.path,"update.sequence"),"w") as f:
            f.write(self.update_sequence)
