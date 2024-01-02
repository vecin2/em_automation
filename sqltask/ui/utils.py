import sys

from prompt_toolkit import prompt as tk_prompt

from sqltask.docugen.completer import SuggestionCompleter


def prompt(text, completer=None, default=""):
    try:
        if not sys.stdout.isatty() or not sys.stdin.isatty():
            # return input(text)
            print(text)
            if default:
                print("using default")
                user_input = default
            else:
                user_input = sys.stdin.readline().strip()
            print(user_input)
            return user_input
        else:
            return tk_prompt(text, completer=completer, default=default)
    except EOFError:
        # If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()


def prompt_suggestions(text, suggestions, default=""):
    str_suggestions = [str(item) for item in suggestions]
    completer = SuggestionCompleter(str_suggestions)
    return prompt(text, completer=completer, default=default)


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
