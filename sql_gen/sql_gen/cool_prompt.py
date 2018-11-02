from sql_gen.ui.cli_ui_util import input_with_validation
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
#import click
from fuzzyfinder import fuzzyfinder
from sql_gen.emproject import addb
from sql_gen.sql_gen.completer import PathCompleter
#result =addb.query("SELECT NAME FROM EVA_ENTITY_DEFINITION")
#suggestions=[]
#for key in result:
#    print(suggestions.append(key['NAME']))

#print (str(suggestions))
suggestions = ['select', 'from', 'insert', 'update', 'delete', 'drop']

class SQLCompleter(Completer):
    def __init__(self,suggestions):
        self.suggestions = suggestions
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, self.suggestions)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))

def cool_prompt(question):
    while 1:
        user_input = prompt(question,
                            #completer=SQLCompleter(suggestions)
                            completer= PathCompleter()
                            )
    return user_input

cool_prompt("hello: ")

class Prompt:
    def __init__(self, variable_name, filter_list):
        self.variable_name =variable_name
        self.filter_list = filter_list

    def get_diplay_text(self):
        self.display_text = self.variable_name
        for template_filter in self.filter_list:
            self.display_text = template_filter.apply(self.display_text);
        return self.display_text+": "

    def auto_suggestions(self):
        print("hello")

    def append_filter(self, prompt_filter):
        self.filter_list.append(prompt_filter)

    def populate_value(self,context):
        #var =input_with_validation(self.get_diplay_text())
        var = cool_prompt(self.get_diplay_text())
        if var:
            context[self.variable_name] = var
