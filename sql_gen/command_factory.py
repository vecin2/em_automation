import argparse

from sql_gen.create_sqltask_command import CreateSQLTaskCommand
from sql_gen.commands import PrintSQLToConsoleCommandBuilder
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv


class CommandFactory(object):
    def make(self):
        args =self.parse_args()
        path = args.dir
        if path:
            return CreateSQLTaskCommand()
        else:
            return self.make_print_sql_to_console_command()

    def make_print_sql_to_console_command(self):
        return PrintSQLToConsoleCommandBuilder().\
                    with_environment(EMTemplatesEnv().get_env()).\
                    with_sql_renderer(FakeSQLRenderer()).\
                    build()


    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()


