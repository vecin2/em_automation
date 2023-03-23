import pytest

from sql_gen.test.utils.app_runner import PrintSQLToConsoleAppRunner
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder


@pytest.fixture
def app_runner(fs):
    app_runner = PrintSQLToConsoleAppRunner(fs=fs)
    yield app_runner
    app_runner.teardown()


@pytest.fixture
def project_builder(fs):
    em_root = "/fake/em/projects/my_project"
    yield FakeEMProjectBuilder(fs, root=em_root)


@pytest.fixture
def em_project(fs, project_builder):
    em_project = project_builder.base_setup().build()
    yield em_project


def test_it_throws_exception_when_no_templates_path_define(app_runner, em_project):
    with pytest.raises(ValueError) as excinfo:
        app_runner.with_emproject(em_project).print_sql()
    assert "'sqltask.library.path' not set" in str(excinfo.value)


def test_it_throws_exception_when_templates_path_points_to_non_existing_folder(
    app_runner, em_project, project_builder
):
    project_builder.append_to_app_config("sqltask.library.path=/non/existing/path")
    with pytest.raises(ValueError) as excinfo:
        app_runner.with_emproject(em_project).print_sql()
    assert "sqltask.library.path' points to an invalid path" in str(excinfo.value)


def test_returns_empty_when_no_template_selected(app_runner, em_project, fs):
    app_runner.with_emproject(em_project).with_task_library(
        "/library"
    ).saveAndExit().print_sql().assert_printed_sql("")


def test_keeps_prompting_after_entering_non_existing_template(
    app_runner, em_project, fs
):

    app_runner.with_emproject(em_project).with_task_library("/library").select_template(
        "abc", {}
    ).saveAndExit().print_sql().assert_printed_sql("").assert_all_input_was_read()


def test_prints_expected_text_when_a_valid_template_is_run(app_runner, em_project, fs):
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "say_hello.txt", "hello!"
    ).select_template(
        "1. say_hello.txt", {}
    ).saveAndExit().print_sql().assert_printed_sql(
        "hello!"
    ).assert_all_input_was_read()


def test_prints_expected_text_when_a_valid_template_with_placeholders_is_run(
    app_runner, em_project, fs
):
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "say_hello.txt", "hello {{name}}"
    ).select_template(
        "1. say_hello.txt", {"name": "David"}
    ).saveAndExit().print_sql().assert_printed_sql(
        "hello David"
    )


def test_prints_expected_text_when_user_goes_back_select_a_different_value(
    app_runner, em_project, fs
):
    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "greeting.txt", "hello {{name}} {{surname}}!"
    ).select_template(
        "1. greeting.txt", ["David", "<", "Juan", "Rodriguez"]
    ).saveAndExit().print_sql().assert_printed_sql(
        "hello Juan Rodriguez!"
    )


def test_fills_two_templates_and_combines_output(app_runner, em_project, fs):

    app_runner.with_emproject(em_project).with_task_library("/library").add_template(
        "hello.txt", "hello {{name}}"
    ).add_template("bye.txt", "bye {{name}}").select_template(
        "hello.txt", {"name": "David"}
    ).select_template(
        "bye.txt", {"name": "John"}
    ).saveAndExit().print_sql().assert_printed_sql(
        "hello David\nbye John"
    )


@pytest.mark.skip
def test_initial_context_is_used_when_filling_template(app_runner, fs):
    initial_context = {"_dummy_note": "Dummy note"}
    fs.create_file("/templates/hello.sql", contents="hello {{_dummy_note}}!")

    app_runner.with_task_library("/library").with_template_API(
        initial_context
    ).select_template(
        "hello.sql", {"dummy": "hello"}
    ).saveAndExit().run().assert_rendered_sql(
        "hello Dummy note!"
    ).assert_all_input_was_read()
