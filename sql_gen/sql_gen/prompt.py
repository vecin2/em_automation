from sql_gen.ui.cli_ui_util import input_with_validation
from prompt_toolkit import prompt
#from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
from sql_gen.sql_gen.completer import SuggestionCompleter

class Prompt:
    def __init__(self, variable_name, filter_list):
        self.variable_name =variable_name
        self.filter_list = filter_list
        self.display_text = variable_name
        self.completer = None

    def get_display_text(self,context={}):
        return self.display_text+": "

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
        context[self.variable_name] = var

    def run(self,context):
        user_input = prompt(self.get_display_text(),
                                completer=self.completer)
        return user_input


