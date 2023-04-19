from pathlib import Path

from sql_gen.config import PropertiesFile


def assert_equal_properties(properties, filepath):
    config_file = PropertiesFile(filepath)

    assert len(properties) == len(config_file)
    for k, v in properties.items():
        assert v == config_file[k]


class PropertiesFileGenerator(object):
    def __init__(self, properties={}):
        if type(properties) == str:
            properties = self._to_dict(properties)
        self.config = properties

    def _to_dict(self, config_content):
        dict = {}
        for line in config_content.splitlines():
            segments = line.split("=")
            k = segments[0]
            v = "=".join(segments[1:])  # e.g property=some property with = within value
            dict[k] = v
        return dict

    def put(self, property_name, property_value):
        self.config[property_name] = property_value

    def save(self, filepath):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(self._convert_to_text())

    def _convert_to_text(self):
        str_builder = []
        for k, v in self.config.items():
            if str_builder:
                str_builder.append("\n")

            str_builder.append(f"{k}={v}")
        return "".join(str_builder)


class PropertiesFolderGenerator(object):
    def __init__(self):
        self.file_generators = {}

    def add_properties_file(self, key, properties_dict):
        self.file_generators[key] = PropertiesFileGenerator(properties_dict)

    def save(self, destination):
        for key, file_generator in self.file_generators.items():
            file_generator.save(Path(destination) / self._get_file_name(key))

    def _get_file_name(self, key):
        return key
