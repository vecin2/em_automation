import sys

from prompt_toolkit import prompt as tk_prompt
from sql_gen.docugen.completer import SuggestionCompleter

def prompt(text,completer=None):
    try:
        if not sys.stdout.isatty():
            #return input(text)
            print(text)
            return sys.stdin.readline().strip()
        else:
            return tk_prompt(text,completer=completer)
    except EOFError:
        #If Ctrl+D is enter exit the program
        print("\n\nEOF entered. Exiting.")
        exit()

def prompt_suggestions(text,suggestions):
        str_suggestions = [str(item) for item in suggestions]
        completer = SuggestionCompleter(str_suggestions)
        return prompt(text,completer=completer)

class MenuOption(object):
    def __init__(self,code, name):
        self.code =code
        self.name =name

    def matches(self,input_entered):
        if self.code == input_entered or\
            self.name == input_entered or\
            input_entered == str(self):
            return True
        return False

    def __repr__(self):
        return str(self.code) +". "+self.name

def select_option(text, option_list):
    option =None
    while option is None:
        user_input =prompt_suggestions(text,option_list)
        option = match_options(user_input,option_list)
    return option

def select_item(text, string_list):
    result =None
    while result is None:
        user_input =prompt(text)
        if user_input in string_list:
            result = user_input

    return result

def match_options(input_entered,option_list):
    for option in option_list:
        if option.matches(input_entered):
            return option
    return None
