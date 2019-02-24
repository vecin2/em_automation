import os
import pytest

from sql_gen.test.utils.app_runner import CreateSQLTaskAppRunner,PrintSQLToConsoleAppRunner
from sql_gen.commands import SQLTask
@pytest.fixture
def app_runner():
    app_runner = CreateSQLTaskAppRunner()
    yield app_runner
    app_runner.teardown()

def test_creates_sqltask_from_absolute_path(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("/em/prj/modules/module_A")\
               .exist("/em/prj/modules/module_A/tableData.sql",
                       "hello David!")\
               .exist("/em/prj/modules/module_A/update.sequence",
                       "PROJECT $Revision: 123")\
               .assert_all_input_was_read()

def test_creates_sqltask_from_relative_path(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")

    os.chdir("/templates")
    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('bye.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("modules/module_A")\
               .exist("/templates/modules/module_A/tableData.sql",
                       "bye David!")\
               .exist("/templates/modules/module_A/update.sequence",
                       "PROJECT $Revision: 123")\
               .assert_all_input_was_read()

def test_sqltask_exists_user_cancels_then_does_not_create(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    fs.create_dir("/prj/modules/moduleB/bye")
    os.chdir("/prj")
    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .user_inputs("bad input")\
               .user_inputs("n")\
               .run_create_sqltask("modules/moduleB/bye")\
               .assert_all_input_was_read()
    assert False == os.path.exists("/prj/modules/moduleB/bye/tableData.sql")
    assert False == os.path.exists("/prj/modules/moduleB/bye/update.sequence")
