import os
import argparse

from sql_gen.command_factory import CommandFactory

class SysArgParser (object):
    def __init__(self, command_factory):
        self.command_factory=command_factory

    def parse(self):
        args =self.parse_args()
        path = args.dir
        if path:
            return self.command_factory.make_create_sqltask_command(path)
        else:
            return self.command_factory.make_print_sql_to_console_command()

    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()

class CommandLineSQLTaskApp(object):
    """"""
    def __init__(self,args_factory=CommandFactory()):
        self.args_factory = args_factory
    def run (self):
        command =SysArgParser(self.args_factory).parse()
        command.run()

