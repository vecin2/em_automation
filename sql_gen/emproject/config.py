import os

from sql_gen.config import ConfigFile


class EMConfigID(object):
    def __init__(self, env_name, machine_name, container_name):
        self.env_name = env_name
        self.machine_name = machine_name
        self.container_name = container_name

    def __repr__(self):
        return f"{self.env_name},{self.machine_name},{self.container_name}"

    def __str__(self):
        return f"{self.env_name},{self.machine_name},{self.container_name}"

    def filename(self):
        return (
            self.env_name + "-" + self.machine_name + "-" + self.container_name + ".txt"
        )


class EMEnvironmentConfig(object):
    def __init__(self, rootpath, environment_name, config_generator=None):
        self.rootpath = rootpath
        self.environment_name = environment_name
        self.config_files = {}
        self.machine_name = "localhost"  # only localhost supported at the moment
        self.config_generator = config_generator

    def __contains__(self, item):
        for config_file in self.config_files:
            if item in config_file:
                return True
        return False

    def __getitem__(self, component_name):
        if component_name not in self.config_files:
            self.config_files[component_name] = self._read_component_config(
                component_name
            )
        return self.config_files[component_name]

    def _read_component_config(self, component_name):
        if not self._config_file_exist(component_name):
            self._generate_config_files()

        return self._read_config_file(component_name)

    def _config_file_exist(self, component_name):
        return os.path.exists(self._file_location(component_name))

    def _file_location(self, component_name):
        return (
            self.rootpath
            + os.path.sep
            + self._make_config_id(component_name).filename()
        )

    def _generate_config_files(self):
        self.config_generator.generate_config()

    def _read_config_file(self, component_name):
        return ConfigFile(self._file_location(component_name))

    def _make_config_id(self, component_name):
        return EMConfigID(self.environment_name, self.machine_name, component_name)

        # if not config_id.file_exists(self.rootpath):
        #     config_file = config_id.get_config_file()
        #     self.config_files[str(config_id)] = config_file
        # return self.config_files[config_id]
