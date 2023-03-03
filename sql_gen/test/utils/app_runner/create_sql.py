import re

from sql_gen.test.utils.app_runner import AppRunner


class FakeClipboard:
    def copy(self, text):
        self.text = text

    def paste(self):
        return self.text


class CreateSQLTaskAppRunner(AppRunner):
    def __init__(self, fs=None):
        super().__init__(fs=fs)
        self.rev_no = "0"
        self.taskpath = ""
        self.clipboard = FakeClipboard()

    def create_sql(self, sqltask_path=None, template=None):
        self.taskpath = sqltask_path
        params = [".", "create-sql"]

        if sqltask_path:
            params.append(sqltask_path)
        if template:
            params.extend(["--template", template])
        self._run(params, self.build_app())
        return self

    def exists(self, filepath, expected_content):
        with open(filepath) as f:
            s = f.read()
        assert expected_content == s
        return self

    def exists_regex(self, filepath, expected_content):
        with open(filepath) as f:
            text = f.read()
        match = re.search(expected_content, text)
        assert match.group()
        return self

    def assert_path_copied_to_sys_clipboard(self):
        assert self.taskpath == self.clipboard.paste()
        return self
