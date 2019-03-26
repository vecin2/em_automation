import signal
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
    fs.create_dir("/em/prj")

    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("/em/prj/modules/module_A")\
               .exists("/em/prj/modules/module_A/tableData.sql",
                       "hello David!")\
               .exists("/em/prj/modules/module_A/update.sequence",
                       "PROJECT $Revision: 123 $")\
               .assert_all_input_was_read()\
               .assert_path_copied_to_sys_clipboard()

def test_creates_sqltask_from_relative_path(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    fs.create_dir("/em/prj")
    os.chdir("/templates")
    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('bye.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("modules/module_A")\
               .exists("/templates/modules/module_A/tableData.sql",
                       "bye David!")\
               .exists("/templates/modules/module_A/update.sequence",
                       "PROJECT $Revision: 123 $")\
               .assert_all_input_was_read()

def test_sqltask_exists_user_cancels_then_does_not_create(app_runner,fs):
    fs.create_dir("/prj/modules/moduleB/bye")

    app_runner.user_inputs("bad input")\
               .user_inputs("n")\
               .run_create_sqltask("/prj/modules/moduleB/bye")\
               .assert_all_input_was_read()
    assert False == os.path.exists("/prj/modules/moduleB/bye/tableData.sql")
    assert False == os.path.exists("/prj/modules/moduleB/bye/update.sequence")

def test_sqltask_exists_user_confirms_then_creates_sqltask(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    fs.create_dir("/prj/modules/moduleB/bye")
    fs.create_dir("/em/prj")

    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .user_inputs("y")\
               .select_template('bye.sql',{'name':'Frank'})\
               .saveAndExit()\
               .run_create_sqltask("/prj/modules/moduleB/bye")\
               .exists("/prj/modules/moduleB/bye/tableData.sql",
                       "bye Frank!")\
               .exists("/prj/modules/moduleB/bye/update.sequence",
                       "PROJECT $Revision: 123 $")\
               .assert_all_input_was_read()

def test_create_sqltask_uses_offset_svnrevision_property(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    fs.create_dir("/em/prj")

    app_runner.with_emproject_under("/em/prj")\
               .with_app_config({'svn.rev.no.offset':'10'})\
               .using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('bye.sql',{'name':'Frank'})\
               .saveAndExit()\
               .run_create_sqltask("/prj/modules/moduleB/bye")\
               .exists("/prj/modules/moduleB/bye/tableData.sql",
                       "bye Frank!")\
               .exists("/prj/modules/moduleB/bye/update.sequence",
                       "PROJECT $Revision: 133 $")\
               .assert_all_input_was_read()

def test_svn_throws_exception_returns_default_rev_no(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    fs.create_dir("/em/prj")

    app_runner.with_emproject_under("/em/prj")\
               .with_app_config({'svn.rev.no.offset':'11'})\
               .with_svn_rev_no(Exception("an error ocurred"))\
               .using_templates_under("/templates")\
               .select_template('bye.sql',{'name':'Frank'})\
               .saveAndExit()\
               .run_create_sqltask("/prj/modules/moduleB/bye")\
               .exists("/prj/modules/moduleB/bye/tableData.sql",
                       "bye Frank!")\
               .exists("/prj/modules/moduleB/bye/update.sequence",
                       "PROJECT $Revision: -1 $")\
               .assert_all_input_was_read()

def test_run_without_path_it_prompts_for_task_name_to_compute_path(app_runner,fs):
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    fs.create_dir("/em/prj")

    app_runner.with_emproject_under("/em/prj")\
               .with_sql_modules(["PRJCoreEmail","PRJCustomer"])\
               .with_app_config({'db.release.version':'Pacificorp_R_0_0_1'})\
               .using_templates_under("/templates")\
               .user_inputs("PRJCoreEmail")\
               .user_inputs("rewireEditEmail")\
               .select_template('bye.sql',{'name':'Frank'})\
               .saveAndExit()\
               .run_create_sqltask()\
               .exists("/em/prj/modules/PRJCoreEmail/sqlScripts/oracle/updates/Pacificorp_R_0_0_1//rewireEditEmail/tableData.sql",
                       "bye Frank!")\
               .assert_all_input_was_read()
               #

