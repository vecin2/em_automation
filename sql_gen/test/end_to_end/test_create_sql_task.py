import pytest

from sql_gen.test.utils.app_runner import CreateSQLTaskAppRunner,SQLTask,PrintSQLToConsoleAppRunner
@pytest.fixture
def app_runner():
    app_runner = CreateSQLTaskAppRunner()
    yield app_runner
    app_runner.teardown()

@pytest.mark.skip
def test_select_and_srender_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_create_sqltask("ddd")\
               .assert_rendered_sql("hello David!")\
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
