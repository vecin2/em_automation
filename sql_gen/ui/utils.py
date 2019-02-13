import sys

from prompt_toolkit import prompt as tk_prompt
from sql_gen.docugen.completer import SuggestionCompleter

def prompt(text,suggestions):
    try:
        if not sys.stdout.isatty():
            return input(text)
        else:
            str_suggestions = [str(item) for item in suggestions]
            completer = SuggestionCompleter(str_suggestions)
            return tk_prompt(text,completer=completer)
    except EOFError:
        #If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()

class DummyAction():
    def run():
        """implementation of the null pattern"""

class MenuOption(object):
    def __init__(self,code, name,action=DummyAction()):
        self.code =code
        self.name =name
    def __repr__(self):
        return str(self.code) +". "+self.name

def select_option(text, option_list):
    option =None
    while option is None:
        template_input =prompt(text,option_list)
        option = match_option(template_input,option_list)
    return option

def match_option(input_entered,option_list):
    for option in option_list:
        if option.code == input_entered or\
            input_entered == str(option):
            return option
    return None
