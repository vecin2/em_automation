from jinja2.nodes import List,Name,Const
class PromptFilter:
    def _render_args(self,context):
        result=[]
        for arg in self.filter.args:
            result.append(self._render_arg(arg,context))
        return result

    def _render_arg(self,arg,context):
        if isinstance(arg,List):
            return self._render_list(arg,context)
        elif isinstance(arg, Name):
            return context[arg.name]
        elif isinstance(arg,Const):
            return arg.value
        else:
            raise ValueError("Default Filters at the moment only support "+\
                    "constant values, a variable was passed "+str(arg))

    def _render_list(self,arg,context):
            result=[]
            items = [item.value for item in arg.items]
            for item in items:
                result.append(item)
            return result
