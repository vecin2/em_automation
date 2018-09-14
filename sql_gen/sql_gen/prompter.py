from jinja2.visitor import NodeTransformer,NodeVisitor
from jinja2 import meta
import importlib
from collections import OrderedDict

class Prompter(object):
    def __init__(self, env):
        self.env = env

    def get_template_prompts(self, template_name):
        result=[]
        template_source_text = self.env.loader.get_source(self.env,template_name)[0]
        ast = self.env.parse(template_source_text)
        TemplateJoiner(self.env).visit(ast)
        return PromptVisitor(ast).visit(ast)
        #return sorted(undeclare_variables, key=lambda x: list_a.index(x))

    def build_context(self,template_name):
        prompts = self.get_template_prompts(template_name)
        context ={}

        for key, prompt in prompts.items() :
            prompt.populate_value(context)
        return context

class Prompt:
    def __init__(self, variable_name, filter_list):
        self.variable_name =variable_name
        self.filter_list = filter_list

    def get_diplay_text(self):
        self.display_text = self.variable_name
        for template_filter in self.filter_list:
            self.display_text = template_filter.apply(self.display_text);
        return self.display_text+": "

    def append_filter(self, prompt_filter):
        self.filter_list.append(prompt_filter)

    def populate_value(self,context):
        var =input(self.get_diplay_text())
        if var:
            context[self.variable_name] = var

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
        return getattr(importlib.import_module("filters."+filter_name), filter_name.capitalize()+"Filter") 

    def visit_Name(self,node):
        result=OrderedDict()
        #if node.ctx == "load":
        if node.name in meta.find_undeclared_variables(self.ast):
            result[node.name] =Prompt(node.name, [])
        for child in node.iter_child_nodes():
            self.generic_visit(child)
        return result

