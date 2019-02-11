from sql_gen.command_factory import CommandFactory
import sys
def class_name(instance):
    return instance.__class__.__name__

def test_not_args_creates_sqltask_ouput_to_console():
    sys.argv=['.']
    factory = CommandFactory()
    command = factory.make()
    assert "PrintSQLToConsoleCommand" ==class_name(command)

def test_dir_arg_creates_sqltask_ouput_to_file():
    sys.argv=['.','-d','modules/my_module']
    factory = CommandFactory()
    command = factory.make()
    assert "CreateSQLTaskCommand" ==class_name(command)
