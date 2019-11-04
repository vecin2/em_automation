from sql_gen.docugen.prompt_visitor import PromptVisitor
from sql_gen import logger
from sql_gen.docugen.env_builder import TraceUndefined
from sql_gen.docugen.template_inliner import TemplateInliner
from sql_gen.docugen.template_context import TemplateContext

class TemplateFiller(object):
    def __init__(self,template):
        logger.debug("Instantiating TemplateFiller for template '"+ template.name+"'")
        source = TemplateInliner(template).inline()
        self.template = template.environment.from_string(source)
        ast = self.template.environment.parse(source)
        self.prompt_visitor = PromptVisitor(ast)

    def fill(self,initial_context):
        #every time we fill we clear global state with var names
        #that are executed
        TraceUndefined.clear_vars()
        context = self.build_context(self.template,initial_context)
        return self.template.render(context)

    def build_context(self,template,template_values):
        prompt =self.next_prompt(template_values)
        logger.debug("About to build context starting with initial context:\n"+str(template_values))
        while prompt:
            prompt.populate_value(template_values)
            prompt = self.next_prompt(template_values)
        return template_values

    def next_prompt(self,template_values={}):
        context =TemplateContext(self.template,template_values)
        return self.prompt_visitor.next_prompt(context)
