import os
import sys
from io import StringIO

import pytest

from sqltask.commands.verify_templates_cmd import FillTemplateAppRunner
from sqltask.main.default_app_config import DefaultAppContainer


class FakeLogger(object):
    def debug(self):
        """"""

    def info(self):
        """"""

    def error(self):
        """"""


class ApplicationRunner(FillTemplateAppRunner):
    def __init__(self):
        super().__init__()
        self._project = None

    def _run(self, args):
        sys.argv = args
        sys.stdin = StringIO(self._user_input_to_str())
        self.build_app().run()

    def _user_input_to_str(self):
        result = "\n".join([input for input in self.inputs])
        self.inputs.clear()  # so if runs again it doe not repit inputs
        return result

    def build_app(self):
        self.app = DefaultAppContainer().resolve(self._project.emroot)
        return self.app

    def with_project(self, project):
        self._project = project
        return self

    def assert_all_input_was_read(self):
        with pytest.raises(EOFError) as excinfo:
            test = input()
            print("Unexpected input: " + test)
        assert "EOF" in str(excinfo.value)
        return self
