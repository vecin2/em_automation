import pytest

from devtask.commands import ExtendProcessCommand
from sql_gen.commands import (CreateSQLTaskCommand, InitCommand,
                              PrintSQLToConsoleCommand, RunSQLCommand,
                              TestTemplatesCommand)
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv


class CommandFactory(object):
    def __init__(self, project_home=None):
        if project_home:
            self.env_vars = project_home.env_vars
            self.emprj_path = project_home.path()

    def make_init_command(self, args):
        return InitCommand()

    def make_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommand(self.env_vars)

    def make_run_sql_command(self, args):
        template_name = args["--template"]
        return RunSQLCommand(
            emprj_path=self.emprj_path,
            env_vars=self.env_vars,
            template_name=template_name,
        )

    def make_create_sqltask_command(self, args):
        path = args["<directory>"]
        template_name = args["--template"]
        return CreateSQLTaskCommand(path=path, template_name=template_name)

    def make_test_sql_templates_command(self, args):
        templates_path = EMTemplatesEnv().extract_templates_path(self.env_vars)
        emprj_path = self.emprj_path
        if args["-q"]:
            verbose_mode = "-q"
        elif args["-v"]:
            verbose_mode = "-vv"
        else:
            verbose_mode = "-v"
        return TestTemplatesCommand(
            self.make_pytest(),
            templates_path=templates_path,
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
