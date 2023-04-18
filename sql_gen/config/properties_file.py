import io
import os
from configparser import (ConfigParser, ExtendedInterpolation,
                          InterpolationMissingOptionError)

import sql_gen


def add_section_header(properties_file, header_name):
    # configparser.ConfigParser requires at least one section header in a properties file.
    # Our properties file doesn't have one, so add a header to it on the fly.
    yield "[{}]\n".format(header_name)

    for line in properties_file:
        yield line


class PropertiesFile(object):
    def __init__(self, filepath, logger=None):
        if type(filepath) != str:
            filepath = str(filepath)
        if logger is None:
            self.logger = sql_gen.logger
        else:
            self.logger = logger
        self.filepath = filepath
        self._properties = None

    @property
    def properties(self):
        if not self._properties:
            self._properties = self._parse_file()
        return self._properties

    def _parse_file(self):
        result = {}
        try:
            parser = self._init_parser()
            result = parser["DEFAULT"]
        except InterpolationMissingOptionError:
            # self.args = (option, section, rawval, reference)
            self.logger.warning("hi")
            # we should log this as a warning
        return result

    def _init_parser(self):
        self._check_filepath_exist()
        parser = ConfigParser(interpolation=ExtendedInterpolation(), strict=False)
        with io.open(self.filepath, "r", encoding="utf-8") as file:
            file_content = add_section_header(file, "DEFAULT")
            parser.read_file(file_content)
        return parser

    def _check_filepath_exist(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                "Try to load config file '" + self.filepath + "' but it does not exist"
            )

    def get(self, key, default_value):
        return self.properties.get(key, default_value)

    def __contains__(self, item):
        return item in self.properties

    def __getitem__(self, name):
        return self.properties[name]

    def __len__(self):
        return len(self.properties)
