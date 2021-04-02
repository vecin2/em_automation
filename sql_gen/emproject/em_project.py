import os
from collections import defaultdict

import sql_gen
from sql_gen.config import ConfigFile
from sql_gen.exceptions import (
    CCAdminException,
    ConfigException,
    ConfigFileNotFoundException,
    EnvVarNotFoundException,
    InvalidEnvVarException,
    InvalidFileSystemPathException,
)
from sql_gen.utils.filesystem import Path, ProjectLayout

from .ccadmin import CCAdmin


class EMConfigID(object):
    def __init__(self, env_name, machine_name, container_name):
        self.env_name = env_name
        self.machine_name = machine_name
        self.container_name = container_name


PATHS = {
    "ccadmin": "bin",
    "sql_modules": "modules",
    "repo_modules": "repository/default",
    "config": "work/config",
    "show_config_txt": "work/config/show-config-txt",
}
MANDATORY_KEYS = ["ccadmin", "repo_modules"]


ENV_VAR_NAME = "EM_CORE_HOME"


def current_prj_path(env_vars):
    em_root = get_em_root_from_cwd()

    if em_root:
        return em_root
    elif ENV_VAR_NAME not in env_vars:
        help_text = "It should contain the path of your current EM project."
        raise EnvVarNotFoundException(ENV_VAR_NAME, help_text)

    return env_vars[ENV_VAR_NAME]


def get_em_root_from_cwd():
    return get_em_root_from_path(repr(os.getcwd()))


def get_em_root_from_path(path):
    if is_em_root(path):
        return path
    parent = os.path.abspath(os.path.join(path, os.pardir))

    if parent == path:
        return ""

    return get_em_root_from_path(parent)


def is_em_root(path):
    return (
        os.path.exists(os.path.join(path, "bin"))
        and os.path.exists(os.path.join(path, "config"))
        and os.path.exists(os.path.join(path, "components"))
        and os.path.exists(os.path.join(path, "repository"))
    )


def get_prj_home(env_vars):
    result = current_prj_path(env_vars)

    if not os.path.exists(result):
        error_msg = (
            "Environment variable '"
            + ENV_VAR_NAME
            + "' exists "
            + "but it points to an invalid path"
        )
        raise ValueError(error_msg)

    return result


def emproject_home(env_vars=os.environ):
    try:
        return get_prj_home(env_vars)
    except Exception as excinfo:
        sql_gen.logger.error(str(excinfo))
        raise excinfo


class EMProject(object):
    def __init__(self, ccadmin_client=None, env_vars=None, emprj_path=None):
        self._config = None
        self.env_vars = env_vars
        self._root = emprj_path
        self._paths = None
        self._ccadmin_client = ccadmin_client
        self.default_config_id = None

    @property
    def root(self):
        if not self._root:
            self._root = emproject_home(self.env_vars)

        return self._root

    def has_root(self):
        try:
            emproject_home(self.env_vars)

            return True
        except:
            return False

    @property
    def paths(self):
        if not self._paths:
            self._paths = ProjectLayout(self.root, PATHS)

        return self._paths

    @property
    def ccadmin_client(self):
        if not self._ccadmin_client:
            self._ccadmin_client = CCAdmin(self.paths["ccadmin"].path)

        return self._ccadmin_client

    def set_default_config_id(self, config_id):
        self.default_config_id = config_id

    def config(self, config_id=None):
        if not self._config:
            if not self.config_path(config_id).exists():
                self._create_config()
            self._config = ConfigFile(self.config_path(config_id).path)

        return self._config

    def config_path(self, config_id=None):
        file_name = self._build_config_file_name(config_id)
        result = self.paths["show_config_txt"].join(file_name)

        return result

    def _build_config_file_name(self, config_id):
        actual_config_id = self._actual_config_id(config_id)
        env_name = actual_config_id.env_name
        machine_name = actual_config_id.machine_name
        container_name = actual_config_id.container_name

        return env_name + "-" + machine_name + "-" + container_name + ".txt"

    def _actual_config_id(self, config_id):
        if not config_id and not self.default_config_id:
            error_msg = "Try to retrieve configuration but not config_id was specified. You can specify the config by either passing a config_id or by setting a default config_id (environment.name, machine.name and container.name)"
            raise ConfigException(error_msg)
        elif config_id:
            return config_id
        else:
            return self.default_config_id

    def _create_config(self):
        try:
            self.ccadmin_client.show_config("-Dformat=txt")
        except CCAdminException as info:
            error_msg = "Something went wrong while running ccadmin command:\n  " + str(
                info
            )
            raise ConfigException(error_msg)

    def prefix(self):
        sql_gen.logger.debug(
            "Computing Prefix, config_id is: " + str(self.default_config_id)
        )

        if self.default_config_id and "project.prefix" in self.config():
            return self.config()["project.prefix"]

        custom_repo_modules = self._get_repo_custom_modules()

        if len(custom_repo_modules) > 0:
            return self._extract_module_prefix(custom_repo_modules[0])

        return ""

    def _extract_module_prefix(self, repo_module):
        result = ""
        # module like SPENCoreEntities

        for c in repo_module:
            if c.isupper():
                result += c
            else:
                break
        # result is now PCC from PCCoreEntities

        if len(result) > 2:
            return result[:-1]

        return ""

    def _get_repo_custom_modules(self):
        repo_modules = self.paths["repo_modules"].listdir()
        sql_gen.logger.debug("Computing repo custom modules")
        result = defaultdict(list)

        for module in repo_modules:
            prefix = self._extract_module_prefix(module)

            if prefix:
                result[prefix].append(module)
        sql_gen.logger.debug("Modules dict is " + str(result))

        for key in result:
            if len(result[key]) > 1:
                return result[key]

        return []

    def product_layout(self):
        return ProjectLayout(self.config()["product.home"], PATHS)
