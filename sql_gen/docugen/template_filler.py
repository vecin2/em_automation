from sql_gen import logger
from sql_gen.docugen.env_builder import TraceUndefined
from sql_gen.docugen.prompt_visitor import PromptVisitor
from sql_gen.docugen.template_context import TemplateContext
from sql_gen.docugen.template_inliner import TemplateInliner


class TemplateVars(dict):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def remove_last_item(self):
        keys = [k for k in self]
        return self.pop(keys[-1])


class TemplateFiller(object):
    def __init__(self, template=None, initial_context=None):
        if template:
            logger.debug(
                "Instantiating TemplateFiller for template '" + template.name + "'"
            )
        self.set_template(template)
        self.initial_context =initial_context

    def _get_prompt_visitor(self):
        if not self.prompt_visitor:
            self.prompt_visitor = PromptVisitor(self._get_ast())
        return self.prompt_visitor

    def _get_ast(self):
        return self.inline_template().environment.parse(self._get_template_source())

    def set_template(self, template):
        self._template = template
        self._inline_template = None
        self.prompt_visitor = None

    def inline_template(self):
        if not self._inline_template:
            self._inline_template = self._template.environment.from_string(
                self._get_template_source()
            )
        return self._inline_template

    def _get_template_source(self):
        return TemplateInliner(self._template).inline()

    def fill_and_render(self, template):
        self.set_template(template)
        context = self.fill(dict(self.initial_context))
        return self.inline_template().render(self._remove_empties(context))

    def fill(self, initial_context):
        # every time we fill we clear global state with var names
        # that are executed
        TraceUndefined.clear_vars()
        return self.build_context(initial_context)

    def _remove_empties(self, context):
        # we need to remove empties so default filters get applied
        # otherwise it will use empty value instead of the default
        # this allows as well go back to the previous question
        keys = [k for k in context if context[k] == ""]
        for key in keys:
            context.pop(key, None)
        return context

    def build_context(self, template_values):
        prompt = self.next_prompt(template_values)
        logger.debug(
            "About to build context starting with initial context:\n"
            + str(template_values)
        )
        while prompt:
            prompt.populate_value(template_values)
            prompt = self.next_prompt(template_values)
        return template_values

    def next_prompt(self, template_values={}):
        self._get_prompt_visitor()
        context = TemplateContext(self.inline_template(), template_values)
        TraceUndefined.clear_vars()
        return self._get_prompt_visitor().next_prompt(context)
