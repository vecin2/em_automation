from sql_gen.test.utils.draw_trees import TreeDrawer
from jinja2 import  Environment,Template
from jinja2.compiler import generate
from jinja2.utils import concat
from sql_gen.sql_gen.environment_selection import  EMTemplatesEnv

text ='''
 {% set tmp_pd_type = process_descriptor_type      | description('type_id (0=regular process, 2=action, 3=sla)')
					           | default("hesus") %}
{% set suggested_ext_path ="suggestion" %}
 {% set repository_path =         tmp_repo_path | codepath()
						   | default (suggested_ext_path) %}
'''
env = EMTemplatesEnv().get_env()
t =env.from_string(text)
#t = Template(text)
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
