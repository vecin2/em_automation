import pytest

from sql_gen.test.utils.app_runner import AppRunner
@pytest.fixture
def app_runner():
    app_runner = CreateSQLTaskAppRunner()
    yield app_runner
    app_runner.teardown()

@pytest.mark.skip
def test_select_and_render_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")
    files={'tableData.sql'   : "hello Martin!",
           'update.sequence' : "PROJECT $Revision: 123"
           }
    app_runner.using_templates_under("/templates")\
               .em_prj_under("/em/my_prj")\
               .with_svn_rev_no("122")\
               .select_template('greeting.sql',{'name':'Martin'})\
               .saveAndExit()\
               .run_create_sqltask("modules/module_A")\
               .assert_sqltask(files,"/modules/module_A")\
               .assert_all_input_was_read()
