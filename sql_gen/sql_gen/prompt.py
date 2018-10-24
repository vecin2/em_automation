from sql_gen.ui.cli_ui_util import input_with_validation
from prompt_toolkit import prompt
#from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

class Prompt:
    def __init__(self, variable_name, filter_list):
        self.variable_name =variable_name
        self.filter_list = filter_list
        self.display_text = ""
        self.suggestions =[]

    def add_suggestions(self,suggestions):
        for suggestion in suggestions:
            self.suggestions.append(suggestion)

    def get_diplay_text(self):
        self.display_text =self.variable_name
        self._apply_filters()
        return self.display_text+": "

    def get_suggestions(self):
        self.suggestions =[]
        self._apply_filters()
        return self.suggestions

    def _apply_filters(self):
        for template_filter in self.filter_list:
            template_filter.apply(self);

    def append_filter(self, prompt_filter):
        self.filter_list.append(prompt_filter)

    def populate_value(self,context):
        var =self.run()
        if var:
            context[self.variable_name] = var

    def run(self):
           # user_input = prompt(question,
           #                     completer=SQLCompleter(suggestions)
           #                     )
        user_input = prompt(self.get_diplay_text(),
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

