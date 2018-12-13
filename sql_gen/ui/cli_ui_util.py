import signal
from prompt_toolkit import prompt
from sql_gen.sql_gen.completer import SuggestionCompleter

def suggest_prompt(text,suggestions=[]):
    try:
        str_suggestions = [str(item) for item in suggestions]
        completer = SuggestionCompleter(str_suggestions)
        return prompt(text,completer=completer)
    except EOFError:
        #If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()


class InputRequester(object):
    def request_value(self, text, *args):
        value = suggest_prompt(text)
        if args is not None:
            while value not in args:
                value = suggest_prompt(text)
        return value

