import pytest

from sql_gen.commands.verify_templates_cmd import (ExpectedSQLTestTemplate,
                                                   RunOnDBTestTemplate)
from sql_gen.test.utils.app_runner import TemplatesAppRunner
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder


@pytest.fixture
def em_project(fs):
    em_root = "/fake/em/projects/my_project"
    em_project = FakeEMProjectBuilder(fs, root=em_root).base_setup().build()
    yield em_project


@pytest.fixture
def app_runner(fs, capsys):
    app_runner = TemplatesAppRunner(fs=fs, capsys=capsys)
    yield app_runner
    app_runner.teardown()


# autouse allows to run this fixture even if we are not passing to test
@pytest.fixture(autouse=True)
def fake_pytest(mocker):
    make_pytest = mocker.patch("ccdev.command_factory.CommandFactory.make_pytest")
    yield make_pytest


def test_expects_test_folder_to_be_next_to_templates_folder_and_fails_if_not_exists(
    app_runner, em_project, fs
):
    expected = "Test folder '/library/test_templates' does not exist.\n"
    sql = "SELECT * FROM CE_CUSTOMER"
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "list_customers.sql", sql
    ).test_sql().assert_message_printed(expected)


def test_test_name_not_matching_template_generates_unable_to_find_template_test(
    app_runner, fs, em_project
):
    expected_sql = ExpectedSQLTestTemplate().render(
        template_name="greeting", expected="hello John!", actual=""
    )
    run_on_db = RunOnDBTestTemplate().render(
        template_name="greeting", query="hello John!", emprj_path=em_project.root
    )
    check_sql = expected_sql.add(run_on_db)
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "other_name.sql", "some template"
    ).make_test_dir().add_test(
        "test_greeting.sql", {}, "hello John!"
    ).test_sql().assert_generated_tests(
        check_sql
    )


def test_groovy_extension_does_generate_run_on_db(app_runner, em_project, fs):
    expected_sql = ExpectedSQLTestTemplate().render(
        template_name="greeting", expected="hello John!", actual="hello John!"
    )
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "greeting.groovy", "hello John!"
    ).make_test_dir().add_test(
        "test_greeting.groovy", {}, "hello John!"
    ).test_sql().assert_generated_tests(
        expected_sql
    )


def test_testname_not_sql_ext_does_not_run(app_runner, em_project, fs):
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "greting.sql", "hello John!"
    ).make_test_dir().add_test(
        "test_greeting.sqls", {}, "hello John!"
    ).test_sql().generates_no_test()


def test_generates_test_expected_sql_from_list(app_runner, fs, em_project):
    expected_sql = ExpectedSQLTestTemplate().render(
        template_name="greeting", expected="hello John!", actual="hello John!"
    )
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "greeting.sql", "hello {{name}}!"
    ).make_test_dir().add_test(
        "test_greeting.sql", None, "hello John!", ["John"]
    ).run_test_render_sql().assert_generated_tests(
        expected_sql
    )


def test_generates_multiple_test_expected_sql(app_runner, fs, em_project):
    hello_test = ExpectedSQLTestTemplate().render(
        template_name="hello", expected="hello Fred!", actual="hello Fred!"
    )
    bye_test = ExpectedSQLTestTemplate().render(
        template_name="bye", expected="bye Mark!", actual="bye Mark!"
    )
    expected_source = bye_test.add(hello_test)

    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "hello.sql", "hello {{name}}!"
    ).add_template("bye.sql", "bye {{name}}!").make_test_dir().add_test(
        "test_hello.sql", {"name": "Fred"}, "hello Fred!"
    ).add_test(
        "test_bye.sql", {"name": "Mark"}, "bye Mark!"
    ).run_test_render_sql().assert_generated_tests(
        expected_source
    )


def test_generates_single_test_expected_sql(app_runner, fs, em_project):

    expected_sql = ExpectedSQLTestTemplate().render(
        template_name="greeting", expected="hello John!", actual="hello John!"
    )
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "greeting.groovy", "hello John!"
    ).make_test_dir().add_test(
        "test_greeting.groovy", {}, "hello John!"
    ).run_test_render_sql().assert_generated_tests(
        expected_sql
    )


def test_generates_single_test_run_query(app_runner, fs, em_project):
    verb_test = RunOnDBTestTemplate().render(
        template_name="verb", query="select name from verb", emprj_path=em_project.root
    )

    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "verb.sql", "select {{column}} from verb"
    ).make_test_dir().add_test(
        "test_verb.sql", {"column": "name"}, "select name from verb"
    ).run_test_with_db().assert_generated_tests(
        verb_test
    )


def test_generates_all(app_runner, fs, em_project):
    check_sql = ExpectedSQLTestTemplate().render(
        template_name="verb",
        expected="select name from verb",
        actual="select name from verb",
    )
    run_on_db = RunOnDBTestTemplate().render(
        template_name="verb", query="select name from verb", emprj_path=em_project.root
    )
    expected_sql = check_sql.add(run_on_db)

    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "verb.sql", "select {{column}} from verb"
    ).make_test_dir().add_test(
        "test_verb.sql", {"column": "name"}, "select name from verb"
    ).run_test_all().assert_generated_tests(
        expected_sql
    )


def test_run_only_template(app_runner, fs, em_project):
    check_sql = ExpectedSQLTestTemplate().render(
        template_name="verb",
        expected="select name from verb",
        actual="select name from verb",
    )
    run_on_db = RunOnDBTestTemplate().render(
        template_name="verb", query="select name from verb", emprj_path=em_project.root
    )
    expected_sql = check_sql.add(run_on_db)

    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "verb.sql", "select {{column}} from verb"
    ).add_template("verb2.sql", "select {{column}} from verb").make_test_dir().add_test(
        "test_verb.sql", {"column": "name"}, "select name from verb"
    ).add_test(
        "test_verb2.sql", {"column": "id"}, "select name from verb"
    ).run_one_test(
        "test_verb.sql"
    ).assert_generated_tests(
        expected_sql
    )


def test_run_only_template_wrong_name_does_not_run_anything(app_runner, fs, em_project):
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "verb.sql", "select {{column}} from verb"
    ).add_template("verb2.sql", "select {{column}} from verb").make_test_dir().add_test(
        "test_verb.sql", {"column": "name"}, "select name from verb"
    ).add_test(
        "test_verb2.sql", {"column": "id"}, "select name from verb"
    ).run_one_test(
        "test_wrong_name.sql"
    ).generates_no_test()


# skip until we move test_context_values.yml inside library
@pytest.mark.skip
def test_runs_using_context_values_from_test_folder(app_runner, fs):
    data = {"_locale": "en-GB"}

    check_sql = ExpectedSQLTestTemplate().render(
        template_name="verb",
        expected="select name from verb where locale ='en-GB'",
        actual="select name from verb where locale ='en-GB'",
    )

    app_runner.with_emproject_under("/em/prj").and_prj_built_under(
        "/em/prj"
    ).add_template(
        "verb.sql", "select name from verb where locale ='{{_locale}}'"
    ).make_test_dir().with_test_context_values(
        data
    ).add_test(
        "test_verb.sql", {}, "select name from verb where locale ='en-GB'"
    ).run_test_render_sql().assert_generated_tests(
        check_sql
    )
