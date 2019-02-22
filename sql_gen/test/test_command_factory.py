import sys
import pytest
from sql_gen.command_line_app import SysArgParser
from sql_gen.command_factory import CommandFactory


def class_name(instance):
    return instance.__class__.__name__

class StubCommandFactory(object):
    def make_print_sql_to_console_command(self):
        return "PrintSQL"

    def make_create_sqltask_command(self,path):
        return "CreateSQLTask"
def test_not_args_creates_sqltask_ouput_to_console():
    sys.argv=['.']
    parser = SysArgParser(CommandFactory())
    command = parser.parse()
    assert "PrintSQLToConsoleCommand" ==class_name(command)

def test_dir_args_creates_sqltask_ouput_to_file():
    sys.argv=['.','-d','modules/my_module']
    parser = SysArgParser(CommandFactory())
    command = parser.parse()
    assert "CreateSQLTaskCommand" ==class_name(command)
