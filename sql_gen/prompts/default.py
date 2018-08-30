class DefaultFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt_text):
        default_unicode= self.filter.args[0].value
        if default_unicode:
            default_value= default_unicode.encode('ascii','ignore')
            prompt_text = prompt_text + " (default is "+str(default_value)+")"
        return prompt_text
