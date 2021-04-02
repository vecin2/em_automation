from sql_gen.ui import MenuOption
from sql_gen.ui.utils import match_options


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
