import tempfile
from pathlib import Path

import pytest

from sql_gen.emproject import EMProject
from sql_gen.emproject.config import EMConfigID
from sql_gen.test.utils.emproject_test_util import FakeEMProjectBuilder
from sql_gen.test.utils.project_generator import QuickProjectGenerator


def prj_builder(fs, root="/home/em"):
    return FakeEMProjectBuilder(fs, root)


def make_valid_em_folder_layout(fs, root):
    return FakeEMProjectBuilder(fs, root).make_valid_em_folder_layout()


local_config_id = EMConfigID("localdev", "localhost", "ad")


@pytest.mark.skip
def test_project_prefix_computes_when_exist_a_minimum_of_modules(fs):
    em_project = (
        prj_builder(fs)
        .add_repo_module("PCCoreEntities")
        .add_repo_module("PCContactHistory")
        .add_config(local_config_id, "")
        .build()
    )
    em_project.set_default_config_id(local_config_id)
    assert "PC" == em_project.prefix()


@pytest.mark.skip
def test_project_prefix_returns_empty_if_not_enough_prj_modules(fs):
    em_project = (
        prj_builder(fs)
        .add_repo_module("CAI")
        .add_repo_module("IMAP")
        .add_repo_module("SPENCoreEntities")
        .build()
    )
    assert "" == em_project.prefix()


@pytest.mark.skip
def test_project_prefix_empty_if_not_repo_modules_created(fs):
    em_project = prj_builder(fs).build()
    assert "" == em_project.prefix()


@pytest.mark.skip
def test_project_prefix_empty_if_no_module_with_2_uppercase(fs):
    em_project = prj_builder(fs).add_repo_module("Other").build()
    assert "" == em_project.prefix()


@pytest.mark.skip
def test_project_prefix_empty_if_not_custom_module_created(fs):
    em_project = prj_builder(fs).add_repo_module("").build()
    assert "" == em_project.prefix()


@pytest.mark.skip
def test_project_prefix_skip_modules_without_3_uppercase(fs):
    em_project = (
        prj_builder(fs)
        .add_repo_module("otherModule")
        .add_repo_module("SPENCoreEntities")
        .add_repo_module("SPENContactHistory")
        .build()
    )
    assert "SPEN" == em_project.prefix()


@pytest.mark.skip
def test_project_prefix_in_config_overrides_computation(fs):
    em_project = (
        FakeEMProjectBuilder(fs)
        .add_repo_module("SPENCoreEntities")
        .add_repo_module("SPENContactHistory")
        .add_config(local_config_id, "project.prefix=GSC")
        .build()
    )
    em_project.set_default_config_id(local_config_id)
    assert "GSC" == em_project.prefix()


def make_emproject(root):
    return EMProject(emprj_path=root)


@pytest.fixture
def root():
    with tempfile.TemporaryDirectory() as root:
        yield Path(root)


@pytest.fixture
def project_generator(root):
    quick_generator = QuickProjectGenerator(root / "trunk")
    yield quick_generator.make_project_generator()


def test_product_layout(project_generator):
    project_generator.with_product_home("/products/my_product")
    project = project_generator.generate()
    assert "/products/my_product" == project.product_layout().root
