class DefaultFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt):
        if (len (self.filter.args) is 1 and
            hasattr(self.filter.args[0],"value")):
                default_unicode= self.filter.args[0].value
                prompt.display_text = prompt.display_text + " (default is "+default_unicode+")"
                return prompt.display_text

        raise ValueError("Default Filters at the moment only support "+\
                    "constant values, a variable was passed "+str(self.filter.args[0]))
