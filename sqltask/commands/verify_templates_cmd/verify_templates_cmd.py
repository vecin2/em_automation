import os
import shutil
import sys
import time
from io import StringIO
from pathlib import Path

import pytest
from jinja2 import Template

from sqltask.app_project import AppProject
from sqltask.commands.verify_templates_cmd.test_sql_file import (
    TestFileParser, TestSQLFile)
from sqltask.docugen.env_builder import FileSystemLoader
from sqltask.shell.shell_factory import (InteractiveSQLTemplateRunnerBuilder,
                                         PrintSQLToConsoleDisplayer)
from sqltask.sqltask_jinja.context import ContextBuilder


class SourceCode(object):
    def __init__(self, imports=[], content=""):
        self.imports = []
        self.add_imports(imports)
        self.content = content

    def add(self, source_code):
        self.add_imports(source_code.imports)

        if self.content:
            self.content += "\n"
        self.content += source_code.content

        return self

    def add_imports(self, imports):
        for import_stmt in imports:
            if import_stmt not in self.imports:
                self.imports.append(import_stmt)

    def to_string(self):
        content = ""

        if self.imports:
            content = "\n".join(self.imports)
            content += "\n\n"

        content += self.content

        return content


class PythonModuleTemplate(object):
    def convert_to_src(self, string):
        lines = string.splitlines()
        result = "("

        for i, line in enumerate(lines):
            result += '"' + self.scape(line)

            if i != len(lines) - 1:
                result += '\\n"' + "\n\t"
            else:
                result += '"'
        result += ")"

        return result

    def scape(self, string):
        return string.replace('"', '\\"')


class RunOnDBTestTemplate(PythonModuleTemplate):
    def render(self, **kwargs):
        imports = [
            "from sqltask.app_project import AppProject",
            "from sqltask.database.sqlparser import SQLParser, RelativeIdLoader",
            "import sqlparse",
        ]
        test_content = """
def test_{{template_name}}_runs_succesfully():
    query={{query}}
    emprj_path={{emprj_path}}
    app_project = AppProject(emprj_path=emprj_path)
    db = app_project.get_schema("{{db_schema}}")
    sqlparser =SQLParser(RelativeIdLoader())
    try:
       #app_project.addb.execute(query,sqlparser=sqlparser)
       db.execute(query,sqlparser=sqlparser)
 
    except:
        #if we do not close the connection we get locks issues when test are failing
        #app_project.addb._conn().close()
        db._conn().close()
        raise

"""
        kwargs["query"] = self.convert_to_src(kwargs["query"])
        # repr escape back slashes in windows paths
        kwargs["emprj_path"] = repr(kwargs["emprj_path"])
        template = Template(test_content)
        test_content = template.render(**kwargs)
        source_code = SourceCode(imports=imports, content=test_content)
        return source_code


class UnableToFindTemplateTestTemplate(PythonModuleTemplate):
    def render(self, **kwargs):
        test_content = """
def test_{{template_name}}_runs_succesfully():
"""
        template = Template(test_content)
        test_content = template.render(**kwargs)
        source_code = SourceCode(imports=[], content=test_content)
        return source_code


class ExpectedSQLTestTemplate(PythonModuleTemplate):
    def render(self, **kwargs):
        imports = ["from sqltask.database.sqlparser import SQLParser"]
        test_content = """
def test_rendering_{{template_name}}_matches_expected_sql():
    expected={{expected}}
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    {% if actual %}
    actual={{actual}}
    actual =sqlparser.parse_assertable_statements(actual)
    {% else %}
    raise LookupError("Unable to find matching template. Make sure the test file matches the template's name and location")
    {% endif %}
    assert expected == actual
"""
        kwargs["expected"] = self.convert_to_src(kwargs["expected"])
        if kwargs["actual"]:
            kwargs["actual"] = self.convert_to_src(kwargs["actual"])
        template = Template(test_content)
        test_content = template.render(kwargs)
        return SourceCode(imports=imports, content=test_content)


