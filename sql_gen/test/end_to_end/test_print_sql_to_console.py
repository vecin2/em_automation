import pytest

from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner
from sql_gen.exceptions import EnvVarNotFoundException

@pytest.fixture
def app_runner():
    app_runner = PrintSQLToConsoleAppRunner()
    yield app_runner
    app_runner.teardown()


def test_it_throws_exception_when_no_templates_path_define(app_runner):
    with pytest.raises(ValueError) as  excinfo:
        app_runner.saveAndExit().run()
    assert "Templates path can not" in str(excinfo.value)

def test_it_throws_exception_when_empty_templates_path(app_runner):
    with pytest.raises(ValueError) as  excinfo:
        app_runner.using_templates_under("").saveAndExit().run()
    assert "Templates path can not" in str(excinfo.value)

def test_it_throws_exception_when_run_with_em_context_and_env_var_is_not_set(app_runner):
    with pytest.raises(EnvVarNotFoundException) as  excinfo:
        app_runner.using_templates_under("/my_templates")\
                  .saveAndExit()\
                  .run_prod()
    assert "path of your current EM project" in str(excinfo.value)


def test_returns_empty_when_no_template_selected(app_runner):
    app_runner.with_emproject_under("/em/prj")\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("")

def test_asks_for_template_until_valid_entry(app_runner):
    app_runner.with_emproject_under("/em/prj")\
               .select_template('abc',{})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("")\
               .assert_all_input_was_read()

def test_computes_templates_path_from_prj_path(app_runner,fs):
    fs.create_file("/em/prj/sqltask/templates/say_hello.sql", contents="hello!")
    app_runner.with_emproject_under("/em/prj")\
               .select_template('1. say_hello.sql',{})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello!")\
               .assert_all_input_was_read()

def test_select_and_render_no_vals_template(app_runner,fs):
    fs.create_file("/templates/say_hello.sql", contents="hello!")
    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .select_template('1. say_hello.sql',{})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello!")\
               .assert_all_input_was_read()

def test_select_and_render_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello David!")\
               .assert_all_input_was_read()


def test_fills_two_templates_and_combines_output(app_runner,fs):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('hello.sql',{'name':'John'})\
               .select_template('bye.sql',{'name':'Mark'})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello John!\nbye Mark!")\
               .assert_all_input_was_read()

def test_initial_context_is_used_when_filling_template(app_runner,fs):
    initial_context = {'_dummy_note': 'Dummy note'}
    fs.create_file("/templates/hello.sql", contents="hello {{_dummy_note}}!")

    app_runner.using_templates_under("/templates")\
               .with_initial_context(initial_context)\
               .select_template('hello.sql',{'dummy':'hello'})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello Dummy note!")\
               .assert_all_input_was_read()
