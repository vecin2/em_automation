import argparse

import pytest

from sqltask.main_menu import MenuOption
from sqltask.test.utils.main_menu_runner import MainMenuRunner

first_option = MenuOption("first option")
second_option = MenuOption("second option", "2")


@pytest.fixture
def main_menu_runner():
    main_menu_runner = MainMenuRunner()
    option_list = [first_option, second_option]
    main_menu_runner.with_options(option_list)
    yield main_menu_runner


def test_prompts_until_max_no_of_trials_exceed(main_menu_runner):
    # firt attemp wrong option,follow by wrong parameter, follow by wrong option
    main_menu_runner.with_selections(["asdf", str(second_option) + " -ww", "sdfsd"])

    main_menu_runner.with_max_no_of_trials(2)

    with pytest.raises(Exception) as exception:
        main_menu_runner.run()
    assert str(exception.value) == "Attempts to select a valid option exceeded."


def test_correct_input_resets_no_of_trials(main_menu_runner):
    main_menu_runner.with_selections(
        ["asdf", "slkjafsd", str(first_option), "sdfsd", str(MenuOption.saveAndExit())]
    ).with_max_no_of_trials(2)

    main_menu_runner.run()

    assert [
        "first option",
    ] == main_menu_runner.rendered_templates()


def test_multiple_render_templates_then_exit(main_menu_runner):
    main_menu_runner.with_selections(
        ["first option", "second option", "x. Save && Exit"]
    )
    main_menu_runner.run()

    assert [
        "first option",
        "second option",
    ] == main_menu_runner.rendered_templates()


def printText(args):
    print(args)


@pytest.mark.skip
def test_arg_parse():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()
    task_parser = subparser.add_parser("taskname")
    #     prog="",
    #     description="What the program does",
    #     epilog="Text at the bottom of help",
    # )
    # parser.add_argument('taskname')
    task_parser.add_argument("-d", action="store_true")
    task_parser.set_defaults(func=printText)
    args = parser.parse_args(["","template.sql", "-d"])
    assert "template.sql" == args.taskname
    assert True == args.d
    # args = parser.parse_args(["-h"])
    # assert True == args.h
