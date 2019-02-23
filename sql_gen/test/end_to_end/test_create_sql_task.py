import pytest

from sql_gen.test.utils.app_runner import CreateSQLTaskAppRunner,PrintSQLToConsoleAppRunner
from sql_gen.commands import SQLTask
@pytest.fixture
def app_runner():
    app_runner = CreateSQLTaskAppRunner()
    yield app_runner
    app_runner.teardown()

def test_creates_sql_task_under_path(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("/em/prj/modules/module_A")\
               .exist("/em/prj/modules/module_A/tableData.sql",
                       "hello David!")\
               .exist("/em/prj/modules/module_A/update.sequence",
                       "PROJECT $Revision: 123")\
               .assert_all_input_was_read()

