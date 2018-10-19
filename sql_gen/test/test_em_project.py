import pytest
import os
from sql_gen.emproject import EMProject
from sql_gen.emproject import emproject_home

class FakeCCAdminClient (object):
    show_config_content=""
    fake_emproject_builder = None

    def show_config(self):
        self.fake_emproject_builder.add_config(self.show_config_content)


#from sql_gen.emproject import emproject_home,EMProject
class FakeEMProjectBuilder():
    REPO_PATH="repository/default"

    def __init__(self,
                 fs,
                 root="/home/em",
                 env_name="localdev",
                 machine_name="localhost",
                 container_name="ad"):
        self.fs =fs
        self.root = root
        self.ccadmin_client =FakeCCAdminClient()
        self.ccadmin_client.fake_emproject_builder=self
        self.emproject =EMProject(self.root,self.ccadmin_client)
        self._add_emautomation_config(env_name=env_name,
                                      machine_name=machine_name,
                                      container_name=container_name)

    def _add_emautomation_config(self,
                                 env_name,
                                 machine_name,
                                  container_name):
        config_content=\
            "emautomation.environment.name="+env_name+\
            "\nemautomation.container.name="+container_name+\
            "\nemautomation.machine.name="+machine_name

        self._create_file("config/local.properties",config_content)
        return self

    def add_config(self, config_content):
        self._create_file(self.emproject.config_path(),\
                            contents=config_content)
        return self
    def with_ccadmin(self, ccadmin_client):
        self.ccadmin_client = ccadmin_client
        self.ccadmin_client.fake_emproject_builder=self
        self.emproject.ccadmin_client =self.ccadmin_client
        return self

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

    def _create_file(self,prj_relative_path,contents):
        return self.fs.create_file(self._abs_path(prj_relative_path),\
                                    contents=contents)

    def _abs_path(self, prj_relative_path):
        return os.path.join(self.root, prj_relative_path)

    def build(self):
        return self.emproject

def prj_builder(fs, root='/home/em'):
    return FakeEMProjectBuilder(fs,root)

def test_fs_example(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_fs_create_file_with_content(fs):
    fs.create_file('/var/data/xx1.txt',contents='hello')
    assert os.path.exists('/var/data/xx1.txt')
    with open('/var/data/xx1.txt') as f:
        assert "hello" == f.read()

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

def test_config_return_dict_containing_all_properties(fs):
    emautomation_config_content="""\n
emautomation.environment.name=local
emautomation.container.name=ad
emautomation.machine.name=localhost
"""
    config_content="""\n
database.admin.user=ad
database.user=sa
"""
    em_project = FakeEMProjectBuilder(fs)\
                        .add_config(config_content)\
                        .build()

    config = em_project.config()
    assert "ad" == config['database.admin.user']
    assert "sa" == config['database.user']

def test_config_path_depends_on_container_machine_and_env_names(fs):
    em_project  = FakeEMProjectBuilder(fs,
                                       env_name="mylocal",
                                       container_name="ad",
                                       machine_name="localhost")\
                                      .build()
    assert "work/config/show-config-txt/mylocal-localhost-ad.txt" ==em_project.config_path()

def test_config_generates_config_first_time(fs):
    ccadmin_client=FakeCCAdminClient()
    ccadmin_client.show_config_content="database.admin.user=ad"
    em_project  = FakeEMProjectBuilder(fs)\
                    .with_ccadmin(ccadmin_client)\
                                          .build()
    config = em_project.config()

    assert "ad" == config['database.admin.user']

