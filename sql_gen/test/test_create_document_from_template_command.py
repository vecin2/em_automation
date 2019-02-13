import unittest.mock as mocker
import pytest

from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand,TemplateSelector,SelectTemplateLoader
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.ui import MenuOption

def make():
    return CreateDocumentFromTemplateCommand()

@pytest.fixture
def loader():
    env_vars={'SQL_TEMPLATES_PATH':'/templates'}
    env =EMTemplatesEnv().get_env(env_vars)
    yield SelectTemplateLoader(env)

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
@pytest.mark.skip
def test_it_selects_a_template_then_returns_it_filled():
    template="some_template"
    selector = mocker.Mock(spec=TemplateSelector)
    selector.select_template.return_value=template
    template_filler= mocker.Mock(spec=TemplateFiller)
    template_filler.fill.return_value = "hello Mark!"

    class_under_test = CreateDocumentFromTemplateCommand(selector,template_filler)
    output = class_under_test.run()

    selector.select_template.assert_called_once()
    template_filler.fill.assert_called_once_with(template)
    assert "hello Mark!" == output

@pytest.mark.skip
def test_it_allows_selecting_from_displayable_templates():
    displayer = mocker.Mock(spec=SelectTemplateDisplayer)
    loader = TemplateOption()
    selected = TemplateSelector(loader,displayer)

    selected.select_template()
    displayer.ask_for_template.assert_called_once_with(template_options)

@pytest.mark.skip
def test_exit_returns_no_():
    #option_list.append(Option("1", "create_verb.sql"))
    #option_list.append(Option("x", "Save and Exit"))
    user_inputs =["x"]
    class_under_test = CreateDocumentFromTemplateCommand(selector,template_filler)
    output = class_under_test.run()

    assert None == output

@pytest.mark.skip
def test_enter_option_id_returns_template():
    user_inputs =["1"]
    options = [Option("1","create_verb.sql")]

    selector = TemplateSelector(None,None)
    assert None == selector.run()



