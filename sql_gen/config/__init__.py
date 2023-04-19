# PropertiesFile needs to be imported before ProjectProperties otherwise it fails with circular dependency

from sql_gen.config.properties_file import PropertiesFile

__all__ = ["PropertiesFile"]
