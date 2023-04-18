import glob
import os

from sql_gen.config import PropertiesFile


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
        if rootpath != str:
            rootpath = str(rootpath)
        self.rootpath = rootpath
        self.environment_name = environment_name
        self.machine_name = "localhost"  # only localhost supported at the moment
        self.config_generator = config_generator
        self.properties = {}

    def __getattr__(self, attr):  # self[]
        property_name = attr.replace("_", ".")
        property_value = self._get_value(property_name)

        if property_value:
            return property_value
        else:
            super().__getattribute__(attr)

    def __getitem__(self, property_name):  # self.<<attribute_name>>
        return self._get_value(property_name)

    def __contains__(self, item):
        return item in self._get_properties()

    def _get_value(self, property_name):
        return self._get_properties()[property_name]

    def _get_properties(self):
        if not self.properties:
            self.properties = self._merge_env_property_files()
        return self.properties

    def _merge_env_property_files(self):
        items = []
        from collections import ChainMap
        for file in self._env_property_files():
            items.append(PropertiesFile(file).properties)
        #do not resolve items otherwise we might get interpolation errors
        result = ChainMap(*items)
        return result

    def _env_property_files(self):
        result = []
        all_config_files = self._get_config_files()

        filename_pattern = f"{self.environment_name}-{self.machine_name}-*.txt"
        result = glob.glob(self.rootpath + os.sep + filename_pattern)
        return result
        for file in all_config_files:
            result.append(file)
        return result

    def _get_config_files(self):
        if not os.path.exists(self.rootpath):
            self._generate_config_files()
        return os.listdir(self.rootpath)

    def _generate_config_files(self):
        self.config_generator.generate_config()
