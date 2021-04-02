from sql_gen.sqltask_jinja.filters import PromptFilter


class DefaultFilter(PromptFilter):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter

    def apply(self, prompt, context):
        default_value = self._render_args(context)[0]
        prompt.display_text = (
            prompt.display_text + " (default is " + str(default_value) + ")"
        )
        return prompt.display_text
