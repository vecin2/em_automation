
import pytest

from sql_gen.test.utils.app_runner import RunSQLAppRunner

@pytest.fixture
def app_runner(fs,capsys):
    app_runner = RunSQLAppRunner(fs=fs)
    yield app_runner
    app_runner.teardown()


def test_executes_template_filled_against_db(app_runner,fs):
    fs.create_file("/templates/greeting.sql", contents="hello {{name}}!")

    app_runner.using_templates_under("/templates")\
               .select_template('1. greeting.sql',{'name':'David'})\
               .saveAndExit()\
               .run()\
               .assert_sql_executed("hello David!")\
               .assert_all_input_was_read()

