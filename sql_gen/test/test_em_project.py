import pytest
import os
from sql_gen.emproject import EMProject, EMConfigID
from sql_gen.exceptions import ConfigFileNotFoundException,ConfigPropNotFoundException,NoDefaultEnvFoundException,ConfigException
from sql_gen.test.utils.emproject_test_util import FakeCCAdminClient,FakeEMProjectBuilder

def prj_builder(fs, root='/home/em'):
    return FakeEMProjectBuilder(fs,root)

@pytest.mark.skip
def test_config_throws_exception_if_no_default_env_passed():
    with pytest.raises(NoDefaultEnvFoundException) as excinfo:
        emproject = EMProject('/home/em')
        emproject.config()
    assert "Default environment not set" in excinfo.value

def test_project_prefix_from_em_core_home(fs):
    em_project = prj_builder(fs).add_repo_module("SPENCoreEntities")\
                            .build()
    assert "SPEN" == em_project.prefix()

def test_project_prefix_throws_exc_if_not_repo_modules_created(fs):
    with pytest.raises(ValueError) as excinfo:
        em_project = prj_builder(fs).build()
        em_project.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_project_prefix_throws_exc_if_no_module_with_3_uppercase(fs):
    with pytest.raises(ValueError) as excinfo:
        em_project = prj_builder(fs).add_repo_module("other").build()
        em_project.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_project_prefix_throws_exc_if_not_custom_module_created(fs):
    em_project = prj_builder(fs).add_repo_module("").build()
    with pytest.raises(ValueError) as excinfo:
        em_project.prefix()
        assert False, "should have through an ValueError exception"
    assert "compute project prefix" in str(excinfo.value)

def test_project_prefix_skip_modules_without_3_uppercase(fs):
    em_project = prj_builder(fs).add_repo_module("otherModule")\
                                .add_repo_module("SPENCoreEntities")\
                                .build()
    assert "SPEN" == em_project.prefix()

local_config_id=EMConfigID("localdev",
                           "localhost",
                           "ad")

def test_config_path_depends_on_config_id(fs):
    em_project = EMProject("/home/project")
    mylocal_config_id=EMConfigID("mylocal","localhost","ad")
    assert "work/config/show-config-txt/mylocal-localhost-ad.txt" ==em_project.config_path(mylocal_config_id)

def test_returns_config_without_invoke_ccadmin_if_config_exist(fs):
    config_content="""\n
database.admin.user=ad
database.user=sa
"""
    em_project = FakeEMProjectBuilder(fs)\
                        .add_config(local_config_id,
                                    config_content)\
                        .build()

    config = em_project.config(local_config_id)
    assert "ad" == config['database.admin.user']
    assert "sa" == config['database.user']

def test_config_calls_ccadmin_if_config_does_not_exit(fs):
    ccadmin_client=FakeCCAdminClient(local_config_id)
    ccadmin_client.show_config_content="database.admin.user=ad"
    em_project  = FakeEMProjectBuilder(fs)\
                    .with_ccadmin(ccadmin_client)\
                                          .build()
    config = em_project.config(local_config_id)

    assert "ad" == config['database.admin.user']

def test_config_throws_exception_if_ccadmin_config_fails(fs):
    with pytest.raises(ConfigException) as exc_info:
        ccadmin_client=FakeCCAdminClient(None)
        ccadmin_client.show_config_content=None

        em_project  = FakeEMProjectBuilder(fs)\
                        .with_ccadmin(ccadmin_client)\
                                              .build()
        config = em_project.config(local_config_id)
        
    error_msg= "Unable to configure project:\n  Failed when running ccadmin"
    assert error_msg in str(exc_info.value)

def test_config_with_no_args_returns_default_config(fs):
    config_id = EMConfigID("localdev","localhost","ad")
    em_project  = FakeEMProjectBuilder(fs)\
                    .add_config(local_config_id,"database.host=localhost")\
                    .build()

    em_project.set_default_config_id(config_id)
    config = em_project.config()

    assert "localhost" == config["database.host"]

def test_config_with_no_args_throws_exc_when_no_default_defined(fs):
    config_id = EMConfigID("localdev","localhost","ad")
    em_project  = FakeEMProjectBuilder(fs)\
                    .add_config(local_config_id, "database.host=localhost")\
                    .build()

    with pytest.raises(ConfigException) as exc_info:
        em_project.config()

    assert "Try to retrieve configuration but not config_id was specified. You can specify the config by either passing a config_id or by setting a default config_id (environment.name, machine.name and container.name)"

@pytest.mark.skip
def test_emautomation_config_throws_exception_if_file_not_there(fs):
    em_project  = EMProject("/home/em/my_project")
    with pytest.raises(ConfigFileNotFound) as excinfo:
        em_project._emautomation_config()
    assert "Config file" in str(excinfo.value)

@pytest.mark.skip
def test_emautomation_config_throws_exception_if_prop_not_set(fs):
    em_project = FakeEMProjectBuilder(fs)\
                            .build()
    em_project._emautomation_config()['some.strange.prop']
    assert "Property 'emautomation.server.name' has not been set" in "heello"
