class DefaultFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt_text):
        default_unicode= self.filter.args[0].value
        prompt_text = prompt_text + " (default is "+default_unicode+")"
        return prompt_text

