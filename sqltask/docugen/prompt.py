from sqltask import logger
from sqltask.ui import prompt


class Prompt:
    """Prompts for a template value to the user. It contains a list of filters which are applied 
    and can modified the prompt data, e.g. add completion, change display text, etc..."""

    def __init__(self, variable_name, filter_list):
        self.variable_name = variable_name
        self.filter_list = filter_list
        self.display_text = variable_name
        self.text_to_print = None
        self.completer = None

    def __str__(self):
        return self.variable_name

    def get_display_text(self, context={}):
        return self.display_text + ": "

    def resolve(self, eval_context):
        self._apply_filters(eval_context)
        return self

    def _apply_filters(self, context):
        for template_filter in self.filter_list:
            template_filter.apply(self, context)

    def append_filter(self, prompt_filter):
        self.filter_list.append(prompt_filter)

    def populate_value(self, context):
        var = self.run(context)
        # it removes last value enter so it goes back and prompts it again
        if var == "<":
            # context.remove_last_item()
            self._remove_last(context)
        else:
            context[self.variable_name] = var

    def _remove_last(self, context):
        keys = [k for k in context]
        return context.pop(keys[-1])

    def run(self, context):
        logger.debug("Running prompt :'" + self.get_display_text() + "'")
        if self.text_to_print:
            print(self.text_to_print)
        user_input = prompt(self.get_display_text(), completer=self.completer)
        logger.debug("User entered: " + user_input)
        return user_input
