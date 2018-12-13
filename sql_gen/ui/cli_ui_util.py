import signal
from prompt_toolkit import prompt
from sql_gen.sql_gen.completer import SuggestionCompleter

def input_with_validation(text):
    try:
        value = input(text)
        user_input = prompt(text,None)
        return value
    except EOFError:
        #If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()
def suggest_prompt(text,suggestions):
    str_suggestions = [str(item) for item in suggestions]
    completer = SuggestionCompleter(str_suggestions)
    return prompt(text,completer=completer)


class InputRequester(object):
    def __init__(self):
        self.task_already_exists=False

    def request_value(self, text, *args):
        value = input_with_validation(text) 
        if args is not None:
            while value not in args:
                value = input_with_validation(text) 
        return value

