import os
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


def test_it_throws_exception_when_run_outside_em_project(app_runner, root):
    app_runner.with_project(AppProject(root))

    with pytest.raises(ValueError) as excinfo:
        app_runner.print_sql()
    assert (
        "This command should be run from a root EM project folder or any of the subfolders"
        in str(excinfo.value)
    )


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
    assert "'.library' points to an invalid path '/sfa" in str(excinfo.value)


def test_returns_empty_when_no_template_selected(project_generator, app_runner):
    app_runner.with_project(project_generator.generate())
    app_runner.saveAndExit().print_sql().assert_printed_sql("")


def test_keeps_prompting_until_max_retrials_when_entering_non_existing_template(
    project_generator, app_runner
):
    # default max no of trials is 10
    app_runner.with_project(project_generator.generate())
    for iter in range(0, 3):
        app_runner.confirm()
    for iter in range(0, 3):
        app_runner.select_template("abc")
    for iter in range(0, 5):
        app_runner.select_template(
            "abc with some spaces should also be handle gracefully"
        )
    # should exit and dont remain blocked
    try:
        app_runner.saveAndExit().print_sql()
        assert (
            False
        ), "A ValueError should have been raised due to Valid attemps execedeed to select a valid option "
    except ValueError as excinfo:
        assert "Attempts to select a valid option exceeded." == str(excinfo)


def test_correct_input_resets_no_of_trials(
    library_generator, project_generator, app_runner
):
    library_generator.add_template("say_hi.txt", "hi!")
    # default max no of trials is 10
    app_runner.with_project(project_generator.generate())
    for iter in range(0, 10):
        app_runner.select_template("abc")

    app_runner.select_template("say_hi.txt").select_template(
        "abc"
    ).saveAndExit().print_sql()

    assert True  # should not though exception


def test_prints_and_adds_to_system_clipboard_expected_text_when_a_valid_template_is_run(
    project_generator, library_generator, app_runner
):
    library_generator.add_template("say_hello.txt", "hello!")

    app_runner.with_project(project_generator.generate())
    app_runner.select_template(
        "say_hello.txt"
    ).confirm().saveAndExit().print_sql().assert_printed_sql(
        "hello!"
    ).assert_clipboard_content(
        "hello!"
    )


def test_prints_expected_text_when_a_valid_template_with_placeholders_is_run(
    project_generator, library_generator, app_runner
):
    project_generator.with_product_home(
        "some/path/for/product/so/codepath/filter/works"
    )
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


@pytest.fixture
def spy_os_system(mocker):
    spy_os_system = mocker.spy(os, "system")
    yield spy_os_system


def test_when_printsql_select_template_with_edit_flag_keeps_selection_and_runs_edit_configured_command(
    project_generator, library_generator, app_runner, spy_os_system
):
    text_to_print = "I am testing the edit command!!!!"
    project_generator.with_edit_cmd(f'echo "{text_to_print}"')
    library_generator.add_template("say_hello.txt", "hello!")

    app_runner.with_project(project_generator.generate())
    app_runner.edit_template(
        "say_hello.txt"
    ).confirm().saveAndExit().print_sql().assert_printed_sql(
        "hello!"
    ).assert_clipboard_content(
        "hello!"
    )

    expected_cmd = f'echo "{text_to_print}"'
    spy_os_system.assert_called_once_with(expected_cmd)


def test_when_printsql_without_edit_cmd_configured_then_select_template_with_edit_flag_is_ignored_until_flag_is_removed(
    project_generator, library_generator, app_runner, spy_os_system
):
    project_generator.with_edit_cmd(None)
    library_generator.add_template("say_hello.txt", "hello!")

    app_runner.with_project(project_generator.generate())
    # confirm after edit, keeps the name of the template as default
    app_runner.edit_template(
        "say_hello.txt"
    ).confirm().saveAndExit().print_sql().assert_printed_sql(
        "hello!"
    ).assert_clipboard_content(
        "hello!"
    )

    spy_os_system.assert_not_called()


class FakeGit:
    def __init__(self, remote_origin_url, branch):
        self._remote_origin_url = remote_origin_url
        self._branch = branch

    def remote_origin_url(self):
        return self._remote_origin_url

    def show_current_branch(self):
        return self._branch


@pytest.fixture(autouse=True)
def git(mocker):
    mocked = mocker.patch("sqltask.shell.prompt.ViewTemplateDocsAction.make_git")
    mocked.return_value = FakeGit(
        "git@github.com-verint:verint-CME/sqltask-library.git", "master"
    )
    yield mocked


def test_when_printsql_select_template_with_docs_flag_keeps_selection_and_runs_docs_configured_command(
    project_generator, library_generator, app_runner, spy_os_system, git
):
    expected_url_to_open = "https://github.com/verint-CME/sqltask-library/tree/master/docs/LibraryByFolder.md#say-hello"
    project_generator.with_docs_cmd("google")
    library_generator.add_template("say_hello.txt", "hello!")

    app_runner.with_project(project_generator.generate())
    app_runner.docs_template(
        "say_hello.txt"
    ).confirm().saveAndExit().print_sql().assert_printed_sql(
        "hello!"
    ).assert_clipboard_content(
        "hello!"
    )
    spy_os_system.assert_called_once_with(f"google {expected_url_to_open}")
