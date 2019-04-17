import os
import sys
import ast
import re

from io import StringIO

import pytest
import pyperclip
from jinja2 import Template

from sql_gen.ui.utils import select_string_noprompt,prompt_suggestions
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
                 initial_context=None,
                 svn_client= None,
                 clipboard= pyperclip,
                 path=None):
        self._app_project=None
        self.env_vars=env_vars
        if initial_context is None:
            app_project=AppProject(env_vars=env_vars)
            initial_context = init(app_project)
        if svn_client is None:
            svn_client = EMSvn()
        self.path=path
        self.svn_client=svn_client
        self.initial_context=initial_context
        self.displayer = CreateSQLTaskDisplayer()
        self.clipboard = clipboard
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

        sqltask = SQLTask(self.path)
        document=self._create_sql()
        sqltask.update_sequence_no= self._compute_update_seq_no()
        sqltask.write(document)
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
        result = revision_no+ 1 + int(rev_no_offset)
        self.displayer.update_seq_no_computed(result)
        return result


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

class TestGenerator(object):
    #render_sql_test_content=
    def __init__(self,env_vars=None):
        self.tests =[]
        self.env_vars = env_vars
        self.testdir =None
        self.content=""

    def testfilepath(self):
            return self.testdir+"/test_all_templates.py"

    def set_testdir(self,testdir):
        self.testdir = testdir

    def generate(self,**kwargs):
        test_content="""
def test_rendering_{{template_name}}_matches_expected_sql():
    assert "{{expected}}" == "{{actual}}"
"""
        template = Template(test_content)
        if self.content:
            self.content +="\n\n"
        current_content = template.render(kwargs)
        self.content +=current_content
        return current_content


class TestTemplatesCommandDisplayer(object):
    def test_folder_does_no_exist(self,directory):
        print("Test folder '"+directory+"' does not exist.")

class TestTemplatesCommand(PrintSQLToConsoleCommand):
    def __init__(self,
                 env_vars=os.environ,
                 initial_context=None,
                 pytest=pytest,
                 testgen= None):
        super().__init__(env_vars=env_vars,
                         initial_context=initial_context)
        self.app_project = AppProject(env_vars=self.env_vars)
        self.pytest =pytest
        self.displayer = TestTemplatesCommandDisplayer()
        if not testgen:
            testgen = TestGenerator(self.env_vars)
        self.testgen =testgen

    def testfilepath(self):
            return self._tmp_folder()+"/test_all_templates.py"

    def run(self):
        testpath=self.app_project.paths["test_templates"].path
        if not os.path.exists(testpath):
            self.displayer.test_folder_does_no_exist(testpath)
            return
        for filename in os.listdir(testpath):
            filepath = os.path.join(testpath,filename)
            if self._is_valid_test_file(filepath):
                self._generate_test(filepath)
        if self.testgen.content:
            test_file = open(self.testfilepath(),"w")
            test_file.write(self.testgen.content)
            test_file.close()
        self.pytest.main(['-x','-v',self._tmp_folder()])

    def _is_valid_test_file(self,filepath):
            filename = os.path.basename(filepath)
            extension = os.path.splitext(filename)[1]
            return os.path.isfile(filepath)\
                    and extension==".sql"\
                    and self._matches_template(filename)

    def _matches_template(self, test_file):
        path = EMTemplatesEnv().get_templates_path(self.env_vars)
        for template_file in os.listdir(path):
            template_name = os.path.splitext(template_file)[0]
            if template_name == self._extract_template_name(test_file):
                return True

        return False

    def _tmp_folder(self):
        tmp_testdir=self.app_project.paths["test_templates_tmp"].path
        if not os.path.exists(tmp_testdir):
            os.makedirs(tmp_testdir)
        return tmp_testdir

    def _generate_test(self,filepath):
        filename =os.path.basename(filepath) 
        test_file = open(filepath,"r+")
        expected = self._remove_first_line(test_file.read())
        actual =self._run_test(filepath)
        template_name =self._extract_template_name(filename)
        self.testgen.set_testdir(self._tmp_folder())
        self.testgen.generate(template_name=template_name,
                                          expected=expected,
                                          actual=actual)

    def _run_test(self,filepath):
            sys.stdin = StringIO(self._user_input_to_str(filepath))
            super().run()
            test_file = open(filepath,"r+")
            expected = self._remove_first_line(test_file.read())
            return self.sql_printed()

    def _user_input_to_str(self,filepath):
        filename =os.path.basename(filepath) 
        inputs=[]
        inputs.append(self._remove_prefix("test_",filename))
        with open(filepath) as f:
             first_line = self._remove_prefix("--",f.readline())
             temp_values =ast.literal_eval(first_line)
        for key in temp_values:
            inputs.append(temp_values[key])
        inputs.append("x")
        return "\n".join([input for input in inputs])

    def _extract_template_name(self,filename):
        return self._remove_prefix("test_",filename).split(".")[0]

    def _remove_prefix(self,prefix, string):
        if string.startswith(prefix):
            return string[len(prefix):].strip()
        return string

    def _remove_first_line(self,string):
        print("string is "+string)
        result= re.sub(r'^[^\n]*\n', '', string)
        print("filepath is "+result)
        return result.replace("\n","")



        #app_runner = PrintSQLToConsoleAppRunner()
        #app_runner.using_templates_under("/templates")\
        #           .select_template('1. greeting.sql',{'name':'David'})\
        #           .saveAndExit()\
        #           .run()\
        #           .assert_rendered_sql("hello David!")\
        #           .assert_all_input_was_read()

