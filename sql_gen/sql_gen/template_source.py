from jinja2 import nodes,meta, Template
from jinja2.nodes import Name, Filter
import importlib
from jinja2.visitor import NodeTransformer,NodeVisitor
from sql_gen.sql_gen.prompter import Prompt

class TreeDrawer(object):
    def __init__(self):
        self.draw =""

    def get_drawer(self, node):
        """Return the visitor function for this node or `None` if no visitor
        exists for this node.  In that case the generic visit function is
        used instead.
        """
        method = 'draw_' + node.__class__.__name__
        return getattr(self, method, None)

    def draw_Include(self,node):
        return "Include("+node.template.value+")"

    def draw_Filter(self,node):
        return "Filter("+node.name+")"
    
    def draw_node(self,node):
        draw_func = self.get_drawer(node) 
        if draw_func is not None:
            return draw_func(node)
        return self.generic_draw(node)

    def generic_draw(self,node):
        return str(node)

    def visit(self,node):
        self.generic_visit(node,"+--")

    def print_node(self,node):
        self.visit(node)
        print(self.draw)

    def generic_visit(self,node,spacer):
        self.draw += spacer + self.draw_node(node) +"\n"
        spacer = "    " + spacer
        for node in node.iter_child_nodes():
            self.generic_visit(node,spacer)

class TemplateJoiner(NodeTransformer):
    def __init__(self,env):
        self.env = env

    def visit_Include(self,node):
        template_name = node.template.value
        source = self.env.loader.get_source(self.env,template_name)[0]
        #swap the include for the actual template source tree
        return self.env.parse(source).body[0]

class PromptVisitor(NodeVisitor):
    def generic_visit(self, node, *args, **kwargs):
        result=[]
        """Called if no explicit visitor function exists for a node."""
        for node in node.iter_child_nodes():
            result.extend(self.visit(node, *args, **kwargs))
        return result

    def visit_Filter(self, node):
        result=self.generic_visit(node)
        for prompt in result:
            DynamicFilter = self.__get_filter_definition(node) 
            template_filter = DynamicFilter(node)
            prompt.append_filter(template_filter)

        return result

    def __get_filter_definition(self,jinja2_filter):
        filter_name=jinja2_filter.name
        return getattr(importlib.import_module("sql_gen.filters."+filter_name), filter_name.capitalize()+"Filter") 

    def visit_Name(self,node):
        result=[]
        if node.ctx == "load":
            result.append(Prompt(node.name, []))
        for child in node.iter_child_nodes():
            self.generic_visit(child)
        return result

class TemplateSource(object):
    def __init__(self,template_name, env):
        t = self.__get_template_with_source(env, template_name)
        self.template_source_text = t.source
        self.ast = env.parse(self.template_source_text)
        parsed_template = t.render({})
       # TreeDrawer().print_node(self.ast)
       # print("**********************************************")
        self.__set_parent(self.ast,None)
        TemplateJoiner(env).visit(self.ast)
       # TreeDrawer().print_node(self.ast)

    def __get_template_with_source(self, env, template_name):
        t = env.get_template(template_name)
        t.source = env.loader.get_source(env,template_name)[0]
        return t    

    def __set_parent(self, node,parent):
        node.parent = parent
        for child in node.iter_child_nodes():
            self.__set_parent(child, node)
        return

    def get_prompts(self):
        return PromptVisitor().visit(self.ast)

    def __get_undeclared_variables(self,prompts):
        result=[]
        for prompt in prompts:
            result.append(prompt.variable_name)
        return result
    def __get_display_text(self,prompts):
        result=[]
        for prompt in prompts:
            result.append(prompt.get_diplay_text())
        return result
    def __sort_by_order_of_appearance(self,prompts):
        undeclare_variables = self.__get_undeclared_variables(prompts)
        display_msgs = self.__get_display_text(prompts)
        list_a = self.template_source_text.split()
        print("*********** undeclare_variables"+ str(undeclare_variables))
        print("*********** display_msgs"+ str(display_msgs))
        #sorted_vars =sorted(undeclare_variables, key=lambda x: list_a.index(x))
        return self.__sort_prompts_by_var_names(prompts, list_a)

    def __sort_prompts_by_var_names(self, prompts, sorted_vars):
        result =[]
        dictionary = {}
        for prompt in prompts:
            dictionary[prompt.variable_name] = prompt
        for variable in sorted_vars:
            if dictionary.get(variable) is not None:
                result.append(dictionary[variable])

        return result

    def get_ordered_undefined_variables(self):
        undeclare_variables = meta.find_undeclared_variables(self.ast)
        list_a = self.template_source_text.split()
        return sorted(undeclare_variables, key=lambda x: list_a.index(x))

