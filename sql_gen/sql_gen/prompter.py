from jinja2.visitor import NodeTransformer,NodeVisitor
from jinja2 import meta
from jinja2.nodes import Call,Name
import importlib
from collections import OrderedDict
from sql_gen.sql_gen.prompt import Prompt
class Prompter(object):
    def __init__(self, template):
        self.template_name = template.name
        self.env =template.environment

    def get_template_prompts(self):
        result=[]
        template_source_text = self.env.loader.get_source(self.env,self.template_name)[0]
        ast = self.env.parse(template_source_text)
        TemplateJoiner(self.env).visit(ast)
        return PromptVisitor(ast).visit(ast)
        #return sorted(undeclare_variables, key=lambda x: list_a.index(x))

    def build_context(self):
        prompts = self.get_template_prompts()
        context ={}

        for key, prompt in prompts.items() :
            prompt.populate_value(context)
        return context


class TemplateJoiner(NodeTransformer):
    def __init__(self,env):
        self.env = env

    def visit_Include(self,node):
        template_name = node.template.value
        source = self.env.loader.get_source(self.env,template_name)[0]
        #swap the include for the actual template source tree
        return self.env.parse(source).body[0]

class PromptVisitor(NodeVisitor):
    def __init__(self,ast):
        self.ast = ast
        self._set_parent(self.ast,None)

    def _set_parent(self,node, parent):
        node.parent =parent
        for child in node.iter_child_nodes():
            self._set_parent(child, node)

    def generic_visit(self, node, *args, **kwargs):
        result=OrderedDict()
        """Called if no explicit visitor function exists for a node."""
        for node in node.iter_child_nodes():
            node_prompts =self.visit(node, *args, **kwargs)
            #override child nodes with existing values before
            #merging back in result
            node_prompts.update(result)
            result.update(node_prompts)
        return result

    def visit_Filter(self, node):
        result=self.generic_visit(node)
        for key, prompt in result.items():
            DynamicFilter = self.__get_filter_definition(node) 
            template_filter = DynamicFilter(node)
            prompt.append_filter(template_filter)

        return result

    def __get_filter_definition(self,jinja2_filter):
        filter_name=jinja2_filter.name
        return getattr(importlib.import_module("sql_gen.filters."+filter_name), filter_name.capitalize()+"Filter") 

    def visit_Name(self,node):
        result=OrderedDict()
        #if node.ctx == "load":
        #camel() --> Call(node=Name(name='camel', ctx='load'),args...
        #Creat a prompt for Name nodes which are in part of the undeclare vars
        #and they are not the node value of CallNode
        if node.name in meta.find_undeclared_variables(self.ast):
            if not isinstance(node.parent,Call) or node.parent.node != node:
                result[node.name] =Prompt(node.name, [])
        return result

