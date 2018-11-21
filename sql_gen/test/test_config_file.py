import pytest
from sql_gen import ConfigFile


def test_value_in_config(fs):
    fs.create_file("/home/config.properties",
                              contents="")
    config_file= ConfigFile("/home/config.properties")
    assert "a.property" not in config_file


