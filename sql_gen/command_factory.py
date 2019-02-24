import os

from sql_gen.commands import PrintSQLToConsoleCommand,CreateSQLTaskCommand

class CommandFactory(object):
    def __init__(self, env_vars=os.environ):
        self.env_vars=env_vars

    def make_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommand()

    def make_create_sqltask_command(self,path):
        return CreateSQLTaskCommand(path=path)

