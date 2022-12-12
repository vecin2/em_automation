import sys

from prompt_toolkit import prompt as tk_prompt

from sql_gen.docugen.completer import SuggestionCompleter


def prompt(text, completer=None, default=""):
    try:
        if not sys.stdout.isatty() or not sys.stdin.isatty():
            # return input(text)
            print(text)
            user_input = sys.stdin.readline().strip()
            print(user_input)
            return user_input
        else:
            return tk_prompt(text, completer=completer, default=default)
    except EOFError:
        # If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()


def prompt_suggestions(text, suggestions, default):
    str_suggestions = [str(item) for item in suggestions]
    completer = SuggestionCompleter(str_suggestions)
    return prompt(text, completer=completer, default=default)


class MenuOption(object):
    def __init__(self, code, name, is_help=False):
        self.code = code
        self.name = name
        self.is_help = is_help

    @staticmethod
    def parse(text):
        if text[-1] == "?":
            is_help = True
        else:
            is_help = False
        # not important code, what we really care is the help flag
        return MenuOption(None, text, is_help)

    def matches(self, input_entered):
        if input_entered[-1] == "?":
            input_entered = input_entered[:-1]  # remove '?' to match
        if (
            self.code == input_entered
            or self.name == input_entered
            or input_entered == str(self)
        ):
            return True
        return False

    def __repr__(self):
        return str(self.code) + ". " + self.name

    def __eq__(self, other):
        return (
            self.code == other.code
            and self.name == other.name
            and self.is_help == other.is_help
        )


def select_option(text, option_list, no_of_retries, default):
    option = None
    counter = 0
    while option is None and counter < no_of_retries:
        user_input = prompt_suggestions(text, option_list, default)
        option = match_options(user_input, option_list)
        counter += 1
    if not option:
        raise ValueError("Too many wrong attempts")
    return option


def select_string(text, string_list):
    result = None
    while result is None:
        user_input = prompt_suggestions(text, string_list)
        if user_input in string_list:
            result = user_input

    return result


def select_string_noprompt(text, string_list):
    result = None
    while result is None:
        user_input = prompt(text)
        if user_input in string_list:
            result = user_input

    return result


def match_options(input_entered, option_list):
    for option in option_list:
        if option.matches(input_entered):
            if input_entered[-1] == "?":
                is_help = True
            else:
                is_help = False
            return MenuOption(option.code, option.name, is_help=is_help)
    return None
