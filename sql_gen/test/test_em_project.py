import pytest
import os
from sql_gen.emproject import EMProject, EMConfigID
from sql_gen.exceptions import ConfigFileNotFoundException,EnvVarNotFoundException,ConfigException,InvalidEnvVarException
from sql_gen.test.utils.emproject_test_util import FakeCCAdminClient,FakeEMProjectBuilder
from unittest.mock import patch

def prj_builder(fs, root='/home/em'):
    return FakeEMProjectBuilder(fs,root)


def make_valid_em_folder_layout(fs,root):
    return FakeEMProjectBuilder(fs,root).make_valid_em_folder_layout()

def test_computes_root_cwd_is_em_root(fs):
    make_valid_em_folder_layout(fs,'opt/em/project')
    os.chdir('/opt/em/project')
    assert "/opt/em/project" == EMProject({}).root

def test_computes_root_when_cwd_is_em_subfolder(fs):
    make_valid_em_folder_layout(fs,'opt/em/project')
    os.chdir('/opt/em/project/config')
    assert "/opt/em/project" == EMProject({}).root

def test_it_uses_env_var_when_cwd_not_within_emproject(fs):
    make_valid_em_folder_layout(fs,'opt/em/project')
    os.chdir('/opt/em/')
    assert "/opt/em/project" == EMProject(
                                    env_vars={'EM_CORE_HOME':'/opt/em/project'}).root

local_config_id=EMConfigID("localdev",
                           "localhost",
                           "ad")

def test_project_prefix_computes_when_exist_a_minimum_of_modules(fs):
    em_project = prj_builder(fs).add_repo_module("PCCoreEntities")\
                            .add_repo_module("PCContactHistory")\
                            .add_config(local_config_id, "")\
                            .build()
    em_project.set_default_config_id(local_config_id)
    assert "PC" == em_project.prefix()

def test_project_prefix_returns_empty_if_not_enough_prj_modules(fs):
    em_project = prj_builder(fs).add_repo_module("CAI")\
                                .add_repo_module("IMAP")\
                                .add_repo_module("SPENCoreEntities")\
                            .build()
    assert "" == em_project.prefix()

def test_project_prefix_empty_if_not_repo_modules_created(fs):
    em_project = prj_builder(fs).build()
    assert "" ==em_project.prefix()

def test_project_prefix_empty_if_no_module_with_2_uppercase(fs):
    em_project = prj_builder(fs).add_repo_module("Other").build()
    assert "" ==em_project.prefix()

def test_project_prefix_empty_if_not_custom_module_created(fs):
    em_project = prj_builder(fs).add_repo_module("").build()
    assert "" ==em_project.prefix()

def test_project_prefix_skip_modules_without_3_uppercase(fs):
    em_project = prj_builder(fs).add_repo_module("otherModule")\
                                .add_repo_module("SPENCoreEntities")\
                                .add_repo_module("SPENContactHistory")\
                                .build()
    assert "SPEN" == em_project.prefix()

def test_project_prefix_in_config_overrides_computation(fs):
    em_project  = FakeEMProjectBuilder(fs)\
                    .add_repo_module("SPENCoreEntities")\
                    .add_repo_module("SPENContactHistory")\
                    .add_config(local_config_id, "project.prefix=GSC")\
                    .build()
    em_project.set_default_config_id(local_config_id)
    assert "GSC" == em_project.prefix()

def make_emproject(root):
    return EMProject(env_vars={'EM_CORE_HOME': root})

def test_config_path_depends_on_config_id(fs):
    em_project = make_emproject("/home/project")
    fs.create_dir("/home/project")
    mylocal_config_id=EMConfigID("mylocal","localhost","ad")
    assert "/home/project/work/config/show-config-txt/mylocal-localhost-ad.txt" == em_project.config_path(mylocal_config_id).path

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
    error_msg="Something went wrong while running ccadmin command:"
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

def test_product_layout(fs):
    config_id = EMConfigID("localdev","localhost","ad")
    em_project  = FakeEMProjectBuilder(fs)\
                    .add_config(local_config_id,"product.home=my_product/is/here")\
                    .build()

    em_project.set_default_config_id(config_id)
    assert "my_product/is/here" == em_project.product_layout().root

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
