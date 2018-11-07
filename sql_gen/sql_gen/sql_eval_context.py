import sys
from sql_gen.queries.queries import Keynames,EntityDefinition,ProcessDescriptor
from jinja2.utils import concat
from sql_gen.logger import logger

_builtin_objects={'_keynames':Keynames(),
                  '_ed'      :EntityDefinition(),
                  '_pd'      :ProcessDescriptor()
                 }
def initialContext():
    return _builtin_objects

def prepare_eval_context(template,*args, **kwargs):
    logger.debug("Starting preparing eval context")
    vars =dict(*args,**kwargs)
    context =_create_eval_context(template,vars)
    logger.debug("Finish preparing eval context")
    return  {**vars, **context.vars}

def _add_builtin_objects(*args,**kwargs):
    return {**dict(*args,**kwargs),**_builtin_objects}

def _create_eval_context(template,template_vars):
    context =template.new_context(template_vars)
    try:
        logger.debug("Start rendering template to resolve arguments")
        s= concat(template.root_render_func(context))
        logger.debug("End rendering")
        #merge template_vals with resolve vars at render time
    except Exception:
        #catch the exception as some vars might not be populated yet
        exc_info = sys.exc_info()
        logger.error("Error occur while rendering. This might be expected as we are rendering with a context which is not filled yet")
    return context
