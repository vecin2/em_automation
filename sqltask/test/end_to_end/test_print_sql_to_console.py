import tempfile
from pathlib import Path

import pytest

from sqltask.app_project import AppProject
from sqltask.test.utils.app_runner import PrintSQLToConsoleAppRunner
from sqltask.test.utils.project_generator import (QuickLibraryGenerator,
                                                  QuickProjectGenerator)


@pytest.fixture
def app_runner():
    app_runner = PrintSQLToConsoleAppRunner()
    yield app_runner
    app_runner.teardown()


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


def test_it_throws_exception_when_run_outside_em_project(app_runner,root):
    app_runner.with_project(AppProject(root))

    with pytest.raises(ValueError) as excinfo:
        app_runner.print_sql()
    assert "This command should be run from a root EM project folder or any of the subfolders" in str(excinfo.value)


def test_it_throws_exception_when_no_templates_path_define(
    project_generator, app_runner
):
    project_generator.clear_library()
    app_runner.with_project(project_generator.generate())

    with pytest.raises(ValueError) as excinfo:
        app_runner.saveAndExit().print_sql()
    assert "Library path not set for current project." in str(excinfo.value)


def test_it_throws_exception_when_templates_path_points_to_non_existing_folder(
    project_generator, library_generator, app_runner
):
    project_generator.with_library_path("/sfadasfd/asdfsad/asdf")
    app_runner.with_project(project_generator.generate())

    with pytest.raises(ValueError) as excinfo:
        app_runner.saveAndExit().print_sql()
    assert "'.library' points to an invalid path '/sfa" in str(
        excinfo.value
    )


def test_returns_empty_when_no_template_selected(project_generator, app_runner):
    app_runner.with_project(project_generator.generate())
    app_runner.saveAndExit().print_sql().assert_printed_sql("")


def test_keeps_prompting_after_entering_non_existing_template(
    project_generator, app_runner
):
    app_runner.with_project(project_generator.generate())
    app_runner.select_template("abc").saveAndExit().print_sql().assert_printed_sql("")


def test_prints_expected_text_when_a_valid_template_without_placeholders_is_run(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("say_hello.txt", "hello!")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "say_hello.txt"
    ).saveAndExit().print_sql().assert_printed_sql("hello!")


def test_prints_expected_text_when_a_valid_template_with_placeholders_is_run(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("say_hello.txt", "hello {{name | codepath()}}!")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "say_hello.txt", {"name": "Tony"}
    ).saveAndExit().print_sql().assert_printed_sql("hello Tony!")


def test_prints_expected_text_when_user_goes_back_select_a_different_value(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("say_hello.txt", "hello {{name}} {{surname}}!")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "say_hello.txt", ["Tony", "<", "Antonio", "Rodriguez"]
    ).saveAndExit().print_sql().assert_printed_sql("hello Antonio Rodriguez!")


def test_fills_two_templates_and_combines_output(
    project_generator, library_generator, app_runner
):

    library_generator.add_template("say_hi.txt", "hi {{name}}")
    library_generator.add_template("say_bye.txt", "bye {{name}}")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template("say_hi.txt", {"name": "Marco"}).select_template(
        "say_bye.txt", {"name": "Fernando"}
    ).saveAndExit().print_sql().assert_printed_sql("hi Marco\nbye Fernando")


# @pytest.mark.skip
# def test_initial_context_is_used_when_filling_template(app_runner, fs):
#     initial_context = {"_dummy_note": "Dummy note"}
#     fs.create_file("/templates/hello.sql", contents="hello {{_dummy_note}}!")
#
#     app_runner.with_task_library("/library").with_template_API(
#         initial_context
#     ).select_template(
#         "hello.sql", {"dummy": "hello"}
#     ).saveAndExit().run().assert_rendered_sql(
#         "hello Dummy note!"
#     ).assert_all_input_was_read()
