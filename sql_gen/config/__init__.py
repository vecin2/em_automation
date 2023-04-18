# PropertiesFile needs to be imported before ProjectProperties otherwise it fails with circular dependency

from sql_gen.config.properties_file import PropertiesFile
from sql_gen.config.project_properties import ProjectProperties

__all__ = ["PropertiesFile", "ProjectProperties"]
