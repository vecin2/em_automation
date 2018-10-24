def description(value, description):
    return value

def get_template_filter():
    return description

class DescriptionFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt):
        prompt.display_text =self.filter.args[0].value
        
