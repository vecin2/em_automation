import os
import sql_gen.docopt_parser as arg_parser

from sql_gen.command_factory import CommandFactory

class SysArgParser (object):
    def __init__(self, command_factory=CommandFactory()):
        self.command_factory=command_factory

    def parse(self):
        args = arg_parser.parse()
        path = args['<directory>']
        if path:
            return self.command_factory.make_create_sqltask_command(path)
        else:
            return self.command_factory.make_print_sql_to_console_command()

    def parse_args(self):
        arguments = docopt(__doc__, version='dtask 0.1')
        print(arguments)
        return arguments

class CommandLineSQLTaskApp(object):
    """"""
    def __init__(self,args_factory=CommandFactory(os.environ)):
        self.args_factory = args_factory

    def run(self):
        try:
            self._dorun()
        except KeyboardInterrupt as excinfo:
            print( '\n KeyboardInterrupt exception')
        except Exception as excinfo:
            raise(excinfo)

    def _dorun (self):
        command =SysArgParser(self.args_factory).parse()
        command.run()

