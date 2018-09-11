from jinja2 import nodes,meta
from jinja2.nodes import Name
import importlib
from jinja2.visitor import NodeTransformer

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

class TemplateSource(object):
    def __init__(self,template_source_text,env):
        self.template_source_text = template_source_text
        self.ast = env.parse(template_source_text)
       # TreeDrawer().print_node(self.ast)
       # print("**********************************************")
        self.__set_parent(self.ast,None)
        TemplateJoiner(env).visit(self.ast)
       # TreeDrawer().print_node(self.ast)


    def __set_parent(self, node,parent):
        node.parent = parent
        for child in node.iter_child_nodes():
            self.__set_parent(child, node)
        return

    def get_ordered_undefined_variables(self):
        undeclare_variables = meta.find_undeclared_variables(self.ast)
        list_a = self.template_source_text.split()
        return sorted(undeclare_variables, key=lambda x: list_a.index(x))

    def get_filters(self, node_name):
        node = self.__get_tree_node_by_name(self.ast,node_name)
        result=[]
        for current_node in self.__ancestors(node):
            if (isinstance(current_node, nodes.Filter)):
                    DynamicFilter = self.__get_filter_definition(current_node) 
                    template_filter = DynamicFilter(current_node)
                    result.append(template_filter)

        return result

    def __get_tree_node_by_name(self,parent,name):
        for node in parent.iter_child_nodes():
            if(isinstance(node,Name) and node.name == name):
                return node
            else:
                child = self.__get_tree_node_by_name(node, name)
                if child:
                    return child
        return

    def __ancestors(self, node):
        result=[]
        while node.parent is not None:
            result.append(node.parent)
            node = node.parent
        return result


    def __get_filter_definition(self,jinja2_filter):
        filter_name=jinja2_filter.name
        return getattr(importlib.import_module("sql_gen.filters."+filter_name), filter_name.capitalize()+"Filter") 
