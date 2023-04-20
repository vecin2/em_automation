import os

import pytest

from sql_gen.test.utils.emproject_test_util import (FakeCCAdminClient,
                                                    FakeEMProjectBuilder)
from sql_gen.test.utils.init_runner import InitAppRunner


root = "/home/em/my_prj"


@pytest.fixture
def app_runner():
    app_runner = InitAppRunner()
    app_runner.with_emproject_home(root)
    yield app_runner
    # app_runner.teardown()


def prj_builder(fs):
    prjbuilder = FakeEMProjectBuilder(fs, root)
    prjbuilder.make_valid_em_folder_layout()
    os.chdir(root)
    return prjbuilder


@pytest.mark.skip
def test_init_creates_sqltask_config_under_current_em_project(fs, app_runner):
    prjbuilder = prj_builder(fs)
    prjbuilder.add_config_environment("localdev")
    prjbuilder.add_config_environment("test")
    prjbuilder.add_config_environment("prod")

    app_runner.init()

    config = app_runner.appconfig()
    assert "localdev" == config["environment.name"]  # computes localdev
    assert "ad" == config["container.name"]  # defaults to ad
    assert "localhost" == config["machine.name"]  # default to localhost
    assert "svn" == config["sequence.generator"]
