import pytest

from sql_gen.create_document_from_template_command import (
    InteractiveSQLGenerator, TemplateSelector,MenuOption)


def match_options(input_entered, option_list):
    selector_displayer = TemplateSelector(generator=InteractiveSQLGenerator())
    return selector_displayer.match_any(input_entered, option_list)


def test_match_option_by_code():
    first_option = MenuOption("1", "first option")
    second_option = MenuOption("2", "second option")
    option_list = [first_option, second_option]
    assert first_option == match_options("1", option_list)


def test_match_option_by_name():
    first_option = MenuOption("1", "first option")
    second_option = MenuOption("2", "second option")
    option_list = [first_option, second_option]
    assert second_option == match_options("second option", option_list)


def test_match_option_by_code_and_name():
    first_option = MenuOption("1", "first option")
    second_option = MenuOption("2", "second option")
    option_list = [first_option, second_option]
    assert second_option == match_options("2. second option", option_list)




@pytest.mark.skip
def test_match_option_with_test_suffix():
    first_option = MenuOption("1", "first option")
    second_option = MenuOption("2", "second option")
    option_list = [first_option, second_option]
    second_option.info = True
    assert second_option == match_options("2. second option_test", option_list)
