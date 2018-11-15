from sql_gen.sql_gen.prompt_parser import PromptParser
from sql_gen.sql_gen.template_context import TemplateContext
from sql_gen.sql_gen.environment_selection import TemplateSelector
from sql_gen.logger import logger

class TemplateRenderer(object):
    def run(self,context):
        logger.debug("About to run template renderer to start filling template values")
        template_selector = TemplateSelector()
        template = template_selector.select_template()
        if template is not None:
            logger.debug("Finish filling and rendering template "+template.name)
            return self.render(template,context)
        return ""

    def render(self,template,context):
        context = self.build_context(template,context)
        logger.debug("About to render template with final context"+template.name)
        result = template.render(context)
        logger.debug("Template rendered successfully: "+template.name)
        return result

    def build_context(self,template,context):
        parser = PromptParser(template)
        template_values=context
        prompt =parser.next_prompt(template_values) 
        logger.debug("About to build context starting with initial context:\n"+str(template_values))
        while prompt:
            prompt.populate_value(template_values)
            prompt = parser.next_prompt(template_values)
        return template_values
