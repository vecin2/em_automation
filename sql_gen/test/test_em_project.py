import pytest
import os
from sql_gen.emproject import EMProject, emproject_home


def test_fs_example(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_computes_project_prefix_from_em_core_home(fs):
    repo_modules =emproject_home()+"/repository/default"
    print("repo_modules is: "+ repo_modules)
    spen_core_entities= repo_modules+ "/SPENCoreEntities/"
    fs.create_dir(spen_core_entities)
    em_project = EMProject()

    assert "SPEN" == EMProject.prefix()

def test_computes_project_prefix_throws_exc_if_not_repo_modules_created(fs):
    with pytest.raises(ValueError) as excinfo:
        em_project = EMProject()
        EMProject.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_computes_project_prefix_throws_exc_if_not_custom_module_created(fs):
    repo_modules =emproject_home()+"/repository/default"
    fs.create_dir(repo_modules)
    with pytest.raises(ValueError) as excinfo:
        em_project = EMProject()
        EMProject.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_computes_project_prefix_only_when_module_start_at_least_with_3_uppercase(fs):
    repo_modules =emproject_home()+"/repository/default"
    other_module= repo_modules+ "/otherModule/"
    fs.create_dir(other_module)
    spen_core_entities= repo_modules+ "/SPENCoreEntities/"
    fs.create_dir(spen_core_entities)
    assert "SPEN" == EMProject.prefix()

