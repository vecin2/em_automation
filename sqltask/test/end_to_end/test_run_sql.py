import os
import tempfile
from pathlib import Path

import pytest

from sqltask.test.utils.app_runner import RunSQLAppRunner
from sqltask.test.utils.db_generator import QuickOracleDatabaseGenerator
from sqltask.test.utils.fake_connection import FakeOracleClient
from sqltask.test.utils.project_generator import (QuickLibraryGenerator,
                                                  QuickProjectGenerator)


@pytest.fixture
def app_runner():
    app_runner = RunSQLAppRunner()
    yield app_runner
    app_runner.teardown()


@pytest.fixture
def database():
    db_generator = QuickOracleDatabaseGenerator().generator()
    database = db_generator.generate()
    yield database


# autouse allows to run this fixture even if we are not passing it to test
# this allow us to mock the DB connection
@pytest.fixture(autouse=True)
def do_connect(mocker, database):
    mocked = mocker.patch("sqltask.database.Connector._oracleclient")
    mocked.return_value = FakeOracleClient(database)

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
    project_generator, library_generator, app_runner, database
):
    sql = "SELECT * FROM CE_CUSTOMER"
    library_generator.add_template("list_customers.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "list_customers.sql"
    ).saveAndExit().run_sql().assert_all_input_was_read()

    assert sql == database.executed_sql("ad")


def test_insert_statement_needs_confirmation_and_runs_once_against_db(
    project_generator, library_generator, app_runner, database
):
    sql = "INSERT INTO CE_CUSTOMER VALUES('David','Garcia')"
    library_generator.add_template("insert_customer.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "insert_customer.sql"
    ).saveAndExit().confirm_run().run_sql().assert_all_input_was_read()

    assert sql == database.executed_sql("ad")


def test_ad_template_run_against_ad_database(
    project_generator, library_generator, app_runner, database
):
    sql = "INSERT INTO CE_CUSTOMER VALUES('David','Garcia')"
    library_generator.add_template("insert_customer.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "insert_customer.sql"
    ).saveAndExit().confirm_run().run_sql()

    assert sql == database.executed_sql("ad")


def test_tps_template_run_against_tps_database(
    project_generator, library_generator, app_runner, database
):
    sql = "INSERT INTO TENANT_PROPERTY VALUES('max.no.chats','5')"
    library_generator.add_tps_template("add_property.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_tps_template(
        "add_property.sql"
    ).saveAndExit().confirm_run().run_sql()

    assert sql == database.executed_sql("tps")


@pytest.mark.skip
# run multiple templates for different schemas
# within the same session is currently not supported
def test_run_ad_template_follow_by_tps_template(
    project_generator, library_generator, app_runner, database
):
    ad_sql = "INSERT INTO CE_CUSTOMER (FIRSNAME,LASTNAME) VALUES('Robert','Dubrey')"
    library_generator.add_template("add_customer.sql", ad_sql)
    tps_sql = "INSERT INTO TENANT_PROPERTY (NAME,VALUE) VALUES('max.no.chats','5')"
    library_generator.add_tps_template("add_property.sql", tps_sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template("add_customer.sql").select_tps_template(
        "add_property.sql"
    ).saveAndExit().confirm_run().run_sql()

    assert ad_sql == database.executed_sql("ad")
    assert tps_sql == database.executed_sql("tps")


@pytest.fixture
def spy_os_system(mocker):
    spy_os_system = mocker.spy(os, "system")
    yield spy_os_system


def test_when_runsql_select_template_with_edit_flag_keeps_selection_and_runs_edit_configured_command(
    project_generator, library_generator, app_runner, database, spy_os_system
):
    text_to_print = "I am testing the edit command!!!!"
    ad_sql = "INSERT INTO CE_CUSTOMER (FIRSNAME,LASTNAME) VALUES('Robert2','Dubrey')"
    project_generator.with_edit_cmd(f'echo "{text_to_print}"')
    library_generator.add_template("add_cust.sql", ad_sql)

    app_runner.with_project(project_generator.generate())

    # confirm after edit, keeps the name of the template as default
    app_runner.edit_template(
        "add_cust.sql"
    ).confirm().saveAndExit().confirm_run().run_sql()

    assert ad_sql == database.executed_sql("ad")
    expected_cmd = f'echo "{text_to_print}"'
    spy_os_system.assert_called_once_with(expected_cmd)


def test_when_runsql_without_edit_cmd_configured_then_select_template_with_edit_flag_is_ignored_until_flag_is_removed(
    project_generator, library_generator, app_runner, database, spy_os_system
):
    project_generator.with_edit_cmd(None)
    ad_sql = "INSERT INTO CE_CUSTOMER (FIRSNAME,LASTNAME) VALUES('Robert2','Dubrey')"
    library_generator.add_template("add_cust.sql", ad_sql)

    app_runner.with_project(project_generator.generate())
    # confirm after edit, keeps the name of the template as default
    app_runner.edit_template(
        "add_cust.sql"
    ).confirm().saveAndExit().confirm_run().run_sql()

    assert ad_sql == database.executed_sql("ad")
    spy_os_system.assert_not_called()
