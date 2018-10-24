def suggest(value, suggestions):
    return value

def get_template_filter():
    return suggest

class SuggestFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt):
        print(self.filter.args[0])
        suggestions=[]
        for item in self.filter.args[0].items:
            suggestions.append(item.value)
        prompt.add_suggestions(suggestions)
        return prompt.display_text
        #return str(self.filter.args[0].items[0].value)
