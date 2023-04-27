import os
from pathlib import Path
from sqltask.test.utils.app_runner import ApplicationRunner

import yaml


class TemplatesAppRunner(ApplicationRunner):
    def __init__(self, capsys=None):
        super().__init__()
        self.capsys = capsys

    @property
    def test_template_path(self):
        return str(Path(self.templates_path).parent / "test_templates")

    def make_test_dir(self):
        self.fs.create_dir(self.test_template_path)
        return self

    def with_test_context_values(self, data):
        self.context_values = None
        filepath = self._app_project.library().test_context_values()
        self._create_file(filepath, yaml.dump(data))
        return self

    def add_test(self, template_path, template_vars, content, template_vars_list=None):
        dirname = os.path.dirname(template_path)
        name = os.path.basename(template_path)
        path = os.path.join(self.test_template_path, dirname)
        test_data_object = self._get_template_vars(template_vars, template_vars_list)
        test_content = "-- " + str(test_data_object) + "\n" + content
        self._create_file(os.path.join(path, name), test_content)
        return self

    def _get_template_vars(self, template_vars, template_vars_list):
        if template_vars is not None:
            return template_vars
        else:
            return template_vars_list

    def run_test_render_sql(self):
        self._run([".", "test-sql", "--tests=expected-sql"])
        return self

    def run_test_with_db(self):
        self._run([".", "test-sql", "--tests=run-on-db"])
        return self

    def run_test_all(self):
        self._run([".", "test-sql", "--tests=all"])
        return self

    def run_one_test(self, test_name):
        self._run([".", "test-sql", "--test-name=" + test_name])
        return self

    def run_assertion_test(self, assertion_type):
        self._run([".", "test-sql", "--assertion=" + assertion_type])
        return self

    def run(self, app=None):
        self._run([".", "test-sql"], self.build_app())
        return self

    def test_sql(self):
        self._run([".", "test-sql"])
        return self

    def assert_message_printed(self, expected):
        captured = self.capsys.readouterr()
        assert expected in captured.out
        return self

    def generates_no_test(self):
        assert not os.path.exists(self.app.last_command_run.generated_test_filepath())

    def assert_generated_tests(self, expected_source):
        testfile = open(self.app.last_command_run.generated_test_filepath())
        test_content = testfile.read()
        testfile.close()
        assert expected_source.to_string() == test_content
