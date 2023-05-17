import tempfile
from pathlib import Path

import pytest

from sqltask.test.utils.app_runner import RunSQLAppRunner
from sqltask.test.utils.emproject_test_util import FakeEMProjectBuilder
from sqltask.test.utils.fake_connection import FakeConnection
from sqltask.test.utils.project_generator import (QuickLibraryGenerator,
                                                  QuickProjectGenerator)


@pytest.fixture
def app_runner():
    app_runner = RunSQLAppRunner()
    yield app_runner
    app_runner.teardown()

@pytest.fixture
def fake_connection(mocker):
    fake_connection = FakeConnection()
    yield fake_connection


# autouse allows to run this fixture even if we are not passing it to test
# this allow us to mock the DB connection
@pytest.fixture(autouse=True)
def do_connect(mocker, fake_connection):
    mocked = mocker.patch("sqltask.database.Connector.do_connect")
    mocked.return_value = fake_connection

    yield mocked


@pytest.fixture
def root():
    with tempfile.TemporaryDirectory() as root:
        yield Path(root)


@pytest.fixture
def project_generator(root):
    quick_generator = QuickProjectGenerator(root / "trunk")
    yield quick_generator.make_project_generator()


@pytest.fixture
def library_generator(project_generator):
    quick_generator = QuickLibraryGenerator(project_generator.root.parent / "library")
    library_generator = quick_generator.make_library_generator()
    project_generator.with_library(library_generator)
    yield library_generator


def test_select_stmt_does_not_need_confirmation_and_is_cached(
    project_generator, library_generator, app_runner, fake_connection
):
    fake_connection.set_cursor_execute_results(
        ["firstname", "lastname"], [["David", "Garcia"]]
    )

    sql = "SELECT * FROM CE_CUSTOMER"
    library_generator.add_template("list_customers.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "list_customers.sql"
    ).saveAndExit().run_sql().assert_all_input_was_read()

    assert sql == fake_connection._cursor.executed_sql


def test_insert_statement_needs_confirmation_and_runs_once_against_db(
    project_generator, library_generator, app_runner, fake_connection
):
    sql = "INSERT INTO CE_CUSTOMER VALUES('David','Garcia')"
    library_generator.add_template("insert_customer.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "insert_customer.sql"
    ).saveAndExit().confirm_run().run_sql().assert_all_input_was_read()

    assert sql == fake_connection._cursor.executed_sql
