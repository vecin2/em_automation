import pytest
from sql_gen.config import ConfigFile


def test_value_in_config(fs):
    fs.create_file("/home/config.properties",
                              contents="")
    config_file= ConfigFile("/home/config.properties")
    assert "home" not in config_file


def test_value_in_config(fs):
    fs.create_file("/home/config.properties",
                              contents="home='/em/prj'")
    config_file= ConfigFile("/home/config.properties")
    assert "home" in config_file

def test_duplicate_property_takes_last_value_assigned(fs):
    fs.create_file("/home/config.properties",
                              contents="home=/em/prj\nhome=/opt/appserver")
    config_file= ConfigFile("/home/config.properties")
    assert "/opt/appserver"== config_file["home"]
