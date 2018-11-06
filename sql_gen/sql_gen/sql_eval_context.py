import sys
from sql_gen.queries.queries import Keynames,EntityDefinition,ProcessDescriptor
from jinja2.utils import concat

_builtin_objects={'_keynames':Keynames(),
                  '_ed'      :EntityDefinition(),
                  '_pd'      :ProcessDescriptor()
                 }
def initialContext():
    return _builtin_objects

def prepare_eval_context(template,*args, **kwargs):
    vars =dict(*args,**kwargs)
    context =_create_eval_context(template,vars)
    return  {**vars, **context.vars}

def _add_builtin_objects(*args,**kwargs):
    return {**dict(*args,**kwargs),**_builtin_objects}

def _create_eval_context(template,template_vars):
    context =template.new_context(template_vars)
    try:
        s= concat(template.root_render_func(context))
        #merge template_vals with resolve vars at render time
    except Exception:
        #catch the exception as some vars might not be populated yet
        exc_info = sys.exc_info()
    return context
