import pytest

from sql_gen.test.utils.app_runner import CreateSQLTaskAppRunner
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
from sql_gen.test.utils.fake_connection import FakeConnection


@pytest.fixture
def app_runner(fs):
    app_runner = CreateSQLTaskAppRunner(fs=fs)
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


def test_creates_sqltask_when_path_passed_as_arg(app_runner, em_project, fs):
    sql = "INSERT INTO CE_CUSTOMER VALUES('{{name}}','{{lastname}}')"
    final_sql = "INSERT INTO CE_CUSTOMER VALUES('David','Garcia')"
    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("list_customers.sql", sql)

    app_runner.select_template(
        "list_customers.sql", {"name": "David", "lastname": "Garcia"}
    ).saveAndExit().create_sql(
        "/em/prj/modules/module_A"
    ).assert_all_input_was_read().exists(
        "/em/prj/modules/module_A/tableData.sql", final_sql
    ).exists_regex(
        "/em/prj/modules/module_A/update.sequence", "PROJECT \$Revision: \d+ \$"
    )


def test_sqltask_exists_user_cancels_then_does_not_create(app_runner, em_project, fs):
    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("dummy1.sql", "dummy1").add_template("dummy2.sql", "dummy2")

    app_runner.select_template("dummy1.sql", {}).saveAndExit().create_sql(
        "/em/prj/modules/module_A"
    )
    app_runner.assert_all_input_was_read().exists(
        "/em/prj/modules/module_A/tableData.sql", "dummy1"  # creates SQL
    )

    # override sqltask folder
    override_task = "n"
    app_runner.user_inputs(override_task).select_template(
        "dummy2.sql", {}
    ).saveAndExit().create_sql("/em/prj/modules/module_B")
    app_runner.assert_all_input_was_read().exists(
        "/em/prj/modules/module_A/tableData.sql", "dummy1"  # was not overriden
    )


def test_sqltask_exists_user_confirms_then_creates_sqltask(app_runner, em_project, fs):
    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("dummy1.sql", "dummy1").add_template("dummy2.sql", "dummy2")

    app_runner.select_template("dummy1.sql", {}).saveAndExit().create_sql(
        "/em/prj/modules/module_B"
    )
    app_runner.assert_all_input_was_read().exists(
        "/em/prj/modules/module_B/tableData.sql", "dummy1"  # creates SQL
    )

    # override sqltask folder
    override_task = "y"
    app_runner.user_inputs(override_task).select_template(
        "dummy2.sql", {}
    ).saveAndExit().create_sql("/em/prj/modules/module_B")
    app_runner.assert_all_input_was_read().exists(
        "/em/prj/modules/module_B/tableData.sql", "dummy2"  # was not overriden
    )


def test_when_seq_generator_throws_exception_writes_negative_one_to_update_sequence(
    app_runner, fs, em_project, mocker
):
    mocked = mocker.patch(
        "sql_gen.commands.create_sql_cmd.TimeStampGenerator.generate_seq_no"
    )
    mocked.side_effect = ValueError("Some mocked error")

    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("dummy1.sql", "dummy1").select_template(
        "dummy1.sql", {}
    ).saveAndExit().create_sql(
        "/em/prj/modules/moduleB"
    )
    app_runner.exists(
        "/em/prj/modules/moduleB/update.sequence", "PROJECT $Revision: -1 $"
    ).assert_all_input_was_read()


def test_run_without_path_it_prompts_for_task_name_to_compute_path(
    app_runner, em_project, fs
):
    sql = "INSERT INTO PERSON VALUES('{{name}}','{{lastname}}')"
    final_sql = "INSERT INTO PERSON VALUES('John','Smith')"

    sqltask_path = None
    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("list_customers.sql", sql)

    app_runner.user_inputs("PRJCoreEmail").user_inputs(
        "rewireEditEmail"
    ).select_template(
        "list_customers.sql", {"name": "John", "lastname": "Smith"}
    ).saveAndExit().create_sql(
        sqltask_path
    ).assert_all_input_was_read().exists(
        "/fake/em/projects/my_project/modules/PRJCoreEmail/sqlScripts/oracle/updates/PRJ01/rewireEditEmail/tableData.sql",
        final_sql,
    ).exists_regex(
        "/fake/em/projects/my_project/modules/PRJCoreEmail/sqlScripts/oracle/updates/PRJ01/rewireEditEmail/update.sequence",
        "PROJECT \$Revision: \d+ \$",
    )


def test_when_pass_template_does_not_prompt_for_template(app_runner, em_project, fs):
    sql = "INSERT INTO PERSON VALUES('{{name}}','{{lastname}}')"
    final_sql = "INSERT INTO PERSON VALUES('John','Smith')"

    app_runner.with_emproject(em_project).using_templates_under(
        "/templates"
    ).add_template("create_customer.sql", sql)

    app_runner.user_inputs("PRJCoreEmail").user_inputs("rewireEditEmail").user_inputs(
        "John"
    ).user_inputs("Smith").saveAndExit().create_sql(
        template="create_customer.sql"
    ).assert_all_input_was_read().exists(
        "/fake/em/projects/my_project/modules/PRJCoreEmail/sqlScripts/oracle/updates/PRJ01/rewireEditEmail/tableData.sql",
        final_sql,
    ).exists_regex(
        "/fake/em/projects/my_project/modules/PRJCoreEmail/sqlScripts/oracle/updates/PRJ01/rewireEditEmail/update.sequence",
        "PROJECT \$Revision: \d+ \$",
    )
