from sql_gen.docugen.prompt_parser import PromptParser
from sql_gen.docugen.template_context import TemplateContext
from sql_gen.docugen.environment_selection import TemplateSelector
from sql_gen import logger

class TemplateRenderer(object):
    def __init__(self, listener,template_selector):
        self.listener = listener
        self.template_selector = template_selector

    def run(self,context):
        logger.debug("About to run template renderer to start filling template values")
        template = self.template_selector.select_template()
        if template is not None:
            self.fill_template(template,context)
            logger.debug("Finish filling and rendering template "+template.name)
        self.listener.finished()

    def fill_template(self,template,context):
        context = self.build_context(template,context)
        return template.render(context)

    def build_context(self,template,context):
        parser = PromptParser(template)
        template_values=context
        prompt =parser.next_prompt(template_values) 
        logger.debug("About to build context starting with initial context:\n"+str(template_values))
        while prompt:
            prompt.populate_value(template_values)
            prompt = parser.next_prompt(template_values)
        return template_values
