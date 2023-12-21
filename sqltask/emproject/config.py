import glob
import os
from collections import ChainMap
from pathlib import Path

from sqltask.config.properties_file import NullPropertiesFile, PropertiesFile


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
        for file in self._env_property_files():
            items.append((PropertiesFile(file)))
        return self._merge_avoiding_interpolation_errors(items)

    def merge_properties_file(self, *properties_files):
        items = []
        items.append(self.properties)
        for properties_file in properties_files:
            items.append(properties_file.properties)
        return self._merge_avoiding_interpolation_errors(items)

    def _merge_avoiding_interpolation_errors(self, list_of_maps):
        # do not resolve items otherwise we might get interpolation errors
        return ChainMap(*list_of_maps)

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


class ProjectProperties(object):
    def __init__(self, project_root, config_generator=None):
        if type(project_root) == str:
            project_root = Path(project_root)
        self.project_root = project_root
        self._core_properties = None
        self._local_properties = None
        self._em_properties = None
        self.config_generator = config_generator

    @property
    def config_folder(self):
        return self.project_root / "project/sqltask/config"

    @property
    def library_file_path(self):
        return self.config_folder / ".library"

    @property
    def core_properties_path(self):
        return self.config_folder / "core.properties"

    @property
    def local_properties_path(self):
        return self.config_folder / "local.properties"

    @property
    def environment_properties_path(self):
        return self.project_root / "work/config/show-config-txt"

    @property
    def library_path(self):
        return Path(self.library_file_path.read_text().strip())

    @property
    def core(self):
        if not self._core_properties:
            self._core_properties = PropertiesFile(self.core_properties_path)
        return self._core_properties

    @property
    def local(self):
        if not self._local_properties:
            # local properties not mandatory
            if not os.path.exists(self.local_properties_path):
                self._local_properties = NullPropertiesFile()
            else:
                self._local_properties = PropertiesFile(self.local_properties_path)
        return self._local_properties

    @property
    def em(self):
        if not self._em_properties:
            self._em_properties = EMEnvironmentConfig(
                self.environment_properties_path,
                self.environment_name,
                config_generator=self.config_generator,
            )
        return self._em_properties

    @property
    def merged_config(self):
        return AttributeBasedConfig(
            self.em.merge_properties_file(self.core, self.local)
        )

    @property
    def environment_name(self):
        return self.core["environment.name"]


class AttributeBasedConfig(object):
    def __init__(self, properties_map):
        self.properties_map = properties_map

    def __getitem__(self, property_name):  # self.<<attribute_name>>
        return self.properties_map[property_name]

    def __contains__(self, item):
        return item in self.properties_map

    def __getattr__(self, property_name):  # self[]
        attr = property_name.replace("_", ".")
        property_value = self.properties_map[attr]
        if property_value:
            return property_value
        else:
            super().__getattribute__(attr)
