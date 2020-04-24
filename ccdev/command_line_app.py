import sys
import os

import sql_gen
import ccdev.docopt_parser as arg_parser
from sql_gen.app_project import AppProject
from ccdev.command_factory import CommandFactory

class SysArgParser (object):
    def __init__(self, command_factory=CommandFactory()):
        self.command_factory=command_factory

    def parse(self):
        args = arg_parser.parse()
        if args['create-sql']:
            return self.command_factory.make_create_sqltask_command(args)
        elif args['print-sql']:
            return self.command_factory.make_print_sql_to_console_command()
        elif args['test-sql']:
            return self.command_factory.make_test_sql_templates_command(args)
        elif args['run-sql']:
            return self.command_factory.make_run_sql_command(args)
        elif args['extend-process']:
            return self.command_factory.make_extend_process_command(args)
        #else:
        #    return self.command_factory.make_interactive_shell_command(args)

    def parse_args(self):
        arguments = docopt(__doc__, version='dtask 0.1')
        print(arguments)
        return arguments

class CommandLineSQLTaskApp(object):
    """"""
    def __init__(self,args_factory=CommandFactory(os.environ),logger=None):
        self.args_factory = args_factory
        if logger:
            AppProject.set_logger(logger)
        else:
            AppProject(os.environ).setup_logger()
        self._logger =logger

    def run(self):
        try:
            self._dorun()
        except KeyboardInterrupt as excinfo:
            print( '\n KeyboardInterrupt exception')
        except Exception as excinfo:
            raise(excinfo)

    def _dorun (self):
        sql_gen.logger.info("Starting application with params: "+str(sys.argv))
        command =SysArgParser(self.args_factory).parse()
        command.run()

