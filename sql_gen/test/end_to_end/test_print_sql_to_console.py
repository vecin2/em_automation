import pytest

from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner
from sql_gen.exceptions import EnvVarNotFoundException

@pytest.fixture
def app_runner(fs):
    app_runner = PrintSQLToConsoleAppRunner(fs=fs)
    yield app_runner
    app_runner.teardown()


def test_it_throws_exception_when_no_templates_path_define(app_runner):
    with pytest.raises(ValueError) as  excinfo:
        app_runner.saveAndExit().run()
    assert "Templates path can not" in str(excinfo.value)

def test_it_throws_exception_when_templates_path_does_not_exist(app_runner):
    with pytest.raises(ValueError) as  excinfo:
        app_runner.using_templates_under("").saveAndExit().run()
    assert "Make sure the directory is created" in str(excinfo.value)

def test_it_throws_exception_when_run_with_em_context_and_env_var_is_not_set(fs,app_runner):
    fs.create_dir("/my_templates")
    with pytest.raises(EnvVarNotFoundException) as  excinfo:
        app_runner.using_templates_under("/my_templates")\
                  .saveAndExit()\
                  .run_prod()
    assert "path of your current EM project" in str(excinfo.value)

def test_it_throws_exception_when_run_with_em_context_and_em_path_does_not_exist(app_runner,fs):
    fs.create_dir("/my_templates")
    with pytest.raises(ValueError) as  excinfo:
        app_runner.with_emproject_under("/em/prj")\
                  .using_templates_under("/my_templates")\
                  .saveAndExit()\
                  .run_prod()
    assert "points to an invalid path" in str(excinfo.value)


def test_returns_empty_when_no_template_selected(app_runner,fs):
    fs.create_dir("/my_templates")
    app_runner.using_templates_under("/my_templates")\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("")

def test_asks_for_template_until_valid_entry(app_runner,fs):
    fs.create_dir("/templates")
    app_runner.using_templates_under("/templates")\
               .select_template('abc',{})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("")\
               .assert_all_input_was_read()

def test_computes_templates_path_from_prj_path(app_runner,fs):
    app_runner.with_emproject_under("/em/prj")\
               .and_prj_built_under("/em/prj")\
               .add_template("say_hello.sql","hello!")\
               .select_template('1. say_hello.sql',{})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello!")\
               .assert_all_input_was_read()

def test_computes_templates_path_from_current_path(app_runner):
    app_runner.and_prj_built_under("/em/prj")\
               .from_current_dir("/em/prj")\
               .add_template("say_bye.sql","bye!")\
               .select_template('say_bye.sql',{})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("bye!")\
               .assert_all_input_was_read()

def test_select_and_render_no_vals_template(app_runner,fs):
    app_runner.with_emproject_under("/em/prj")\
               .using_templates_under("/templates")\
               .add_template("say_hello.sql","hello!")\
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

def test_user_goes_back_and_render_template(app_runner,fs):
    contents="hello {{name}} {{surname}}!"
    fs.create_file("/templates/greeting.sql", contents=contents)

    # '<' goes back and prompts name again
    values=['David','<','Juan','Rodriguez']
    app_runner.using_templates_under("/templates")\
               .select_template('1. greeting.sql',values)\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello Juan Rodriguez!")\
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
               .with_template_API(initial_context)\
               .select_template('hello.sql',{'dummy':'hello'})\
               .saveAndExit()\
               .run()\
               .assert_rendered_sql("hello Dummy note!")\
               .assert_all_input_was_read()
