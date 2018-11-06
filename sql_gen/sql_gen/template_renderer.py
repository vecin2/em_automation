from sql_gen.sql_gen.prompt_parser import PromptParser
from sql_gen.sql_gen.environment_selection import TemplateSelector
from sql_gen.sql_gen.sql_eval_context import initialContext

class TemplateRenderer(object):
    def run(self):
        template_selector = TemplateSelector()
        template = template_selector.select_template()
        if template is not None:
            return self.render(template)
        return ""

    def render(self,template):
        context = self.build_context(template)
        return template.render(context)

    def build_context(self,template):
        template_values = initialContext()
        parser = PromptParser(template)
        prompt =parser.next_prompt(template_values) 
        while prompt:
            prompt.populate_value(template_values)
            prompt = parser.next_prompt(template_values)
        return template_values
