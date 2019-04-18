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
                 pytest=pytest,
                 templates_path=None,
                 emprj_path=None,
                 initial_context=None):
        self.templates_path = templates_path
        self.emprj_path = emprj_path
        self.initial_context = initial_context
        self.apprunner = FileAppRunner(templates_path, 
                                  emprj_path,
                                  initial_context)
        self.app_project = AppProject(emprj_path=emprj_path)
        self.pytest =pytest
        self.displayer = TestTemplatesCommandDisplayer()
        self.source_builder = SourceTestBuilder()
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
        for template_file in os.listdir(self.templates_path):
            if template_file == self._extract_template_filename(test_file):
                return True

        return False

    def _generate_test(self,filepath):
        filename =os.path.basename(filepath) 
        test_file = open(filepath,"r+")
        expected = self.parser.parse_expected_sql(test_file.read())
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


class FillTemplateAppRunner():
    def __init__(self):
        self.original_stdin = sys.stdin
        self.inputs=[]

    def saveAndExit(self):
        self.user_inputs("x")
        return self

    def select_template(self, template_option,values):
        self.user_inputs(template_option)
        for value in values.values():
            self.user_inputs(value)
        return self

    def user_inputs(self, user_input):
        self.inputs.append(user_input)
        return self

    def teardown(self):
        sys.stdin = self.original_stdin

class FileAppRunner(FillTemplateAppRunner):
    def __init__(self,templates_path,emprj_path, initial_context=None):
        super().__init__()
        self.parser =TestFileParser()
        self.print_sql_cmd = PrintSQLToConsoleCommand(
                            initial_context=initial_context,
                            emprj_path=emprj_path,
                            templates_path =templates_path)

    def _run_test(self,filepath):
        sys.stdin = StringIO(self._user_input_to_str(filepath))
        self.run()
        test_file = open(filepath,"r+")
        expected = self.parser.parse_expected_sql(test_file.read())
        return self.print_sql_cmd.sql_printed()

    def run(self):
        self.print_sql_cmd.run()
        self.inputs.clear()
        self.teardown()

    def _user_input_to_str(self,filepath):
        filename =os.path.basename(filepath) 
        with open(filepath) as f:
             template_name =self.parser._extract_template_filename(filename)
             temp_values = self.parser.parse_values(f.read())
             self.select_template(template_name,temp_values)
        self.saveAndExit()
        inputs = self.inputs
        return "\n".join([input for input in inputs])
