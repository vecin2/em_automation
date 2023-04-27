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
        if not app:
            app = CommandLineSQLTaskApp.build_app(self.project_home_path, None)
        app.run()

