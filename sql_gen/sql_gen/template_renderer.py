from sql_gen.sql_gen.prompt_parser import PromptParser
from sql_gen.sql_gen.environment_selection import TemplateSelector
from sql_gen.sql_gen.sql_eval_context import initialContext
from sql_gen.logger import logger

class TemplateRenderer(object):
    def run(self):
        logger.debug("About to run template renderer to start filling template values")
        template_selector = TemplateSelector()
        template = template_selector.select_template()
        if template is not None:
            logger.debug("Finish filling and rendering template "+template.name)
            return self.render(template)
        return ""

    def render(self,template):
        context = self.build_context(template)
        logger.debug("About to render template with final context"+template.name)
        result = template.render(context)
        logger.debug("Template rendered successfully: "+template.name)
        return result

    def build_context(self,template):
        template_values = initialContext()
        parser = PromptParser(template)
        logger.debug("About to build context starting with initial context:\n"+str(template_values))
        prompt =parser.next_prompt(template_values) 
        while prompt:
            prompt.populate_value(template_values)
            prompt = parser.next_prompt(template_values)
        return template_values
