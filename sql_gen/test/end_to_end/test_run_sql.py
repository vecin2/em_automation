import pytest

from sql_gen.test.utils.app_runner import RunSQLAppRunner
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
from sql_gen.test.utils.fake_connection import FakeConnection


@pytest.fixture
def app_runner(fs, capsys):
    app_runner = RunSQLAppRunner(fs=fs)
    yield app_runner
    app_runner.teardown()


@pytest.fixture
def em_project(fs):
    em_root = "/fake/em/projects/my_project"
    em_project = FakeEMProjectBuilder(fs, root=em_root).base_setup().build()
    yield em_project


@pytest.fixture
def fake_connection(mocker):
    fake_connection = FakeConnection()
    yield fake_connection


# autouse allows to run this fixture even if we are not passing to test
# this allow us to mock the DB connection
@pytest.fixture(autouse=True)
def do_connect(mocker, fake_connection):
    mocked = mocker.patch("sql_gen.database.Connector.do_connect")
    mocked.return_value = fake_connection

    yield mocked


def test_select_stmt_does_not_need_confirmation_and_is_cached(
    fake_connection, app_runner, em_project, fs
):
    fake_connection.set_cursor_execute_results(
        ["firstname", "lastname"], [["David", "Garcia"]]
    )
    sql = "SELECT * FROM CE_CUSTOMER"
    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("list_customers.sql", sql).select_template(
        "list_customers.sql", {}
    ).saveAndExit().run_sql().assert_printed_sql(
        sql
    ).assert_all_input_was_read()
    # it runs twice the SQL: one when running the individual template
    # (which allows subsequent templates to see changes made by previous templates)
    # , and one at the end when user confim
    # However select stmts are currently cached and don't run a second time

    assert sql == fake_connection._cursor.executed_sql


def test_insert_statement_needs_confirmation_and_executes_twice(
    fake_connection, app_runner, em_project, fs
):
    sql = "INSERT INTO CE_CUSTOMER VALUES('{name}','{lastname}')"
    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("list_customers.sql", sql).select_template(
        "list_customers.sql", {"name": "David", "lastname": "Garcia"}
    ).saveAndExit().confirmRun().run_sql().assert_printed_sql(
        sql
    ).assert_all_input_was_read()
    # Because inserts are not cache the SQL is executed twice against the database
    # The first time is rolled back and the second time is the one that counts
    # need to investigate why is needed to run it the first time a rollback
    assert 2 * sql == fake_connection._cursor.executed_sql
