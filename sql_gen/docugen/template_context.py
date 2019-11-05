from jinja2 import Template
from jinja2.utils import concat
from sql_gen import logger

class TemplateContext():
    def __init__(self,template,vars={}):
        self._vars=vars
        self.template = template
        self._last_eval_context=None

    def resolve(self,var_name):
        context =self._eval_context()
        try:
            self._render_template(context)
        except Exception as exception:
            if var_name in context:
                #although template throwed an excpetion while rendered var was resolved
                return context[var_name]
            else:
                raise exception
        return context[var_name]

    def _eval_context(self):
        vars_copy =dict(self._vars)
        self._last_eval_context = self.template.new_context(vars_copy)
        return self._last_eval_context

    def _render_template(self,context):
        logger.debug("Start rendering template to resolve arguments")
        rendered_text =concat(self.template.root_render_func(context))
        logger.debug("End rendering")

    def __iter__(self):
            return self._vars.__iter__()

    def keys(self):
        return self._vars.keys()
    def next(self): # Python 3: def __next__(self)
            return self._vars.next()
