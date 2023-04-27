import tempfile
from pathlib import Path

import pytest

from sqltask.test.utils.project_generator import (LibraryGenerator,
                                                  ProjectGenerator)


@pytest.fixture
def root():
    with tempfile.TemporaryDirectory() as root:
        yield Path(root)


@pytest.fixture
def project_generator(root):
    project_generator = ProjectGenerator(root / "trunk")
    yield project_generator


@pytest.fixture
def library_generator(root):
    library_generator = LibraryGenerator(root / "library")
    yield library_generator


def test_instantiate_ad_queryrunner(project_generator, library_generator):
    ad_queries = {"v_names__by_ed": "SELECT * FROM verb_name WHERE NAME='{}'"}
    library_generator.with_ad_queries(ad_queries)
    project_generator.with_library(library_generator)

    project_generator.with_db_type("oracle")
    project_generator.with_environment_name("localdev")
    project_generator.with_ad_connection_details(
        host="localhost", port="1433", user="sa", password="admin!"
    )
    project = project_generator.generate()
    assert (
        ad_queries["v_names__by_ed"]
        == project.ad_queryrunner.query_dict["v_names__by_ed"]
    )


def test_product_layout(project_generator):
    project_generator.with_environment_name("localdev")
    project_generator.with_product_home("/products/my_product")
    project = project_generator.generate()
    assert "/products/my_product" == project.product_layout().root
