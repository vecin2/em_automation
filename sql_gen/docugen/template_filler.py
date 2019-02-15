from sql_gen.docugen.prompt_parser import PromptParser
from sql_gen import logger

class TemplateFiller(object):
    def fill(self,template,initial_context):
        context = self.build_context(template,initial_context)
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
