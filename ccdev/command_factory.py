import os
from pathlib import Path

import pytest

from devtask.commands import ExtendProcessCommand
from sqltask.app_project import AppProject
from sqltask.commands import (CreateSQLTaskCommand, InitCommand,
                              PrintSQLToConsoleCommand, RunSQLCommand,
                              TestTemplatesCommand)
from sqltask.sqltask_jinja.context import ContextBuilder


class CommandFactory(object):
    def __init__(self, emprj_path=None):
        self.emprj_path = emprj_path
        self.context_builder = ContextBuilder(emprj_path=self.emprj_path)

    def make_init_command(self, args):
        return InitCommand(AppProject(self.emprj_path))

    def make_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommand(
            templates_path=self.templates_path,
            context_builder=self.context_builder,
            project_root=self.emprj_path
        )

    @property
    def templates_path(self):
        try:
            library_path = AppProject(self.emprj_path).task_library_path()
            if library_path:
                result = str(Path(library_path) / "templates")
            # test use fakefs which does work with Path().exists()
            if result and os.path.exists(result):
                return str(result)

            else:
                error_msg = f"'sqltask.library.path' property points to an invalid path '{result}'.\nPlease edit 'core.properties' file and make sure it points to the parent folder of your 'templates' folder."
                raise ValueError(error_msg)

        except KeyError:
            error_msg = """'sqltask.library.path' property not set.\nPlease add it to core.properties and make sure it points to the parent folder of your 'templates' folder."""
            raise ValueError(error_msg)

    def make_run_sql_command(self, args):
        return RunSQLCommand(
            templates_path=self.templates_path,
            context_builder=self.context_builder,
        )

    def make_create_sqltask_command(self, args):
        path = args["<directory>"]
        return CreateSQLTaskCommand(
            path=path,
            templates_path=self.templates_path,
            emprj_path=self.emprj_path,
        )

    def make_test_sql_templates_command(self, args):
        emprj_path = self.emprj_path
        if args["-q"]:
            verbose_mode = "-q"
        elif args["-v"]:
            verbose_mode = "-vv"
        else:
            verbose_mode = "-v"
        return TestTemplatesCommand(
            self.make_pytest(),
            templates_path=self.templates_path,
            emprj_path=emprj_path,
            verbose_mode=verbose_mode,
            test_group=args["--tests"],
            test_name=args["--test-name"],
            reuse_tests=args["--reuse-tests"],
        )

    def make_pytest(self):
        return pytest

    def make_extend_process_command(self, args):
        return ExtendProcessCommand()
