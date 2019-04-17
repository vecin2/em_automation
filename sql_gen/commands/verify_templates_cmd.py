import os
import sys
import re
import ast
from io import StringIO

from jinja2 import Template
import pytest

from sql_gen.commands import PrintSQLToConsoleCommand
from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv

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

