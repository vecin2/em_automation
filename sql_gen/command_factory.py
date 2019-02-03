from sql_gen.create_sqltask_command import CreateSQLTaskCommand
from sql_gen.print_sql_to_console import PrintSQLToConsole
import argparse

class CommandFactory(object):
    def make(self):
        args =self.parse_args()
        path = args.dir
        if path:
            return CreateSQLTaskCommand()
        else:
            return PrintSQLToConsole()

    def parse_args(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
        return ap.parse_args()


