import sys
import importlib

from jinja2.visitor import NodeTransformer, NodeVisitor
from jinja2 import meta
from jinja2.nodes import Call

from sql_gen.docugen.prompt import Prompt
from sql_gen import logger
from sql_gen.docugen.template_context import TemplateContext
from sql_gen.docugen.env_builder import TraceUndefined


# No longer used as TemplateInliner removes all the includes
class TemplateJoiner(NodeTransformer):
    def __init__(self, env):
        self.env = env

    def visit_Include(self, node):
        template_name = node.template.value
        source = self.env.loader.get_source(self.env, template_name)[0]
        # swap the include node for the template tree recursively
        ast1 = self.env.parse(source)
        visited = self.visit(ast1)
        return ast1.body


class PromptVisitor(NodeVisitor):
    def __init__(self, ast):
        logger.debug("Instantiating Prompt visitor")
        self.ast = ast
        self._set_parent(self.ast, None)
        # need to track visited names when the user enter blank
        # then the variable should not added to the values and
        # neither should be prompted again
        self.names_visited = []
        logger.debug("Finish Prompt visitor instantion")

    def _set_parent(self, node, parent):
        node.parent = parent
        for child in node.iter_child_nodes():
            self._set_parent(child, node)

    def next_prompt(self, eval_context):
        logger.debug("Starting next prompt")
        prompt = self.visit(self.ast, eval_context)
        logger.debug("Prompt returned: " + str(prompt))
        if prompt:
            logger.debug("Resolving prompt")
            prompt.resolve(eval_context)
        logger.debug("Returning prompt")
        return prompt

    def generic_visit(self, node, template_values={}):
        """Called if no explicit visitor function exists for a node."""
        for node in node.iter_child_nodes():
            prompt = self.visit(node, template_values)
            if prompt:
                return prompt
        return None

    def visit_Filter(self, node, template_values={}):
        prompt = self.generic_visit(node, template_values)
        if prompt:
            DynamicFilter = self.__get_filter_definition(node)
            if DynamicFilter:
                template_filter = DynamicFilter(node)
                prompt.append_filter(template_filter)
        return prompt

    def __get_filter_definition(self, jinja2_filter):
        filter_name = jinja2_filter.name
        try:
            return getattr(
                importlib.import_module("sql_gen.sqltask_jinja.filters." + filter_name),
                filter_name.capitalize() + "Filter",
            )
        except ModuleNotFoundError as excinfo:
            logger.info(
                "Found filter " + filter_name + " which is not implemented in sqltask"
            )
            return None

    def visit_Name(self, node, template_values={}):
        # Create a prompt for Name nodes which are in part of the undeclare vars
        # and they are not the node value of CallNode
        if (
            node.name not in template_values
            and node.name in meta.find_undeclared_variables(self.ast)
            and node.ctx == "load"
            and (not isinstance(node.parent, Call) or node.parent.node != node)
            and node.name not in template_values
            and self._is_executed(node.name, template_values)
        ):
            self.names_visited.append(node.name)
            return Prompt(node.name, [])
        return None

    def _is_executed(self, var_name, template_values):
        try:
            template_values.resolve(var_name)
        except Exception as exc_info:
            if var_name in TraceUndefined.executed_vars:
                return True
        return False

    def _has_been_visit(self, node_name):
        return node_name in self.names_visited
