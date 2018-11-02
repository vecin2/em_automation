from sql_gen.filters import PromptFilter

def description(value, description):
    return value

def get_template_filter():
    return description

class DescriptionFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt,context):
        prompt.display_text = self._render_args(context)[0]
