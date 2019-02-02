import sys
from sql_gen.command_line_app import CommanLineApp
from sql_gen.create_sqltask_app import CreateSQLTaskApp

def test_invokes_create_app_with_dir_from_args():
    sys.argv=['.','-d','modules/my_module']
    create_task_app=CreateSQLTaskApp()
    app = CommanLineApp(create_task_app)
    app.run()
    assert create_task_app.path == 'modules/my_module'

def test_invokes_create_app_with_dir_from_args_when_no_dir_passed():
    sys.argv=['.']
    create_task_app=CreateSQLTaskApp()
    app = CommanLineApp(create_task_app)
    app.run()
    assert create_task_app.path == None
