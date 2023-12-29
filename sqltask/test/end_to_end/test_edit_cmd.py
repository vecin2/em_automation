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
