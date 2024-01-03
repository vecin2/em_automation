import pytest

from devtask.commands import ExtendProcessCommand
from sqltask.app_project import AppProject
from sqltask.commands import (CreateSQLTaskCommand, InitCommand,
                              PrintSQLToConsoleCommand, RunSQLCommand,
                              TestTemplatesCommand)
from sqltask.commands.generate_libdocs_cmd.generate_libdocs_cmd import GenerateLibDocsCommand


class CommandFactory(object):
    def __init__(self, project=None, console_printer=None):
        self.project = project
        self.console_printer = console_printer

    def make_init_command(self, args):
        return InitCommand(AppProject(self.projectroot))

    def make_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommand(project=self.project)

    @property
    def projectroot(self):
        return self.project.emroot

    @property
    def templates_path(self):
        return self.project.library().templates_path

    def make_run_sql_command(self, args):
        return RunSQLCommand(project=self.project)

    def make_create_sqltask_command(self, args):
        path = args["<directory>"]
        return CreateSQLTaskCommand(
            path=path,
            project=self.project,
        )

    def make_test_sql_templates_command(self, args):
        if args["-q"]:
            verbose_mode = "-q"
        elif args["-v"]:
            verbose_mode = "-vv"
        else:
            verbose_mode = "-v"
        return TestTemplatesCommand(
            self.make_pytest(),
            templates_path=self.templates_path,
            emprj_path=self.projectroot,
            project=self.project,
            verbose_mode=verbose_mode,
            test_group=args["--tests"],
            test_name=args["--test-name"],
            reuse_tests=args["--reuse-tests"],
        )

    def make_pytest(self):
        return pytest

    def make_extend_process_command(self, args):
        return ExtendProcessCommand()

    def make_generate_libdocs_command(self, args):
        return GenerateLibDocsCommand(self.project.library_path())
