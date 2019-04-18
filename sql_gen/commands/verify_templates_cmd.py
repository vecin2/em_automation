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

class SourceTestBuilder(object):
    def __init__(self):
        self.content=""

    def add_expected_sql_test(self,**kwargs):
        test_content="""
def test_rendering_{{template_name}}_matches_expected_sql():
    expected={{expected}}
    actual={{actual}}
    assert expected == actual
"""
        kwargs["expected"]=self.convert_to_src(kwargs["expected"])
        kwargs["actual"]=self.convert_to_src(kwargs["actual"])
        template = Template(test_content)
        if self.content:
            self.content +="\n\n"
        current_content = template.render(kwargs)
        self.content +=current_content
        return current_content

    def convert_to_src(self,string):
        lines = string.splitlines()
        result="("
        for i,line in enumerate(lines):
            result += "\""+line
            if i != len(lines)-1:
                result +="\\n\""+"\n\t"
            else:
                result +="\""
        result +=")"
        return result


class TestFileParser(object):
    def parse_values(self,string):
        first_line = self._first_line(string)
        str_values = self._remove_prefix("--",first_line)
        return ast.literal_eval(str_values)

    def _first_line(self,string):
        return string.split("\n")[0]

    def _extract_template_filename(self,filename):
        return self._remove_prefix("test_",filename)

    def _remove_prefix(self,prefix, string):
        if string.startswith(prefix):
            return string[len(prefix):].strip()
        return string

    def parse_expected_sql(self,string):
       return self._remove_first_line(string)

    def _remove_first_line(self,string):
        return re.sub(r'^[^\n]*\n', '', string)

class TestTemplatesCommandDisplayer(object):
    def test_folder_does_no_exist(self,directory):
        print("Test folder '"+directory+"' does not exist.")

class TestTemplatesCommand(object):
    def __init__(self,
                 apprunner = None,
                 env_vars = None,
                 pytest=pytest,
                 source_builder= None):
        self.apprunner= apprunner
        self.env_vars=env_vars
        self.app_project = AppProject(env_vars=self.env_vars)
        self.pytest =pytest
        self.displayer = TestTemplatesCommandDisplayer()
        if not source_builder:
            source_builder = SourceTestBuilder()
        self.source_builder =source_builder
        self.parser = TestFileParser()

    def generated_test_filepath(self):
            return self._tmp_folder()+"/test_all_templates.py"

    def _tmp_folder(self):
        tmp_testdir=self.app_project.paths["test_templates_tmp"].path
        if not os.path.exists(tmp_testdir):
            os.makedirs(tmp_testdir)
        return tmp_testdir

    @property
    def all_tests_path(self):
        return self.app_project.paths["test_templates"].path

    def run(self):
        if not os.path.exists(self.all_tests_path):
            self.displayer.test_folder_does_no_exist(self.all_tests_path)
            return
        self._create_test_file(self._generate_all_tests())
        self.pytest.main(['-x','-v',self._tmp_folder()])

    def _generate_all_tests(self):
        testpath = self.all_tests_path
        for filename in os.listdir(testpath):
            filepath = os.path.join(testpath,filename)
            if self._is_valid_test_file(filepath):
                self._generate_test(filepath)
        return self.source_builder.content

    def _is_valid_test_file(self,filepath):
            filename = os.path.basename(filepath)
            extension = os.path.splitext(filename)[1]
            return os.path.isfile(filepath)\
                    and extension==".sql"\
                    and self._matches_template(filename)

    def _matches_template(self, test_file):
        path = EMTemplatesEnv().get_templates_path(self.env_vars)
        for template_file in os.listdir(path):
            if template_file == self._extract_template_filename(test_file):
                return True

        return False

    def _generate_test(self,filepath):
        filename =os.path.basename(filepath) 
        test_file = open(filepath,"r+")
        expected = self.parser.parse_expected_sql(test_file.read())
        #apprunner = AppRunner(env_vars=self.env_vars,initial_context=self.initial_context)
        actual =self.apprunner._run_test(filepath)
        template_file = self._extract_template_filename(filename)
        template_name = os.path.splitext(template_file)[0]
        self.source_builder.add_expected_sql_test(template_name=template_name,
                                          expected=expected,
                                          actual=actual)

    def _extract_template_filename(self,filename):
        return self._remove_prefix("test_",filename)

    def _remove_prefix(self,prefix, string):
        if string.startswith(prefix):
            return string[len(prefix):].strip()
        return string

    def _create_test_file(self,source):
        if source:
            test_file = open(self.generated_test_filepath(),"w")
            test_file.write(source)
            test_file.close()


class AppRunner(PrintSQLToConsoleCommand):
    def __init__(self,env_vars=os.environ, initial_context=None):
        self.parser =TestFileParser()
        emprj_path= AppProject.home_path(env_vars)
        templates_path=EMTemplatesEnv().extract_templates_path(env_vars)
        super().__init__(initial_context=initial_context,
                         emprj_path=emprj_path,
                         templates_path =templates_path)

    def _run_test(self,filepath):
            sys.stdin = StringIO(self._user_input_to_str(filepath))
            self.run()
            test_file = open(filepath,"r+")
            expected = self.parser.parse_expected_sql(test_file.read())
            return self.sql_printed()

    def _user_input_to_str(self,filepath):
        filename =os.path.basename(filepath) 
        inputs=[]
        inputs.append(self.parser._extract_template_filename(filename))
        with open(filepath) as f:
             temp_values = self.parser.parse_values(f.read())
        for key in temp_values:
            inputs.append(temp_values[key])
        inputs.append("x")
        return "\n".join([input for input in inputs])

        #app_runner = PrintSQLToConsoleAppRunner()
        #app_runner.using_templates_under("/templates")\
        #           .select_template('1. greeting.sql',{'name':'David'})\
        #           .saveAndExit()\
        #           .run()\
        #           .assert_rendered_sql("hello David!")\
        #           .assert_all_input_was_read()

