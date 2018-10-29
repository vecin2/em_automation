from sql_gen.ui.cli_ui_util import input_with_validation
from prompt_toolkit import prompt
#from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

class Prompt:
    def __init__(self, variable_name, filter_list):
        self.variable_name =variable_name
        self.filter_list = filter_list
        self.display_text = variable_name
        self.suggestions =[]

    def add_suggestions(self,suggestions):
        for suggestion in suggestions:
            self.suggestions.append(suggestion)

    def get_display_text(self,context={}):
        return self.display_text+": "

    def get_suggestions(self,context={}):
        return self.suggestions

    def resolve(self, eval_context):
        self._apply_filters(eval_context)
        return self

    def _apply_filters(self,context):
        for template_filter in self.filter_list:
            template_filter.apply(self,context);

    def append_filter(self, prompt_filter):
        self.filter_list.append(prompt_filter)

    def populate_value(self,context):
        var =self.run(context)
        if var:
            context[self.variable_name] = var

    def run(self,context):
        user_input = prompt(self.get_display_text(),
                                completer=SuggestionCompleter(self.suggestions))
        return user_input

class SuggestionCompleter(Completer):
    def __init__(self,suggestions):
        self.suggestions = suggestions
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, self.suggestions)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))

