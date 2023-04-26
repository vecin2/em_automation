import re
from pathlib import Path

import pyperclip

from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner


class CreateSQLTaskAppRunner(PrintSQLToConsoleAppRunner):
    def __init__(self):
        super().__init__()
        self.module_name = ""
        self.task_name = ""

    def create_sql(self, sqltask_path=None, template=None):
        params = [".", "create-sql"]

        if sqltask_path:
            sqltask_path = str(self._project.emroot / sqltask_path)
            params.append(sqltask_path)
        if template:
            params.extend(["--template", template])
        self._run(params)
        return self

    def with_sql_module(self, module_name):
        self.user_inputs(module_name)
        self.module_name = module_name
        return self

    def and_task_name(self, task_name):
        self.user_inputs(task_name)
        self.task_name = task_name
        return self

    def exists_table_data(self, release_name=None, expected_content=""):
        self.exists(
            self.get_task_folder(release_name) / "tableData.sql", expected_content
        )
        return self

    def exists_update_seq(self, release_name=None, update_seq=None):
        if not update_seq:
            expected_content = "PROJECT \$Revision: \d+ \$"  # regex
        else:
            expected_content = f"PROJECT $Revision: {update_seq} $"

        self.exists(
            self.get_task_folder(release_name) / "update.sequence", expected_content
        )
        return self

    def get_task_folder(self, release_name):
        return Path(
            f"modules/{self.module_name}/sqlScripts/oracle/updates/{release_name}/{self.task_name}"
        )

    def exists(self, filepath, expected_content):
        filepath = str(self._project.emroot / filepath)
        with open(filepath) as f:
            text = f.read()
        match = re.search(expected_content, text)
        if not match:
            assert expected_content == text, "do not match"
        else:
            assert match.group()
        return self

    def assert_path_copied_to_sys_clipboard(self,release_name):
        assert str(release_name) in pyperclip.paste()
        return self