class TestGenerator(object):
    def __init__(self, emprj_path=None, test_type=None, apprunner=None):
        self.content = SourceCode()
        self.apprunner = apprunner
        self.emprj_path = emprj_path
        self.test_type = test_type

    def build(self, testfile, emprj_path=None):
        return self.run_builders(self.get_builders(testfile), testfile)

    def run_builders(self, builders, testfile):
        for builder in builders:
            builder.apprunner = self.apprunner
            self.content.add(builder.build(testfile))

    def get_builders(self, testfile):
        result = []
        testfile_lines = testfile.content.splitlines()
        if not testfile.filepath.endswith("sql") or (
            len(testfile_lines) > 1 and testfile_lines[1] == "--skip.run-on-db"
        ):
            print("Generating expected-sql test for " + testfile.template_name())
            result.append(ExpectedSQLTestBuilder(self.emprj_path))
        elif self.test_type == "all":
            print("Generating expected-sql test for " + testfile.template_name())
            result.append(ExpectedSQLTestBuilder(self.emprj_path))
            print("Generating run-on-db test for " + testfile.template_name())
            result.append(RunOnDBTestBuilder(self.emprj_path, self.apprunner))
        elif self.test_type == "expected-sql":
            print("Generating expected-sql test for " + testfile.template_name())
            result.append(ExpectedSQLTestBuilder(self.emprj_path))
        elif self.test_type == "run-on-db":
            print("Generating run-on-db test for " + testfile.template_name())
            result.append(RunOnDBTestBuilder(self.emprj_path, self.apprunner))
        return result


class ExpectedSQLTestBuilder(object):
    def __init__(self, emprj_path):
        self.emprj_path = emprj_path

    def build(self, testfile, emprj_path=None):
        expected = testfile.expected_sql()
        actual = self.apprunner.run_test(testfile)
        template_name = testfile.template_name()
        return ExpectedSQLTestTemplate().render(
            template_name=template_name, expected=expected, actual=actual
        )


class RunOnDBTestBuilder(object):
    def __init__(self, emprj_path, apprunner):
        self.emprj_path = str(emprj_path)
        self.apprunner = apprunner

    def build(self, testfile, emprj_path=None):

        return RunOnDBTestTemplate().render(
            db_schema=testfile.top_folder(),
            template_name=testfile.template_name(),
            query=testfile.expected_sql(),
            emprj_path=str(self.emprj_path),
        )


class TestTemplatesCommandDisplayer(object):
    def test_folder_does_no_exist(self, directory):
        print("Test folder '" + directory + "' does not exist.")


class TestLoader(object):
    def __init__(self, testpath, templates_path):
        self.testpath = testpath
        self.templates_path = templates_path
        self.parser = TestFileParser()

    def load_tests(self):
        result = []
        for filepath in self._list_all_test_files():
            result.append(TestSQLFile(filepath))
        return result

    def load_test(self, test_name):
        testpath = self.testpath
        for filepath in self._list_all_test_files():
            filename = os.path.basename(filepath)
            if test_name == filename:
                return TestSQLFile(filepath)
        return None

    def _list_all_test_files(self):
        result = []
        testpath = self.testpath
        filesystemloader = FileSystemLoader(testpath)
        test_files = filesystemloader.list_templates()
        for filename in test_files:
            filepath = os.path.join(testpath, filename)
            if self._is_valid_test_file(filepath):
                result.append(filepath)
        return sorted(result)  # return tests in alfabetical order

    def _is_valid_test_file(self, filepath):
        filename = os.path.basename(filepath)
        extension = os.path.splitext(filename)[1]
        return os.path.isfile(filepath) and filename.startswith("test_")
        # and self._matches_template(filename)

    def _matches_template(self, test_file):
        for template_file in os.listdir(self.templates_path):
            if template_file == self.parser._extract_template_filename(test_file):
                return True
        return False


