from sql_gen.test.utils.draw_trees import TreeDrawer
from jinja2 import  Environment,Template
from jinja2.lexer import Lexer
from sql_gen.sql_gen.environment_selection import populate_filters

td = TreeDrawer()
env = Environment()
populate_filters(env)
tmpl_source ='''
{% set martin_name = "Juan"%}
martin is {{name | default(martin_name)}}
'''
tmpl = env.from_string(tmpl_source)

ast = env.parse(tmpl_source)
td.print_node(ast)
print("root func "+ str(tmpl.root_render_func.__name__))

context =  {"name":"juan", "desc_name":"the name"}
concat = u''.join

for event in tmpl.root_render_func(tmpl.new_context(context)):
    print ("event "+ event)

#print(some_function())
tmpl.generate()
out = tmpl.render(foo=list(range(10)))
#text="""
#{% set entity_id ="123d" %}
#{% set query = "SELECT CONFIG_ID FROM EVA_PROCESS_DESCRIPTOR WHERE ENTITY_DEF_ID =" + entity_id %}
#this is the query  {{query}}
#{{ config_dd | default(query+"jesus") }} is --config_id
#{{ name | default("david")}}
#"""
#text= """
#{% set query ="jesus"%}
#{{ config_id | default ("hola"+query)}}
#"""
text ='''
{% set martin_name = "Juan"%}
martin is {{name | default(martin_name)}}
lastt name is {{last_name | default("nothing")}}
'''

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

