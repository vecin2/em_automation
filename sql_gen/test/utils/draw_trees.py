from jinja2 import Template
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

#text="""
#{% set entity_id ="123d" %}
#{% set query = "SELECT CONFIG_ID FROM EVA_PROCESS_DESCRIPTOR WHERE ENTITY_DEF_ID =" + entity_id %}
#this is the query  {{query}}
#{{ config_dd | default(query+"jesus") }} is --config_id
#{{ name | default("david")}}
#"""
text= """
{% set query ="jesus"%}
{{ config_id | default ("hola"+query)}}
"""

t = Template(text)
print("***printing template rendered****")
print(t.render({}))
import ast
from jinja2.compiler import generate
from jinja2.nodes import Name
ast 

tree = t.environment.parse(text)
print(str(tree))
print("***printing tree****")
TreeDrawer().print_node(tree)
print("***rendering template****")
print(t.render())
add_exp =tree.body[2].nodes[1].args[0]
print("this is "+ generate(tree, t.environment, "pedro", "<<ast>>"))
#def generate(node, environment, name, filename, stream=None,
#             defer_init=False, optimized=True):
#add_exp = ast.parse(add_exp)
#exec(compile(add_exp,filename="<ast>",mode="exec"))
#print(str(add_exp))
#exec(t.environment.compile(ast,

