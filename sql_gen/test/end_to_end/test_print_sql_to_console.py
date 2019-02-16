import pytest

from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner
@pytest.fixture
def app_runner():
    app_runner = PrintSQLToConsoleAppRunner()
    yield app_runner
    app_runner.teardown()


def test_returns_empty_when_no_template_selected(app_runner):
    app_runner.saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("")

def test_asks_for_template_until_valid_entry(app_runner):
    app_runner.select_template('abc',{})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("")\
               .assert_all_input_was_read()

def test_select_and_render_no_vals_template(app_runner,fs):
    fs.create_file("/templates/say_hello.sql", contents="hello!")
    app_runner.using_templates_under("/templates")\
               .select_template('1. say_hello.sql',{})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello!")\
               .assert_all_input_was_read()

def test_select_and_render_one_value_template(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello David!")\
               .assert_all_input_was_read()


def test_fills_two_templates_combines_output(app_runner,fs):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('hello.sql',{'name':'John'})\
               .select_template('bye.sql',{'name':'Mark'})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello John!\nbye Mark!")\
               .assert_all_input_was_read()

def test_initial_context_is_using_when_filling_template(app_runner,fs):
    initial_context = {'_dummy_note': 'Dummy note'}
    fs.create_file("/templates/hello.sql", contents="hello {{_dummy_note}}!")

    app_runner.using_templates_under("/templates")\
               .with_initial_context(initial_context)\
               .select_template('hello.sql',{'dummy':'hello'})\
               .saveAndExit()\
               .run_print_SQL_to_console()\
               .assert_rendered_sql("hello Dummy note!")\
               .assert_all_input_was_read()
