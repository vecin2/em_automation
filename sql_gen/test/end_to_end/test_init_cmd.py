import tempfile
from pathlib import Path

import pytest

from sql_gen.test.utils.app_runner.init import InitAppRunner
from sql_gen.test.utils.project_generator import ProjectGenerator

root = "/home/em/my_prj"


@pytest.fixture
def root():
    with tempfile.TemporaryDirectory() as root:
        yield Path(root)


@pytest.fixture
def app_runner():
    app_runner = InitAppRunner()
    yield app_runner


@pytest.fixture
def project_generator(root):
    project_generator = ProjectGenerator(root / "trunk")
    project_generator.add_folder("bin")
    project_generator.add_folder("config")
    project_generator.add_folder("components")
    project_generator.add_folder("repository")
    yield project_generator


@pytest.mark.skip
def test_init_creates_sqltask_config_under_current_em_project(
    project_generator, app_runner
):
    app_runner.with_emproject_home(project_generator.generate().emroot)
    # prjbuilder = prj_builder(fs)
    # prjbuilder.add_config_environment("localdev")
    # prjbuilder.add_config_environment("test")
    # prjbuilder.add_config_environment("prod")

    app_runner.init()

    # config = app_runner.appconfig()
    # assert "localdev" == config["environment.name"]  # computes localdev
    # assert "ad" == config["container.name"]  # defaults to ad
    # assert "localhost" == config["machine.name"]  # default to localhost
    # assert "svn" == config["sequence.generator"]
