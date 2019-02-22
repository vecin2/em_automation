import sys
import pytest
from sql_gen.command_line_app import SysArgParser


def class_name(instance):
    return instance.__class__.__name__

def test_not_args_creates_sqltask_ouput_to_console():
    sys.argv=['.']
    parser = SysArgParser()
    command = parser.parse()
    assert "PrintSQLToConsoleCommand" ==class_name(command)

def test_dir_args_creates_sqltask_ouput_to_file():
    sys.argv=['.','-d','modules/my_module']
    parser = SysArgParser()
    command = parser.parse()
    assert "CreateSQLTaskCommand" ==class_name(command)
