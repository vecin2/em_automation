import os
import sys
import re
import ast
import shutil
import sqlparse
from io import StringIO

from jinja2 import Template
import pytest

import sql_gen
from sql_gen.commands import PrintSQLToConsoleCommand
from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv

class SourceCode(object):
    def __init__(self,imports=[],content=""):
        self.imports=[]
        self.add_imports(imports)
        self.content=content

    def add(self,source_code):
        self.add_imports(source_code.imports)
        if self.content:
            self.content+="\n"
        self.content+=source_code.content
        return self
    def add_imports(self,imports):
        for import_stmt in imports:
            if import_stmt not in self.imports:
                self.imports.append(import_stmt)

    def to_string(self):
        content =""
        if self.imports:
            content = "\n".join(self.imports)
            content +="\n\n"

        content += self.content
        return content

class PythonModuleTemplate(object):
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

class RunOnDBTestTemplate(PythonModuleTemplate):
    def render(self,**kwargs):
        imports=["from sql_gen.app_project import AppProject",
                "from sql_gen.database.sqlparser import SQLParser, RelativeIdLoader",
                "import sqlparse"]
        test_content="""
def test_{{template_name}}_runs_succesfully():
    query={{query}}
    emprj_path={{emprj_path}}
    app_project = AppProject(emprj_path=emprj_path)
    sqlparser =SQLParser(RelativeIdLoader())
    app_project.addb.execute(query,sqlparser=sqlparser)
"""
        kwargs["query"]=self.convert_to_src(kwargs["query"])
        kwargs["emprj_path"]=self.convert_to_src(kwargs["emprj_path"])
        template = Template(test_content)
        test_content= template.render(**kwargs)
        source_code = SourceCode(imports= imports, content=test_content)
        return source_code

class ExpectedSQLTestTemplate(PythonModuleTemplate):
    def render(self,**kwargs):
        imports=["from sql_gen.database.sqlparser import SQLParser"]
        test_content="""
def test_rendering_{{template_name}}_matches_expected_sql():
    expected={{expected}}
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    actual={{actual}}
    actual =sqlparser.parse_assertable_statements(actual)
    assert expected == actual
"""
        kwargs["expected"]=self.convert_to_src(kwargs["expected"])
        kwargs["actual"]=self.convert_to_src(kwargs["actual"])
        template = Template(test_content)
        test_content = template.render(kwargs)
        return  SourceCode(imports= imports, content=test_content)

class TestGenerator(object):
    def __init__(self,emprj_path=None,test_type=None,apprunner=None):
        self.content=SourceCode()
        self.apprunner =apprunner
        self.emprj_path=emprj_path
        self.test_type= test_type

    def build(self,testfile,emprj_path=None):
        return self.run_builders(self.get_builders(),testfile)

    def run_builders(self,builders,testfile):
        for builder in builders:
            builder.apprunner = self.apprunner
            self.content.add(builder.build(testfile))

    def get_builders(self):
        result =[]
        if self.test_type == "all":
                result.append(ExpectedSQLTestBuilder(self.emprj_path))
                result.append(RunOnDBTestBuilder(self.emprj_path,
                                                 self.apprunner))
        elif self.test_type == "expected-sql":
                result.append(ExpectedSQLTestBuilder(self.emprj_path))
        elif self.test_type == "run-on-db":
                result.append(RunOnDBTestBuilder(self.emprj_path,
                                                 self.apprunner))
        return result

class ExpectedSQLTestBuilder(object):
    def __init__(self,emprj_path):
        self.emprj_path=emprj_path

    def build(self,testfile,emprj_path=None):
        expected = testfile.expected_sql()
        app_project = AppProject(emprj_path=self.emprj_path)
        actual =self.apprunner.run_test(testfile)
        template_name = testfile.template_name()
        return ExpectedSQLTestTemplate().render(
                                  template_name=template_name,
                                  expected=expected,
                                  actual=actual)


class RunOnDBTestBuilder(object):
    def __init__(self,emprj_path,apprunner):
        self.emprj_path=emprj_path
        self.apprunner =apprunner

    def build(self,testfile,emprj_path=None):
        actual =self.apprunner.run_test(testfile)
        return RunOnDBTestTemplate().render(
                              template_name=testfile.template_name(),
                              query=testfile.expected_sql(),
                              emprj_path=self.emprj_path)


class TestTemplatesCommandDisplayer(object):
    def test_folder_does_no_exist(self,directory):
        print("Test folder '"+directory+"' does not exist.")

class TestLoader(object):
    def __init__(self,testpath,templates_path):
        self.testpath=testpath
        self.templates_path=templates_path
        self.parser = TestFileParser()

    def load_tests(self):
        result =[]
        for filepath in self._list_all_test_files():
                result.append(TestSQLFile(filepath))
        return result

    def load_test(self,test_name):
        testpath = self.testpath
        for filepath in self._list_all_test_files():
            filename= os.path.basename(filepath)
            if test_name == filename:
                    return TestSQLFile(filepath)
        return None

    def _list_all_test_files(self):
        result =[]
        testpath = self.testpath
        for filename in os.listdir(testpath):
            filepath = os.path.join(testpath,filename)
            if self._is_valid_test_file(filepath):
                result.append(filepath)
        return result

    def _is_valid_test_file(self,filepath):
            filename = os.path.basename(filepath)
            extension = os.path.splitext(filename)[1]
            return os.path.isfile(filepath)\
                    and extension==".sql"\
                    and self._matches_template(filename)

    def _matches_template(self, test_file):
        for template_file in os.listdir(self.templates_path):
            if template_file == self.parser._extract_template_filename(test_file):
                return True
        return False