class TestTemplatesCommand(object):
    def __init__(
        self,
        pytest=pytest,
        templates_path=None,
        emprj_path=None,
        context_builder=None,
        verbose_mode="-v",
        test_group="all",
        test_name=None,
        reuse_tests=False,
        args=None,
        project=None,
    ):
        self.reuse_tests = reuse_tests
        self.emprj_path = str(emprj_path)
        self.app_project = project
        self.context_builder = self._init_context_builder(
            self.app_project, context_builder
        )
        self.apprunner = FileAppRunner(
            templates_path, emprj_path, self.context_builder, project=project
        )
        self._test_generator = None
        self.pytest = pytest
        self.displayer = TestTemplatesCommandDisplayer()
        self.templates_path = templates_path
        self.test_loader = TestLoader(self.all_tests_path, templates_path)
        self.verbose_mode = verbose_mode
        self.test_group = test_group
        self.test_name = test_name

    def _init_context_builder(self, app_project, context_builder):
        if not context_builder:
            context_builder = ContextBuilder(app_project)
        test_context_values_filepath = self.app_project.library().test_context_values()
        if os.path.exists(test_context_values_filepath):
            context_builder.context_values_filepath = test_context_values_filepath
        return context_builder

    @property
    def test_generator(self):
        if not self._test_generator:
            self._test_generator = TestGenerator(
                self.emprj_path, self.test_group, self.apprunner
            )
        return self._test_generator

    def generated_test_filepath(self):
        return self._tmp_folder() + "/test_expected_sql.py"

    @property
    def tmp_testdir(self):
        return str(Path(self.all_tests_path) / ".tmp")
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
        return str(Path(self.templates_path).parent / "test_templates")

    def run(self):
        start_time = time.time()
        if not os.path.exists(self.all_tests_path):
            self.displayer.test_folder_does_no_exist(self.all_tests_path)
            return
        print(f"Test Templates loaded from '{self.all_tests_path}'")
        if self.verbose_mode == "-q":
            original_stdout = sys.stdout
            stdout_file = open(os.devnull, "w")
            sys.stdout = stdout_file

        if not self.reuse_tests:
            self._recreate_tmp_folder()
            self._create_test_file(self._generate_all_tests())
        if self.verbose_mode == "-q":
            sys.stdout = original_stdout
        output = self.pytest.main([self.verbose_mode, self._tmp_folder()])
        print("--- Run in %s seconds ---" % (time.time() - start_time))

    def _create_test_file(self, source):
        if source.to_string():
            test_file = open(self.generated_test_filepath(), "w")
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


class FillTemplateAppRunner:
    def __init__(self):
        self.original_stdin = sys.stdin
        self.inputs = []

    def saveAndExit(self):
        self.user_inputs("exit")
        return self

    def select_tps_template(self, template_name, values={}):
        self.select_template("tenant_properties_service/" + template_name, values)
        return self

    def select_template(self, template_name, values={}):
        self.user_inputs(template_name)
        if isinstance(values, dict):
            value_list = list(values.values())
        else:
            value_list = values
        for value in value_list:
            self.user_inputs(value)
        return self

    def edit_template(self, template_name):
        self.user_inputs(f"{template_name} --edit")
        return self

    def confirm(self):
        self.user_inputs("\n")
        return self

    def user_inputs(self, user_input):
        self.inputs.append(user_input)
        return self

    def clear_inputs(self):
        self.inputs.clear()

    def run(self):
        str_inputs = "\n".join([input for input in self.inputs])
        sys.stdin = StringIO(str_inputs)
        self._run()

    def teardown(self):
        sys.stdin = self.original_stdin


class FileAppRunner(FillTemplateAppRunner):
    def __init__(self, templates_path, emprj_path, context_builder=None, project=None):
        super().__init__()
        self.project_root = emprj_path
        self.templates_path = templates_path
        self.console_printer = PrintSQLToConsoleDisplayer()
        self.context_builder = context_builder
        self.project = project

    def run_test(self, testfile):
        self.clear_inputs()
        self.select_template(testfile.template_path(), testfile.values())
        self.saveAndExit()
        self.run()
        result = self.console_printer.rendered_sql
        self.console_printer.rendered_sql = ""  # otherwise it keeps appending template
        return result

    def _run(self):
        builder = InteractiveSQLTemplateRunnerBuilder.default(self.project)
        builder.sql_runner = None
        shell = builder.build()
        self.console_printer = builder.displayer
        shell.run()
        self.teardown()
