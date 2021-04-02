from jinja2.nodes import List, Name, Const, Getitem, Getattr
from sql_gen import logger


class PromptFilter:
    def _render_args(self, context):
        result = []
        for arg in self.filter.args:
            result.append(self._render_arg(arg, context))
        return result

    def _render_arg(self, arg, context):
        error_msg = (
            "Filters at the moment only support collections,contants, variables and _keynames. "
            + "But you passed something else, maybe a function? "
        )
        logger.debug(
            "Render argument '" + str(arg) + "' within filter " + self.filter.name
        )
        if isinstance(arg, List):
            result = self._render_list(arg, context)
        elif isinstance(arg, Name):
            #        import pdb;pdb.set_trace()
            result = context.resolve(arg.name)
        elif isinstance(arg, Const):
            result = arg.value
        elif isinstance(arg, Getitem):
            dict = self._render_arg(arg.node, context)
            key = self._render_arg(arg.arg, context)
            result = dict[key]
        elif isinstance(arg, Getattr):
            value = context.resolve(arg.node.name)
            result = value.__getattr__(arg.attr)
        else:
            print(str(arg))
            raise ValueError(error_msg + "\n" + str(arg))
        logger.debug("Argument resolved to: " + str(result))
        return result

    def _render_list(self, arg, context):
        result = []
        items = [self._render_arg(item, context) for item in arg.items]
        for item in items:
            result.append(item)
        return result
