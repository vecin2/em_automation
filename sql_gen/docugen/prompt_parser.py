import sys
import importlib
from collections import OrderedDict

from jinja2.visitor import NodeTransformer,NodeVisitor
from jinja2 import meta
from jinja2.nodes import Call,Name

from sql_gen.docugen.prompt import Prompt
from sql_gen import logger
from sql_gen.docugen.template_context import TemplateContext
from sql_gen.docugen.template_inliner import TemplateInliner
from sql_gen.docugen.env_builder import TraceUndefined

class PromptParser(object):
    def __init__(self,template):
        logger.debug("Instantiating PromptParser for template '"+ template.name+"'")
        source = TemplateInliner(template).inline()
        self.template = template.environment.from_string(source)
        ast = self.template.environment.parse(source)

        #self.template = template
        #ast = self._join_included_templates(template)

        self.prompt_visitor = PromptVisitor(ast)

    def _inline_included_templates(self,template):
        """consolidates all the included templates in one template"""
        source = TemplateInliner(template).inline()
        return template.environment.from_string(source)

    def _join_included_templates(self,template):
        logger.debug("Joining included templates under one single AST")
        source = self._get_source(template)
        ast = self.template.environment.parse(source)
        exploded_ast =TemplateJoiner(template.environment).visit(ast)
        logger.debug("Finishing joining templates")
        return exploded_ast

    def next_prompt(self,template_values={}):
        context =TemplateContext(self.template,template_values)
        return self.prompt_visitor.next_prompt(context)

    def _get_source(self,template):
            return template.environment.loader.get_source(template.environment,template.name)[0]


#No longer used as TemplateInliner removes all the includes
class TemplateJoiner(NodeTransformer):
    def __init__(self,env):
        self.env = env

    def visit_Include(self,node):
        template_name = node.template.value
        source = self.env.loader.get_source(self.env,template_name)[0]
        #swap the include node for the template tree recursively
        ast1 = self.env.parse(source)
        visited =self.visit(ast1)
        return ast1.body

class PromptVisitor(NodeVisitor):
    def __init__(self,ast):
        logger.debug("Instantiating Prompt visitor")
        self.ast = ast
        self._set_parent(self.ast,None)
        self.names_visited = []
        logger.debug("Finish Prompt visitor instantion")

    def _set_parent(self,node, parent):
        node.parent =parent
        for child in node.iter_child_nodes():
            self._set_parent(child, node)

    def next_prompt(self,eval_context):
        logger.debug("Starting next prompt")
        prompt = self.visit(self.ast, eval_context)
        logger.debug("Prompt returned: "+ str(prompt))
        if prompt:
            logger.debug("Resolving prompt")
            prompt.resolve(eval_context)
        logger.debug("Returning prompt")
        return prompt

    def generic_visit(self, node, template_values={}):
        """Called if no explicit visitor function exists for a node."""
        for node in node.iter_child_nodes():
            prompt =self.visit(node, template_values)
            if prompt:
                return prompt
        return None

    def visit_Filter(self, node,template_values={}):
        prompt=self.generic_visit(node,template_values)
        if prompt:
            DynamicFilter = self.__get_filter_definition(node) 
            if DynamicFilter:
                template_filter = DynamicFilter(node)
                prompt.append_filter(template_filter)
        return prompt

    def __get_filter_definition(self,jinja2_filter):
        filter_name=jinja2_filter.name
        try:
            return getattr(importlib.import_module("sql_gen.sqltask_jinja.filters."+filter_name), filter_name.capitalize()+"Filter") 
        except ModuleNotFoundError as excinfo:
            logger.info("Found filter "+filter_name+" which is not implemented in sqltask")
            return None

    def visit_Name(self,node,template_values={}):
        #Create a prompt for Name nodes which are in part of the undeclare vars
        #and they are not the node value of CallNode
        if node.name not in template_values \
                and node.name in meta.find_undeclared_variables(self.ast)\
                and node.ctx == 'load'\
                and (not isinstance(node.parent,Call) or node.parent.node != node)\
                and not self._has_been_visit(node.name)\
                and self._is_executed(node.name,template_values):
                self.names_visited.append(node.name)
                return Prompt(node.name, [])
        return None

    def _is_executed(self,var_name,template_values):
        try:
            template_values.resolve(var_name)
        except Exception as exc_info:
            if var_name in  TraceUndefined.executed_vars:
                return True
        return False

    def _has_been_visit(self,node_name):
        return node_name in self.names_visited

