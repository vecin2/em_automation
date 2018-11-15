import pytest
import os
from sql_gen.emproject import EMProject,EMConfigID
from sql_gen.emproject import emproject_home
from sql_gen.exceptions import CCAdminException

class FakeCCAdminClient (object):
    show_config_content=""
    fake_emproject_builder = None

    def __init__(self,config_id):
        self.config_id = config_id

    def show_config(self,params):
        if self.show_config_content:
            self.fake_emproject_builder.add_config(self.config_id,self.show_config_content)
            return
        error_msg= "Failed when running ccadmin show-config -Dformat=txt"
        raise CCAdminException(error_msg)


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
        self.ccadmin_client =FakeCCAdminClient(None)
        self.ccadmin_client.fake_emproject_builder=self
        self.emproject =EMProject(self.root,self.ccadmin_client)
        self.config_map={}

    def add_config_settings(self, config_id, settings_map):
        self.config_map[config_id] = settings_map

    def _config_env_machine_container(self,
                                 env_name,
                                 machine_name,
                                  container_name):
        config_content=\
            "emautomation.environment.name="+env_name+\
            "\nemautomation.container.name="+container_name+\
            "\nemautomation.machine.name="+machine_name

        self._create_file(EMProject.EMAUTOMATION_CONFIG_PATH,\
                          config_content)
        return self

    def add_emautomation_config(self, config_content):
        self._create_file(self.emproject.emautomation_config_path(),\
                            contents=config_content)

    def add_config(self, config_id, config_content):
        self._create_file(self.emproject.config_path(config_id),\
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

