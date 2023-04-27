from sqltask.sqltask_jinja.filters import PromptFilter


def print(value, text):
    return value


def get_template_filter():
    return print


class PrintFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter

    def apply(self, prompt, context):
        resolved_args = self._render_args(context)
        prompt.text_to_print = "\n" + str(resolved_args[0])
