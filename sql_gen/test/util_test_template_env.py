from jinja2 import Environment, meta, Template, nodes, FileSystemLoader, select_autoescape
from sql_gen.sql_gen.filter_loader import load_filters
import os

def test_env():
    dirname = os.path.dirname(__file__)
    templates_path = "./"+os.path.join(dirname, 'templates')
    env = Environment(
    loader=FileSystemLoader("/home/dgarcia/dev/python/em_automation/sql_gen/test/templates"),
    autoescape=select_autoescape(['html', 'xml']))
    load_filters(env)
    return env

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

