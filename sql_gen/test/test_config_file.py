import pytest
from sql_gen.config import ConfigFile


def test_value_in_config(fs):
    fs.create_file("/home/config.properties", contents="")
    config_file = ConfigFile("/home/config.properties")
    assert "home" not in config_file


def test_value_in_config(fs):
    fs.create_file("/home/config.properties", contents="home='/em/prj'")
    config_file = ConfigFile("/home/config.properties")
    assert "home" in config_file
