from sql_gen.filters import PromptFilter

def suggest(value, suggestions):
    return value

def get_template_filter():
    return suggest

class SuggestFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt,context):
        args=self._render_args(context)
        suggestions = args[0]
        prompt.add_suggestions(suggestions)
        return prompt.display_text
