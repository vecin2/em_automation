import os
from pathlib import Path

from sql_gen.emproject.config import ProjectProperties
from sql_gen.exceptions import CCAdminException


class FakeCCAdminClient(object):
    show_config_content = ""
    fake_emproject_builder = None

    def __init__(self, config_id):
        self.config_id = config_id

    def show_config(self, params):
        if self.show_config_content:
            self.fake_emproject_builder.add_config(
                self.config_id, self.show_config_content
            )
            return
        error_msg = "Failed when running ccadmin show-config -Dformat=txt"
        raise CCAdminException(error_msg)


class FakeEMProjectBuilder:
    REPO_PATH = "repository/default"

    def __init__(
        self,
        fs,
        root="/home/em",
    ):
        self.fs = fs
        self.root = root
        self.ccadmin_client = FakeCCAdminClient(None)
        self.ccadmin_client.fake_emproject_builder = self
        self.emproject = None
        self.config_map = {}
        self.environment_name = "localdev"
        self.container_name = "ad"
        self.machine_name = "localhost"

    def make_valid_em_folder_layout(self):
        self._create_dir("bin")
        self._create_dir("config")
        self._create_dir("components")
        self._create_dir("modules")
        self._create_dir("repository")
        return self

    def base_setup(self):
        self.make_valid_em_folder_layout()
        self.make_app_config()
        self.make_em_config()
        return self

    def make_app_config(self):
        self._create_dir("project/sqltask/config")
        ad_config_text = """
database.host=localhost
database.user=user
database.pass=password
database.name=oracleCL
database.port=1521
database.type=oracle
database.reporting.user=reporting_user
database.reporting.pass=reporting_password
"""
        self._create_file(
            self.ccadmin_config_path("ad"),
            contents=ad_config_text,
        )
        tps_config_text = """
database.host=localhost
database.name=oracleCL
database.port=1521
database.type=oracle
database.tenant-properties-service.user=pepe
database.tenant-properties-service.pass=pepepass
        """
        self._create_file(
            self.ccadmin_config_path("tenant-properties-service"),
            contents=tps_config_text,
        )

    def append_to_app_config(self, content):
        self._append_to_file(self.core_config_path(), content)

    def read_app_config(self):
        with open(self._abs_path(self.ccadmin_config_path()), "r") as f:
            content = f.read()
        return content

    def ccadmin_config_path(self, container_name):
        return f"work/config/show-config-txt/{self.environment_name}-{self.machine_name}-{container_name}.txt"

    def make_em_config(self):

        config_text = """
#core properties
environment.name={environment_name}
container.name={container_name}
machine.name={machine_name}
db.release.version=PRJ01

#it would be uses if the update.sequence number does not follow the pattern svn rev no + 1
#svn.rev.no.offset=100

# db.release.version=Du_01

sequence.generator=timestamp
""".format(
            environment_name=self.environment_name,
            container_name=self.container_name,
            machine_name=self.machine_name,
        )
        self._create_file(self.core_config_path(), contents=config_text)

    def core_config_path(self):
        return "project/sqltask/config/core.properties"

    def add_emautomation_config(self, config_content):
        self._create_file(
            self.emproject.emautomation_config_path(), contents=config_content
        )

    def add_config(self, config_id, config_content):

        # localdev_generator = EMEnvironmentConfigGenerator(
        #     env_name=config_id.env_name, machine_name=config_id.machine_name
        # )
        # localdev_generator.add_properties_file(config_id.container_name, config_content)
        # localdev_generator.save()
        filepath = (
            ProjectProperties(self.root).environment_properties_path
            / config_id.filename()
        )
        self._create_file(str(filepath), contents=config_content)
        # filepath = ProjectProperties(self.root).core_properties_path
        # self._create_file(
        #     str(filepath), contents="environment.name=" + config_id.env_name
        # )
        return self

    def with_ccadmin(self, ccadmin_client):
        self.ccadmin_client = ccadmin_client
        self.ccadmin_client.fake_emproject_builder = self
        self.emproject._ccadmin_client = self.ccadmin_client
        return self

    def add_repo_module(self, module_name):
        if not self._exists(self.REPO_PATH):
            self._create_dir(self.REPO_PATH)
        if module_name:
            self._create_dir(self.REPO_PATH + "/" + module_name + "/")
        return self

    def add_config_environment(self, environment_name):
        self._create_dir(f"config/environment.{environment_name}")

    def _exists(self, prj_relative_path):
        return os.path.exists(self._abs_path(prj_relative_path))

    def _create_dir(self, prj_relative_path):
        return self.fs.create_dir(self._abs_path(prj_relative_path))

    def _create_file(self, prj_relative_path, contents):
        return self.fs.create_file(self._abs_path(prj_relative_path), contents=contents)

    def _append_to_file(self, prj_relative_path, contents):
        with open(self._abs_path(prj_relative_path), "a") as f:
            f.write(contents)
        # return self.fs.create_file(, contents=contents)

    def _abs_path(self, prj_relative_path):
        rootpath = Path(self.root)
        return str((rootpath / prj_relative_path))

    def build(self):
        if not os.path.exists(self.root):
            self.fs.create_dir(self.root)
        return self.emproject
