import tempfile
from pathlib import Path

import pytest

from sql_gen.commands.verify_templates_cmd import (ExpectedSQLTestTemplate,
                                                   RunOnDBTestTemplate)
from sql_gen.test.utils.app_runner import TemplatesAppRunner
from sql_gen.test.utils.project_generator import (QuickLibraryGenerator,
                                                  QuickProjectGenerator)


@pytest.fixture
def app_runner(capsys):
    app_runner = TemplatesAppRunner(capsys=capsys)
    yield app_runner
    app_runner.teardown()


# autouse allows to run this fixture even if we are not passing to test
@pytest.fixture(autouse=True)
def fake_pytest(mocker):
    make_pytest = mocker.patch("ccdev.command_factory.CommandFactory.make_pytest")
    yield make_pytest


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


def test_expects_test_folder_to_be_next_to_templates_folder_and_fails_if_not_exists(
    project_generator, app_runner
):
    app_runner.with_project(project_generator.generate())

    app_runner.saveAndExit().test_sql()
    expected = "library/test_templates' does not exist.\n"
    app_runner.assert_message_printed(expected)


@pytest.mark.skip
def test_test_name_not_matching_template_generates_unable_to_find_template_test(
    project_generator, library_generator, app_runner
):
    library_generator.add_template()
    app_runner.with_project(project_generator.generate())
    app_runner.saveAndExit().test_sql()
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


def test_groovy_extension_does_generate_run_on_db(
    project_generator, library_generator, app_runner
):
    expected_sql = ExpectedSQLTestTemplate().render(
        template_name="greeting", expected="hello John!", actual="hello John!"
    )
    library_generator.add_template("greeting.groovy", "hello John!").add_test(
        "test_greeting.groovy", "hello John!"
    )
    app_runner.with_project(project_generator.generate())
    app_runner.saveAndExit().test_sql().assert_generated_tests(expected_sql)


def test_testname_not_sql_ext_does_not_run(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("greeting.sqls", "hello John!").add_test(
        "test_greeting.sqls", "hello John!"
    )
    app_runner.with_project(project_generator.generate())
    app_runner.saveAndExit().test_sql().generates_no_test()


def test_render_sql_with_test_passing_list_params(
    project_generator, library_generator, app_runner
):
    expected_sql = ExpectedSQLTestTemplate().render(
        template_name="greeting", expected="hello John!", actual="hello John!"
    )

    template_content = '--["John"]\nhello John!'
    library_generator.add_template("greeting.sql", "hello {{name}}!").add_test(
        "test_greeting.sql", template_content
    )
    app_runner.with_project(project_generator.generate())
    app_runner.run_test_render_sql().assert_generated_tests(expected_sql)


def test_render_sql_generates_multiple_testexpected_sql(
    project_generator, library_generator, app_runner
):
    hello_test = ExpectedSQLTestTemplate().render(
        template_name="hello", expected="hello Fred!", actual="hello Fred!"
    )
    bye_test = ExpectedSQLTestTemplate().render(
        template_name="bye", expected="bye Mark!", actual="bye Mark!"
    )
    expected_source = bye_test.add(hello_test)

    library_generator.add_template("hello.sql", "hello {{name}}!").add_test(
        "test_hello.sql", '--{"name":"Fred"}\nhello Fred!'
    ).add_template("bye.sql", "bye {{name}}!").add_test(
        "test_bye.sql", '--{"name":"Mark"}\nbye Mark!'
    )
    app_runner.with_project(project_generator.generate())
    app_runner.run_test_render_sql().assert_generated_tests(expected_source)


def test_generates_single_test_run_query(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("verb.sql", "select {{column}} from verb").add_test(
        "test_verb.sql", '--{"column":"name"}\nselect name from verb'
    )
    project = project_generator.generate()

    verb_test = RunOnDBTestTemplate().render(
        template_name="verb", query="select name from verb", emprj_path=project.emroot
    )

    app_runner.with_project(project)
    app_runner.run_test_with_db().assert_generated_tests(verb_test)


def test_generates_all(project_generator, library_generator, app_runner):
    library_generator.add_template("verb.sql", "select {{column}} from verb").add_test(
        "test_verb.sql", '--{"column":"name"}\nselect name from verb'
    )
    project = project_generator.generate()
    check_sql = ExpectedSQLTestTemplate().render(
        template_name="verb",
        expected="select name from verb",
        actual="select name from verb",
    )
    run_on_db = RunOnDBTestTemplate().render(
        template_name="verb", query="select name from verb", emprj_path=project.emroot
    )
    expected_source = check_sql.add(run_on_db)

    app_runner.with_project(project)
    app_runner.run_test_all().assert_generated_tests(expected_source)


def test_run_only_template(project_generator, library_generator, app_runner):
    library_generator.add_template("verb.sql", "select {{column}} from verb").add_test(
        "test_verb.sql", '--{"column":"name"}\nselect name from verb'
    ).add_template("verb2.sql", "select {{column}} from verb2").add_test(
        "test_verb2.sql", '--{"column":"name"}\nselect name from verb2'
    )

    project = project_generator.generate()
    check_sql = ExpectedSQLTestTemplate().render(
        template_name="verb",
        expected="select name from verb",
        actual="select name from verb",
    )
    run_on_db = RunOnDBTestTemplate().render(
        template_name="verb", query="select name from verb", emprj_path=project.emroot
    )
    expected_source = check_sql.add(run_on_db)

    app_runner.with_project(project)
    app_runner.run_one_test("test_verb.sql").assert_generated_tests(expected_source)


def test_run_only_template_wrong_name_does_not_run_anything(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("verb.sql", "select {{column}} from verb").add_test(
        "test_verb.sql", '--{"column":"name"}\nselect name from verb'
    ).add_template("verb2.sql", "select {{column}} from verb2").add_test(
        "test_verb2.sql", '--{"column":"name"}\nselect name from verb2'
    )

    app_runner.with_project(project_generator.generate()).run_one_test(
        "test_wrong_name.sql"
    ).generates_no_test()


def test_runs_using_context_values_from_library(
    project_generator, library_generator, app_runner
):
    check_sql = ExpectedSQLTestTemplate().render(
        template_name="verb",
        expected="select name from verb where locale='en-GB'",
        actual="select name from verb where locale='en-GB'",
    )

    data = {"_locale": "en-GB"}
    library_generator.add_template(
        "verb.sql", "select name from verb where locale='{{_locale}}'"
    ).add_test(
        "test_verb.sql", "select name from verb where locale='en-GB'"
    ).with_test_context_values(
        data
    )
    app_runner.with_project(project_generator.generate())
    app_runner.run_test_render_sql().assert_generated_tests(check_sql)
