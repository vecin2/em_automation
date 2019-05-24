from sql_gen.sqltask_jinja.filters import PromptFilter

def description(value, description,table=None):
    return value

def get_template_filter():
    return description

class DescriptionFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt,context):
        resolved_args=self._render_args(context)
        display_text=""
        if len(resolved_args) >1:
            table =resolved_args[1]
            display_text +=str(table)+"\n"
        display_text+=resolved_args[0]
        prompt.display_text = display_text
