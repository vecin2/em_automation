from sql_gen.sql_gen.prompt_parser import PromptParser

class Prompter(object):
    def __init__(self, template):
        self.template = template

    def build_context(self):
        template_values ={}
        parser = PromptParser(self.template)
        prompt =parser.next_prompt(template_values) 
        while prompt:
            prompt.populate_value(template_values)
            prompt = parser.next_prompt(template_values)
        return template_values
