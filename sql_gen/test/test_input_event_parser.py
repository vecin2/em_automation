import pytest

from sql_gen.docugen.render_template_handler import RenderTemplateHandler
from sql_gen.help import ViewTestHandler
from sql_gen.main_menu import ExitHandler, HandlerType, InputParser, MenuOption

first_option = MenuOption("1", "first_option")
second_option = MenuOption("2", "second_option")
option_list = [first_option, second_option, MenuOption.saveAndExit()]


class HandlerFactory(object):
    def make(self, handler_type):
        if handler_type == HandlerType.RENDER:
            return RenderTemplateHandler(None)
        elif handler_type == HandlerType.EXIT:
            return ExitHandler()
        elif handler_type == HandlerType.VIEW_TEST:
            return ViewTestHandler(None)


handler_factory = HandlerFactory()


parser = InputParser()


def parse(input_str):
    return parser.parse(input_str, option_list)


def assert_handled_by(handler_type, input_str):
    input = parse(input_str)
    handler = handler_factory.make(handler_type)

    assert handler.handles(input)


def test_parse_render_event():
    input_str = "1. first_option"
    assert_handled_by(HandlerType.RENDER, input_str)


def test_parse_view_test_event():
    input_str = "1. first_option -t"
    assert_handled_by(HandlerType.VIEW_TEST, input_str)


@pytest.mark.skip
def test_parse_view_test_event_with_extra_spaces():
    input_str = "1. first_option -t  "
    input_event = parse(input_str)

    assert InputEvent(first_option, HandlerType.VIEW_TEST) == input_event


def test_parse_exit_event():
    input_str = "x. Save && Exit"
    assert_handled_by(HandlerType.EXIT, input_str)
