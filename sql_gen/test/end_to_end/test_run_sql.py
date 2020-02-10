
import pytest

from sql_gen.test.utils.app_runner import RunSQLAppRunner
from sql_gen.database.sqltable import SQLTable,SQLRow

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
               .confirmRun()\
               .run()\
               .assert_sql_executed("hello David!")\
               .assert_all_input_was_read()

def test_executed_select_stmt_prints_results(app_runner,fs):
    select_stmt="--this shows all the customers\n"+\
                "SELECT * FROM {{table_name}}"
    fs.create_file("/templates/view_customers.sql", contents=select_stmt)
    sqltable = SQLTable(
                        [SQLRow({"NAME":"Martin","SURNAME":"Landa"}),
                         SQLRow({"NAME":"Nelson","SURNAME":"Simpson"})]
                        )

    app_runner.using_templates_under("/templates")\
               .select_template('1. view_customers.sql',{'name':'CUSTOMER'})\
               .fetch_returns(sqltable)\
               .saveAndExit()\
               .run()\
               .assert_prints(str(sqltable))\
               .assert_all_input_was_read()

