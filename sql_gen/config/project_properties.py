from pathlib import Path

from sql_gen.config import PropertiesFile
from sql_gen.emproject.config import EMEnvironmentConfig


class ProjectProperties(object):
    def __init__(self, project_root):
        if type(project_root) == str:
            project_root = Path(project_root)
        self.project_root = project_root
        self._core_properties = None
        self._em_properties = None

    @property
    def core_properties_path(self):
        return self.project_root / "project/sqltask/config/core.properties"

    @property
    def environment_properties_path(self):
        return self.project_root / "work/config/show-config-txt"

    @property
    def core(self):
        if not self._core_properties:
            self._core_properties = PropertiesFile(self.core_properties_path)
        return self._core_properties

    @property
    def em(self):
        if not self._em_properties:
            self._em_properties = EMEnvironmentConfig(
                self.environment_properties_path, self.environment_name
            )
        return self._em_properties

    @property
    def environment_name(self):
        return self.core["environment.name"]
