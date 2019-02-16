import pytest

from sql_gen.create_document_from_template_command import SelectTemplateLoader
from sql_gen.ui import MenuOption

def make():
    return CreateDocumentFromTemplateCommand()

@pytest.fixture
def loader():
    yield SelectTemplateLoader('/templates')

def test_no_templates_returns_only_exit(loader):
    expected_options=[MenuOption('x','Save && Exit')]
    assert str(expected_options) ==str(loader.list_options())

def test_load_one_template(fs,loader):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    expected_options=[MenuOption('1','hello.sql'),
                      MenuOption('x','Save && Exit')]
    assert str(expected_options) ==str(loader.list_options())

def test_list_multiple_templates_in_alphabetic_order(fs,loader):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    expected_options=[MenuOption('1','bye.sql'),
                      MenuOption('2','hello.sql'),
                      MenuOption('x','Save && Exit')]
    assert str(expected_options) ==str(loader.list_options())
