import pytest

from devtask.repository import (
    InvalidCedObject,
    Repository,
    UndefinedClassException,
    InvalidClassException,
)
from devtask.test.utils.temp_folder import tempfolder
from devtask.object_factory import new_process_def

product_path = tempfolder / "product"
project_path = tempfolder / "project"
repository = Repository(product_path, project_path)


def test_load_class_throws_exception_when_class_not_found():
    with pytest.raises(UndefinedClassException):
        repository.load("PCCustomer.Implementation.NonExistingObject")


def test_load_class_throws_exception_when_class_is_invalid():
    classpath = "PCCustomer.Implementation.InvalidObject"
    invalid_object = InvalidCedObject(classpath)
    repository.save(invalid_object)

    with pytest.raises(InvalidClassException):
        invalid_object = repository.load(classpath)


@pytest.mark.skip
def test_loads_gtprocess():
    classpath = "PCCustomer.Implementation.Process.SearchCustomer.xml"
    repository.add_to_project(new_process_def(classpath, "Hello"))

    result = repository.load(classpath)
    assert "ced.repository.ProcessDefintion" == result
