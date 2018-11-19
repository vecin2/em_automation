from sql_gen.logger import logger
from sql_gen.sql_gen.template_context import TemplateContext
from jinja2.visitor import NodeTransformer,NodeVisitor
from jinja2 import meta
from jinja2.nodes import Call,Name
import importlib
from collections import OrderedDict
from sql_gen.sql_gen.prompt import Prompt
import sys

class PromptParser(object):
    def __init__(self,template):
        logger.debug("Instantiating PromptParser for template '"+ template.name+"'")
        self.template =template
        ast = self._join_included_templates(template)
        self.prompt_visitor = PromptVisitor(ast)

    def _join_included_templates(self,template):
        logger.debug("Joining included templates under one single AST")
        ast =self._extract_template_ast(template)
        TemplateJoiner(self.env).visit(ast)
        logger.debug("Finishing joining templates")
        return ast

    def _extract_template_ast(self,template):
        self.template_name = template.name
        self.env =template.environment
        template_source_text = self.env.loader.get_source(self.env,self.template_name)[0]
        return self.env.parse(template_source_text)

    def next_prompt(self,template_values={}):
        context =TemplateContext(self.template,template_values)
        return self.prompt_visitor.next_prompt(context)

class TemplateJoiner(NodeTransformer):
    def __init__(self,env):
        self.env = env

    def visit_Include(self,node):
        template_name = node.template.value
        source = self.env.loader.get_source(self.env,template_name)[0]
        #swap the include nodor for the template tree
        return self.env.parse(source).body[0]

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
            template_filter = DynamicFilter(node)
            prompt.append_filter(template_filter)
        return prompt

    def __get_filter_definition(self,jinja2_filter):
        filter_name=jinja2_filter.name
        return getattr(importlib.import_module("sql_gen.sqltask_jinja.filters."+filter_name), filter_name.capitalize()+"Filter") 

    def visit_Name(self,node,template_values={}):
        #Create a prompt for Name nodes which are in part of the undeclare vars
        #and they are not the node value of CallNode
        if node.name not in template_values \
                and node.name in meta.find_undeclared_variables(self.ast)\
                and (not isinstance(node.parent,Call) or node.parent.node != node)\
                and not self._has_been_visit(node.name):
                self.names_visited.append(node.name)
                return Prompt(node.name, [])
        return None

    def _has_been_visit(self,node_name):
        return node_name in self.names_visited

