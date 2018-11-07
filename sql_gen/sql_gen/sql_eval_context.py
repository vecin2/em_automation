import sys
from sql_gen.queries.queries import Keynames,EntityDefinition,ProcessDescriptor
from jinja2.utils import concat
from sql_gen.logger import logger

_builtin_objects={'_keynames':Keynames(),
                  '_ed'      :EntityDefinition(),
                  '_pd'      :ProcessDescriptor()
                 }
def initialContext():
    #build a copy 
    return dict(_builtin_objects)

#The eval context keeps a  spcial key "__exception" whih setting up an exception
#which then can be rethrow instead of throwing keyError
#This is because the exception is relevant only if we are not able to resolve a var
class EvalContext(dict):
    def __init__(self, *args, **kw):
        super(EvalContext,self).__init__(*args, **kw)
        self.itemlist = super(EvalContext,self).keys()

    def __getitem__(self,key):
        if key not in self:
            if '__exception' in self:
                print("dict does not contay key: "+ str(key) +"with dict"+ str(dict))
                exception = super(EvalContext,self).__getitem__('__exception')
                raise exception
            else:
                raise Exception("Unable to  resolve '"+key+"'. Please review the template and make sure this var has a value assigned")
        else:
            return super(EvalContext,self).__getitem__(key)

def prepare_eval_context(template,*args, **kwargs):
    logger.debug("Starting preparing eval context")
    vars =dict(*args,**kwargs)
    context =_create_eval_context(template,vars)
    logger.debug("Finish preparing eval context")
    combined_dict = {**vars, **context.vars}
    return EvalContext(combined_dict)

def _add_builtin_objects(*args,**kwargs):
    return {**dict(*args,**kwargs),**_builtin_objects}

def _create_eval_context(template,template_vars):
    context =template.new_context(template_vars)
    try:
        logger.debug("Start rendering template to resolve arguments")
        s= concat(template.root_render_func(context))
        logger.debug("End rendering")
        #merge template_vals with resolve vars at render time
    except Exception as exception:
        #catch the exception as some vars might not be populated yet
       exc_info = sys.exc_info()
       context.vars['__exception']=exception
       logger.error("Error occur while rendering. This might be expected as we are rendering with a context which is not filled yet")
    return context
