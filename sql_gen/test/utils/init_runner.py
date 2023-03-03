import os
import sys
from sys import path

from ccdev.command_line_app import CommandLineSQLTaskApp


class InitAppRunner(object):
    def __init__(self):
        self.project_home_path = path

    def with_emproject_home(self, path):
        self.project_home_path = path

    def init(self, app=None):
        self._run([".", "init"], app=app)
        return self

    def _run(self, args, app=None):
        sys.argv = args
        # sys.stdin = StringIO(self._user_input_to_str())
        if not app:
            app = CommandLineSQLTaskApp.build_app(os.getcwd(), os.environ)
        app.run()

    # def _user_input_to_str(self):
    #     return "\n".join([input for input in self.inputs])
