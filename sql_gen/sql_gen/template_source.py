from jinja2 import nodes,meta
from anytree import Node
from filters.default import DefaultFilter
import importlib


class TemplateSource(object):
    def __init__(self,ast):
        self.ast =ast
        self.ast_nodes =self.ast.body[0].nodes
        self.root = self.get_root_node()
        self.template_name=""

    def get_template(self):
        return self.template;

    def get_root_node(self):
        self.root=""
        if self.root:
            return self.root
        else:
            self.root = Node("templateRoot")
            for node in self.ast_nodes:
                   self.add_children_nodes(node,self.root)
            return self.root

    def add_children_nodes(self,node,parent):
        node_value = node
        if node_value:
            if (hasattr(node_value, "name")):
                current_node = Node(node_value.name, parent, value=node)
                if hasattr(node_value, "node"):
                     self.add_children_nodes(node_value.node,current_node)

        return


    def get_tree_node_by_name(self,parent,name):
        if not parent.children:
            return None
        for node in parent.children:
            if(node.name == name):
                return node
            else:
                child = self.get_tree_node_by_name(node, name)
                if child:
                    return child
        return

    def find_undeclared_variables(self):
        return meta.find_undeclared_variables(self.ast)

    def get_filters(self, node_name):
        node = self.get_tree_node_by_name(self.root,node_name)
        result=[]
        for current_node in node.ancestors:
            if (hasattr(current_node, "value")) and\
                isinstance(current_node.value, nodes.Filter):
                    DynamicFilter = self.get_filter_definition(current_node.value) 
                    template_filter = DynamicFilter(current_node.value)
                    result.append(template_filter)

        return result

    def get_filter_definition(self,jinja2_filter):
        filter_name=jinja2_filter.name
        return getattr(importlib.import_module("sql_gen.filters."+filter_name), filter_name.capitalize()+"Filter") 
