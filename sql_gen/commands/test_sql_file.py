import ast
import os
import re

import sqlparse

import sql_gen


class TestSQLFile(object):
    # because the name starts with 'Test' pytest tries to run it
    __test__ = False  # stop pytest from running this as a test

    def __init__(self, filepath):
        self.filepath = filepath
        self.parser = TestFileParser()
        test_file = open(self.filepath, "r+")
        self.content = test_file.read()
        test_file.close()

    def filename(self):
        return os.path.basename(self.filepath)

    def template_filename(self):
        return self.parser._extract_template_filename(self.filename())

    def template_path(self):
        test_template_path = self.filepath.split("test_templates" + os.sep)[1]
        template_path = test_template_path.replace(
            self.filename(), self.template_filename()
        )
        return template_path

    def template_name(self):
        return os.path.splitext(self.template_filename())[0]

    def expected_sql(self):
        return self.parser.parse_expected_sql(self.content)

    def values(self):
        return self.parser.parse_values(self.content)


class TestFileParser(object):
    def parse_values(self, string):
        first_line = self._first_line(string)
        str_values = self._remove_prefix("--", first_line)
        try:
            return ast.literal_eval(str_values)
        except Exception as excinfo:
            sql_gen.logger.debug(
                "Unable to parse values from first line; '" + first_line + "'"
            )
            return {}

    def _first_line(self, string):
        return string.split("\n")[0]

    def _extract_template_filename(self, filename):
        return self._remove_prefix("test_", filename)

    def _remove_prefix(self, prefix, string):
        if string.startswith(prefix):
            return string[len(prefix) :].strip()
        return string

    def parse_expected_sql(self, string):
        return sqlparse.format(string, strip_comments=True).strip()
        # return self._remove_first_line(string)

    def _remove_first_line(self, string):
        return re.sub(r"^[^\n]*\n", "", string)
