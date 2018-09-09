from jinja2 import nodes,meta
from jinja2.nodes import Name
import importlib


class TemplateSource(object):
    def __init__(self,ast):
        self.ast =ast
        self.__set_parent(self.ast,None)

    def __set_parent(self, node,parent):
        node.parent = parent
        for child in node.iter_child_nodes():
            self.__set_parent(child, node)
        return

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
