import os
from collections import defaultdict
from pathlib import Path

import sqltask
from sqltask.config.properties_file import PropertiesFile
from sqltask.emproject.config import ProjectProperties
from sqltask.exceptions import CCAdminException, ConfigException
from sqltask.utils.filesystem import ProjectLayout

from sqltask.emproject.ccadmin import CCAdmin

PATHS = {
    "ccadmin": "bin",
    "db_releases_file": "config/releases.xml",
    "sql_modules": "modules",
    "repo_modules": "repository/default",
    "config": "work/config",
    "show_config_txt": "work/config/show-config-txt",
}
MANDATORY_KEYS = ["ccadmin", "repo_modules"]


class EMProject(object):
    def __init__(self, ccadmin_client=None, emprj_path=None):
        self._config = None
        self.root = Path(emprj_path)
        self._paths = None
        self._ccadmin_client = ccadmin_client
        self.default_config_id = None
        self.emconfig = None
        self._project_properties = None

    @property
    def paths(self):
        if not self._paths:
            self._paths = ProjectLayout(self.root, PATHS)

        return self._paths


