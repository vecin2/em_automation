import tempfile
from pathlib import Path

import pytest

from sql_gen.test.utils.app_runner import CreateSQLTaskAppRunner
from sql_gen.test.utils.fake_connection import FakeConnection
from sql_gen.test.utils.project_generator import (QuickLibraryGenerator,
                                                  QuickProjectGenerator)

######### FIXTURES #############


@pytest.fixture
def app_runner():
    app_runner = CreateSQLTaskAppRunner()
    yield app_runner
    app_runner.teardown()


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


######### TESTS #############
def test_passing_path_as_arg_does_not_prompt_for_it(
    project_generator, library_generator, app_runner
):

    sql = "INSERT INTO CE_CUSTOMER VALUES('{{name}}','{{lastname}}')"
    final_sql = "INSERT INTO CE_CUSTOMER VALUES('Mary','Jane')"

    library_generator.add_template("insert_customer.sql", sql)

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "insert_customer.sql", {"name": "Mary", "lastname": "Jane"}
    ).saveAndExit().create_sql("module_A").exists(
        "module_A/tableData.sql", final_sql
    ).exists(
        "module_A/update.sequence", "PROJECT \$Revision: \d+ \$"
    )


def test_sqltask_exists_user_cancels_then_does_not_create(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("dummy1.sql", "dummy1")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template("dummy1.sql").saveAndExit().create_sql("module_A")
    app_runner.assert_all_input_was_read().exists(
        "module_A/tableData.sql", "dummy1"  # creates SQL first time
    )

    override_task = "n"
    app_runner.user_inputs(override_task).create_sql(
        "module_A"
    )  # try create on the smae localtion

    app_runner.assert_all_input_was_read().exists(
        "module_A/tableData.sql", "dummy1"  # was not overriden
    )


def test_sqltask_exists_user_confirms_then_creates_sqltask(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("dummy1.sql", "dummy1").add_template(
        "dummy2.sql", "dummy2"
    )

    app_runner.with_project(project_generator.generate())
    app_runner.select_template("dummy1.sql").saveAndExit().create_sql("module_A")
    app_runner.assert_all_input_was_read().exists(
        "module_A/tableData.sql", "dummy1"  # creates SQL first time
    )

    override_task = "y"
    # app_runner.user_inputs(override_task).create_sql("module_A") #try create on the smae localtion
    app_runner.user_inputs(override_task).select_template(
        "dummy2.sql"
    ).saveAndExit().create_sql("module_A")

    app_runner.assert_all_input_was_read().exists(
        "module_A/tableData.sql", "dummy2"  # was overriden
    )


def test_when_seq_generator_throws_exception_writes_negative_one_to_update_sequence(
    project_generator, library_generator, app_runner, mocker
):
    mocked = mocker.patch(
        "sql_gen.commands.create_sql_cmd.TimeStampGenerator.generate_seq_no"
    )
    mocked.side_effect = ValueError("Some mocked error")

    library_generator.add_template("dummy1.sql", "dummy1")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template("dummy1.sql").saveAndExit().create_sql("module_A")
    app_runner.assert_all_input_was_read().exists(
        "module_A/tableData.sql", "dummy1"  # creates SQL first time
    )

    app_runner.exists("module_A/update.sequence", "PROJECT $Revision: -1 $")


def test_run_prompts_module_task_name_and_creates_modules_dir_when_not_exist(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("dummy1.sql", "dummy1")
    project_generator.append_release("PRJ_01")
    app_runner.with_project(project_generator.generate())

    app_runner.with_sql_module("PRJCoreEmail").and_task_name(
        "rewireEditEmail"
    ).select_template("dummy1.sql").saveAndExit().create_sql(None)
    app_runner.assert_all_input_was_read()
    app_runner.exists_table_data(release_name="PRJ_01", expected_content="dummy1")
    app_runner.exists_update_seq(
        release_name="PRJ_01"
    ).assert_path_copied_to_sys_clipboard("PRJ_01")
