import pytest
import os
from sql_gen.emproject import current_emproject as EMProject
from sql_gen.emproject import emproject_home


#from sql_gen.emproject import emproject_home,EMProject
class FakeEMProjectBuilder():
    REPO_PATH="repository/default"

    def __init__(self, fs, root="/home/em"):
        self.fs =fs
        self.root = root

    def add_repo_module(self, module_name):
        if not self._exists(self.REPO_PATH):
            self._create_dir(self.REPO_PATH)
        if module_name:
            self._create_dir(self.REPO_PATH+"/"+module_name+"/")
        return self

    def _exists(self,prj_relative_path):
        return os.path.exists(self._abs_path(prj_relative_path))

    def _create_dir(self,prj_relative_path):
        return self.fs.create_dir(self._abs_path(prj_relative_path))

    def _abs_path(self, prj_relative_path):
        return os.path.join(self.root, prj_relative_path)

    def build(self):
        self._create_dir("work/config/show-config-txt")
        return EMProject(self.root)

def prj_builder(fs, root='/home/em'):
    return FakeEMProjectBuilder(fs,root)

def test_fs_example(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_fs_create_same_file_does_not_through_duplicate_exc(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_computes_project_prefix_from_em_core_home(fs):
    em_project = prj_builder(fs).add_repo_module("SPENCoreEntities")\
                            .build()
    assert "SPEN" == em_project.prefix()

def test_computes_project_prefix_throws_exc_if_not_repo_modules_created(fs):
    with pytest.raises(ValueError) as excinfo:
        em_project = prj_builder(fs).build()
        em_project.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_computes_project_prefix_throws_exc_if_no_module_with_3_uppercase(fs):
    with pytest.raises(ValueError) as excinfo:
        em_project = prj_builder(fs).add_repo_module("other").build()
        em_project.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_computes_project_prefix_throws_exc_if_not_custom_module_created(fs):
    em_project = prj_builder(fs).add_repo_module("").build()
    with pytest.raises(ValueError) as excinfo:
        em_project.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_computes_project_prefix_skip_modules_without_3_uppercase(fs):
    em_project = prj_builder(fs).add_repo_module("otherModule")\
                                .add_repo_module("SPENCoreEntities")\
                                .build()
    assert "SPEN" == em_project.prefix()

def test_config(fs):
    fs.create_dir("/dd")
    #em_project = FakeEMProjectBuilder.make(fs).build()
    #config = em_project.config()
    #assert "sa" == config["database.host"]

