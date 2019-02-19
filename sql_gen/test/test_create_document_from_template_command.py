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

def test_lists_one_template(fs,loader):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    expected_options=[MenuOption('1','hello.sql'),
                      MenuOption('x','Save && Exit')]
    assert str(expected_options) ==str(loader.list_options())

def test_lists_templates_within_template_foler_in_alphabetic_order(fs,loader):
    fs.create_file("/templates/hello.sql", contents="hello {{name}}!")
    fs.create_file("/templates/bye.sql", contents="bye {{name}}!")
    expected_options=[MenuOption('1','bye.sql'),
                      MenuOption('2','hello.sql'),
                      MenuOption('x','Save && Exit')]
    assert str(expected_options) ==str(loader.list_options())

def test_hides_templates_within_hidden_folder(fs,loader):
    fs.create_file("/templates/create_verb.sql", contents="hello {{name}}!")
    fs.create_file("/templates/hidden_templates/raw_insert_verb.sql", contents="bye {{name}}!")
    expected_options=[MenuOption('1','create_verb.sql'),
                      MenuOption('x','Save && Exit')]
    assert str(expected_options) ==str(loader.list_options())

