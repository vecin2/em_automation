from sql_gen.test.utils.draw_trees import TreeDrawer
from jinja2 import  Environment,Template
from jinja2.compiler import generate
from jinja2.utils import concat

text ='''
{% set martin_name = "Juan"%}
martin is {{name | default(martin_name)}}
lastt name is {{last_name | default("nothing")}}
'''
text="{%set greeting =  'hello'%} {{name}}"

t = Template(text)
print("***printing template rendered****")
print(t.render({}))

tree = t.environment.parse(text)
print("***printing tree****")
TreeDrawer().print_node(tree)
print("****Generated root function****")
print(generate(tree, t.environment, "pedro", "<<ast>>"))
context =t.new_context({})
rendered_text =concat(t.root_render_func(context))
print("context looks like "+str(context))
print("context vars looks like "+str(context.vars))
