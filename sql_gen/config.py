import configparser
import os
import re
from configparser import ConfigParser, ExtendedInterpolation

import sql_gen


def add_section_header(properties_file, header_name):
    # configparser.ConfigParser requires at least one section header in a properties file.
    # Our properties file doesn't have one, so add a header to it on the fly.
    yield "[{}]\n".format(header_name)

    for line in properties_file:
        yield line


class ConfigFile(object):
    def __init__(self, filepath, logger=None):
        if logger is None:
            self.logger = sql_gen.logger
        else:
            self.logger = logger
        self.filepath = filepath
        self._parser = None

    @property
    def properties(self):
        if not self._parser:
            self._parser = ConfigParser(interpolation=ExtendedInterpolation())

            if not os.path.exists(self.filepath):
                raise FileNotFoundError(
                    "Try to load config file '"
                    + self.filepath
                    + "' but it does not exist"
                )
            file = open(self.filepath, encoding="utf_8")
            file_content = add_section_header(file, "DEFAULT")
            self._parser.read_file(file_content)

        return self._parser["DEFAULT"]

    def get(self, key, default_value):
        return self.properties.get(key, default_value)

    def __contains__(self, item):
        return item in self.properties

    def __getitem__(self, name):
        return self.properties[name]
