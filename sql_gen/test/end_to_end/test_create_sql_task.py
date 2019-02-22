import pytest

from sql_gen.test.utils.app_runner import CreateSQLTaskAppRunner,PrintSQLToConsoleAppRunner
from sql_gen.commands import SQLTask
@pytest.fixture
def app_runner():
    app_runner = CreateSQLTaskAppRunner()
    yield app_runner
    app_runner.teardown()

def test_select_and_srender_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")
    expected_sqltask=SQLTask(
                    path="/modules/module_A",
                    table_data="hello David!",
                    update_sequence="PROJECT $Revision: 123")

    app_runner.using_templates_under("/templates")\
               .with_svn_rev_no("122")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("/modules/module_A")\
               .assert_sqltask(expected_sqltask)\
               .assert_all_input_was_read()
@pytest.mark.skip
def test_select_and_render_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")
    expected_sqltask=SQLTask(
                    path="/modules/module_A",
                    table_data="hello Martin",
                    update_sequence="PROJECT $Revision: 123")

    app_runner.using_templates_under("/templates")\
               .em_prj_under("/em/my_prj")\
               .select_template('greeting.sql',{'name':'Martin'})\
               .saveAndExit()\
               .run_create_sqltask("ddd")\
               .assert_rendered_sql("ddda")\
               .assert_all_input_was_read()
