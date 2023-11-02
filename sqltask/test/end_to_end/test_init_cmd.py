import tempfile
from pathlib import Path

import pytest

from sqltask.app_project import AppProject
from sqltask.test.utils.app_runner.init import InitAppRunner
from sqltask.test.utils.project_generator import (QuickLibraryGenerator,
                                                  QuickProjectGenerator)

root = "/home/em/my_prj"


@pytest.fixture
def app_runner():
    app_runner = InitAppRunner()
    yield app_runner


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


def test_init_generates_config_and_sets_sqltask_lib_path(
    project_generator, library_generator, app_runner, root
):
    project_generator.clear_core_properties()
    project_generator.clear_library()  # remove pointing to library so it does generate file
    app_runner.with_project(project_generator.generate())
    library_generator.generate()  # creates library and set 'sqltask_task_lib' with valid library path
    properties = {
        "environment_name": "localtest",
        "sequence_generator": "svn",
        "project_prefix": "MP",
    }

    app_runner.with_properties(properties).with_properties(
        {"sqltask_task_lib": str(library_generator.root)}
    ).run()

    project = AppProject(project_generator.root)
    assert "localtest" == project.config["environment.name"]
    assert "svn" == project.config["sequence.generator"]
    assert "MP" == project.config["project.prefix"]
    assert "ad" == project.config["container.name"]  # defaults to ad
    assert "localhost" == project.config["machine.name"]  # default to localhost
    assert str(root / "library") == str(project.library().rootpath)


def test_init_when_files_exist_ask_for_confirmation(
    project_generator, library_generator, app_runner, root
):
    library_generator.override_root(root / "mylibrary")
    app_runner.with_project(project_generator.generate())
    properties = {
        "environment_name": "localtest",
        "sequence_generator": "svn",
        "project_prefix": "MP",
    }

    app_runner.confirm_save().with_properties(
        properties
    ).confirm_save().with_properties(
        {"sqltask_task_lib": str(root / "mylibrary")}
    ).run()

    project = AppProject(project_generator.root)
    assert "localtest" == project.config["environment.name"]  # computes localdev
    assert "svn" == project.config["sequence.generator"]  # computes localdev
    assert "ad" == project.config["container.name"]  # defaults to ad
    assert "localhost" == project.config["machine.name"]  # default to localhost
    assert str(root / "mylibrary") == str(project.library().rootpath)


def test_init_use_existing_empty_props_file(
    project_generator, library_generator, app_runner, root
):
    # removes properties
    project_generator.with_core_property("random.prop.so.it.creates.file", "4")
    project_generator.with_project_prefix(None)
    project_generator.with_environment_name(None)
    project_generator.with_sequence_generator(None)
    library_generator.override_root(root / "mylibrary")
    app_runner.with_project(project_generator.generate())

    properties = {
        "environment_name": "localtest",
        "sequence_generator": "svn",
        "project_prefix": "MP",
    }

    app_runner.confirm_save().with_properties(
        properties
    ).confirm_save().with_properties(
        {"sqltask_task_lib": str(root / "mylibrary")}
    ).run()

    project = AppProject(project_generator.root)
    assert "localtest" == project.config["environment.name"]  # computes localdev
    assert "svn" == project.config["sequence.generator"]  # computes localdev
    assert "ad" == project.config["container.name"]  # defaults to ad
    assert "localhost" == project.config["machine.name"]  # default to localhost
    assert str(root / "mylibrary") == str(project.library().rootpath)
