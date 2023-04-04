from sql_gen.main_menu import (EventType, InputEvent, InputEventParser,
                               MenuOption)


first_option = MenuOption("1", "first_option")
second_option = MenuOption("2", "second_option")
option_list = [first_option, second_option, MenuOption.saveAndExit()]


def parse(input_str):
    return InputEventParser().parse(input_str, option_list)


def test_parse_render_event():
    input_str = "1. first_option"
    input_event = parse(input_str)

    assert InputEvent(first_option, EventType.RENDER) == input_event


def test_parse_view_test_event():
    input_str = "1. first_option -t"
    input_event = parse(input_str)

    assert InputEvent(first_option, EventType.VIEW_TEST) == input_event


def test_parse_view_test_event_with_extra_spaces():
    input_str = "1. first_option -t  "
    input_event = parse(input_str)

    assert InputEvent(first_option, EventType.VIEW_TEST) == input_event


def test_parse_exit_event():
    input_str = "x. Save && Exit"
    input_event = parse(input_str)
    assert InputEvent(MenuOption.saveAndExit(), EventType.EXIT) == input_event
