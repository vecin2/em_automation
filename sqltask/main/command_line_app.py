import sys

import sqltask
import sqltask.main.docopt_parser as arg_parser
from sqltask.app_project import AppProject
from sqltask.main.command_factory import CommandFactory
from sqltask.main.project_home import ProjectHome


class SysArgParser(object):
    def __init__(self, command_factory=None):
        self.command_factory = command_factory

    def parse(self):
        args = arg_parser.parse()

        if args["init"]:
            return self.command_factory.make_init_command(args)
        elif args["create-sql"]:
            return self.command_factory.make_create_sqltask_command(args)
        elif args["print-sql"]:
            return self.command_factory.make_print_sql_to_console_command()
        elif args["test-sql"]:
            return self.command_factory.make_test_sql_templates_command(args)
        elif args["run-sql"]:
            return self.command_factory.make_run_sql_command(args)
        elif args["import-templates"]:
            return self.command_factory.make_import_templates_command(args)
        # elif args["extend-process"]:
        #     return self.command_factory.make_extend_process_command(args)
        # else:
        #    return self.command_factory.make_interactive_shell_command(args)


class CommandLineSQLTaskApp(object):
    """"""

    def __init__(
        self,
        project_home=None,
        args_factory=None,
        logger=None,
    ):
        self.args_factory = args_factory

        self.emprj_path = project_home.path()
        if logger:
            AppProject.set_logger(logger)
        else:
            AppProject(emprj_path=project_home.path()).setup_logger()
        self._logger = logger
        self.last_command_run = None

    @staticmethod
    def build_app(cwd, env_vars=None, logger=None):
        project_home = ProjectHome(cwd, env_vars)
        app = CommandLineSQLTaskApp(
            project_home=project_home,
            args_factory=CommandFactory(
                project_home.path(),
            ),
            logger=logger,
        )
        return app

    def run(self):
        try:
            return self._dorun()
        except KeyboardInterrupt:
            print("\n KeyboardInterrupt exception")
        except Exception as excinfo:
            raise (excinfo)

    def _dorun(self):
        sqltask.logger.info("Starting application with params: " + str(sys.argv))
        command = SysArgParser(self.args_factory).parse()
        command.run()
        self.last_command_run = command
