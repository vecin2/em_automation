import sys
import pytest
from sql_gen.command_line_app import SysArgParser,CommandFactory
from unittest.mock import Mock


def class_name(instance):
    return instance.__class__.__name__

def test_not_args_creates_sqltask_ouput_to_console(fs):
    sys.argv=['.','print-sql']
    fs.create_dir('/opt/projects/my_project/sqltask/templates')
    env_vars ={'EM_CORE_HOME':'/opt/projects/my_project'}
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
