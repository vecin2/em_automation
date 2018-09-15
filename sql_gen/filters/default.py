class DefaultFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt_text):
        if (len (self.filter.args) is 1 and
            hasattr(self.filter.args[0],"value")):
                default_unicode= self.filter.args[0].value
                prompt_text = prompt_text + " (default is "+default_unicode+")"
                return prompt_text

        raise ValueError("Default Filters at the moment only support "+\
                    "constant values, a variable was passed "+str(self.filter.args[0]))
