from jinja2.nodes import List,Name,Const,Getitem
from sql_gen import logger

class PromptFilter:
    def _render_args(self,context):
        result=[]
        for arg in self.filter.args:
            result.append(self._render_arg(arg,context))
        return result

    def _render_arg(self,arg,context):
        logger.debug("Render argument '"+str(arg)+"' within filter "+self.filter.name)
        if isinstance(arg,List):
            result = self._render_list(arg,context)
        elif isinstance(arg, Name):
            result = context.resolve(arg.name)
        elif isinstance(arg,Const):
            result = arg.value
        elif isinstance(arg,Getitem):
            dict = self._render_arg(arg.node,context)
            key = self._render_arg(arg.arg,context)
            result = dict[key]
        else:
            raise ValueError("Filters at the moment only support collections,contants and variables."+\
                    "But you passed something else, maybe a function? "+str(arg))
        logger.debug("Argument resolved to: "+ str(result))
        return result

    def _render_list(self,arg,context):
            result=[]
            items = [self._render_arg(item,context) for item in arg.items]
            for item in items:
                result.append(item)
            return result
