import os
import tempfile
from pathlib import Path

import pytest

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


# autouse allows to run this fixture even if we are not passing it to test
# this allow us to mock the DB connection
@pytest.fixture
def spy_os_system(mocker):
    # mocked = mocker.patch("sqltask.shell.prompt.SystemCmdRunner.execute")
    spy_os_system = mocker.spy(os, "system")
    yield spy_os_system


def test_when_printsql_select_template_with_edit_flag_runs_edit_configured_command(
    project_generator, library_generator, app_runner, spy_os_system
):
    text_to_print = "I am testing the edit command!!!!"
    project_generator.with_edit_cmd(f'echo "{text_to_print}"')
    library_generator.add_template("say_hello.txt", "hello!")

    app_runner.with_project(project_generator.generate())
    app_runner.edit_template("say_hello.txt").saveAndExit().print_sql()
    
    expected_cmd = f'echo "{text_to_print}"'
    spy_os_system.assert_called_once_with(expected_cmd)