class TestSQLFile(object):
    def __init__(self,filepath):
        self.filepath = filepath
        self.parser = TestFileParser()
        test_file = open(self.filepath,"r+")
        self.content =test_file.read()
        test_file.close()

    def filename(self):
        return os.path.basename(self.filepath) 

    def template_filename(self):
        return self.parser._extract_template_filename(self.filename())

    def template_name(self):
        return os.path.splitext(self.template_filename())[0]

    def expected_sql(self):
        return self.parser.parse_expected_sql(self.content)

    def values(self):
        return self.parser.parse_values(self.content)


class TestFileParser(object):
    def parse_values(self,string):
        first_line = self._first_line(string)
        str_values = self._remove_prefix("--",first_line)
        try:
            return ast.literal_eval(str_values)
        except Exception as excinfo:
            sql_gen.logger.debug("Unable to parse values from first line; '"+first_line+"'")
            return {}

    def _first_line(self,string):
        return string.split("\n")[0]

    def _extract_template_filename(self,filename):
        return self._remove_prefix("test_",filename)

    def _remove_prefix(self,prefix, string):
        if string.startswith(prefix):
            return string[len(prefix):].strip()
        return string

    def parse_expected_sql(self,string):
       return sqlparse.format(string,strip_comments=True).strip()
       #return self._remove_first_line(string)

    def _remove_first_line(self,string):
        return re.sub(r'^[^\n]*\n', '', string)

class TestTemplatesCommand(object):
    def __init__(self,
                 pytest=pytest,
                 templates_path=None,
                 emprj_path=None,
                 initial_context=None,
                 verbose_mode="-v",
                 test_group="all",
                 test_name=None,
                 reuse_tests=False):
        self.reuse_tests=reuse_tests
        self.emprj_path = emprj_path
        self.initial_context = initial_context
        self.apprunner = FileAppRunner(templates_path,
                                  emprj_path,
                                  initial_context)
        self.app_project = AppProject(emprj_path=emprj_path)
        self._test_generator=None
        self.pytest =pytest
        self.displayer = TestTemplatesCommandDisplayer()
        self.test_loader = TestLoader(self.all_tests_path,templates_path)
        self.verbose_mode=verbose_mode
        self.test_group=test_group
        self.test_name =test_name

    @property
    def test_generator(self):
        if not self._test_generator:
            self._test_generator =  TestGenerator(self.emprj_path,
                                                  self.test_group,
                                                  self.apprunner)
        return self._test_generator


    def generated_test_filepath(self):
            return self._tmp_folder()+"/test_expected_sql.py"

    @property
    def tmp_testdir(self):
        return self.app_project.paths["test_templates_tmp"].path

    def _tmp_folder(self):
        if not os.path.exists(self.tmp_testdir):
            os.makedirs(self.tmp_testdir)
        return self.tmp_testdir

    def _recreate_tmp_folder(self):
        if os.path.exists(self.tmp_testdir):
            shutil.rmtree(self.tmp_testdir)
        self._tmp_folder()

    @property
    def all_tests_path(self):
        return self.app_project.paths["test_templates"].path

    def run(self):
        if not os.path.exists(self.all_tests_path):
            self.displayer.test_folder_does_no_exist(self.all_tests_path)
            return
        if self.verbose_mode != "-vv":
            original_stdout = sys.stdout
            stdout_file =self._tmp_folder()+"/run_test.log"
            sys.stdout = open(stdout_file,"w")
        if not self.reuse_tests:
            self._recreate_tmp_folder()
            self._create_test_file(self._generate_all_tests())
        if self.verbose_mode != "-vv":
            sys.stdout = original_stdout
        output =self.pytest.main(['-x',self.verbose_mode,self._tmp_folder()])

    def _create_test_file(self,source):
        if source.to_string():
            test_file = open(self.generated_test_filepath(),"w")
            test_file.write(source.to_string())
            test_file.close()

    def _generate_all_tests(self):
        for testfile in self._get_tests_to_run():
            self.test_generator.build(testfile)
        return self.test_generator.content

    def _get_tests_to_run(self):
        if self.test_name:
            testfile = self.test_loader.load_test(self.test_name)
            if testfile:
                return [testfile]
            return []
        return self.test_loader.load_tests()




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

    def clear_inputs(self):
        self.inputs.clear()

    def run(self):
        str_inputs ="\n".join([input for input in self.inputs])
        sys.stdin = StringIO(str_inputs)
        self._run()

    def teardown(self):
        sys.stdin = self.original_stdin

class FileAppRunner(FillTemplateAppRunner):
    def __init__(self,templates_path,emprj_path, initial_context=None):
        super().__init__()
        self.print_sql_cmd = PrintSQLToConsoleCommand(
                            initial_context=initial_context,
                            emprj_path=emprj_path,
                            templates_path =templates_path)

    def run_test(self,testfile):
        self.clear_inputs()
        self.select_template(testfile.template_filename(),
                             testfile.values())
        self.saveAndExit()
        self.run()
        return self.print_sql_cmd.sql_printed()

    def _run(self):
        self.print_sql_cmd.run()
        self.teardown()

