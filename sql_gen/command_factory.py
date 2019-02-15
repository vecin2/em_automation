import argparse
import os

from sql_gen.create_sqltask_command import CreateSQLTaskCommand
from sql_gen.commands import PrintSQLToConsoleCommandFactory


class CommandFactory(object):
    def __init__(self,
                 print_sql_to_console_config=PrintSQLToConsoleCommandFactory()):
        self.print_sql_to_console_config = print_sql_to_console_config

    def make(self,env_vars=os.environ):
        args =self.parse_args()
        path = args.dir
        self.env_vars =env_vars
        if path:
            return CreateSQLTaskCommand()
        else:
            return self.make_print_sql_to_console_command(env_vars)

    def make_print_sql_to_console_command(self,env_vars):
        return self.print_sql_to_console_config.make(env_vars)

    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()


