import sys
import pytest
from ccdev.command_line_app import SysArgParser,CommandFactory
from unittest.mock import Mock


def class_name(instance):
    return instance.__class__.__name__

def test_not_args_creates_sqltask_ouput_to_console():
    sys.argv=['.','print-sql']
    mocked_factory = Mock()
    parser = SysArgParser(mocked_factory)
    command = parser.parse()
    mocked_factory.make_print_sql_to_console_command.assert_called_once()

def test_dir_args_creates_sqltask_ouput_to_file():
    sys.argv=['.','create-sql','modules/my_module']
    mocked_factory = Mock()
    parser = SysArgParser(mocked_factory)
    command = parser.parse()
    mocked_factory.make_create_sqltask_command.assert_called_once()
