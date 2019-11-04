from sql_gen.test.utils.draw_trees import TreeDrawer
from jinja2 import  Environment,Template
from jinja2.compiler import generate
from jinja2.utils import concat
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv


text ='''
 {% set tmp_pd_type = process_descriptor_type      | description('type_id (0=regular process, 2=action, 3=sla)')
					           | default("hesus") %}
{% set suggested_ext_path ="suggestion" %}
 {% set repository_path =         tmp_repo_path | codepath()
						   | default (suggested_ext_path) %}
'''
text=""""
Hi {{ surname | description("Please enter surname") }} and welcome back Mrs {{ surname }}
"""
env = EMTemplatesEnv().make_env("/home/dgarcia/dev/python/em_automation/sql_gen/templates")
#t =env.from_string(text)
#t = env.get_template("dynamic.sql")
t = env.get_template("add_dynamic_content_verb.sql")
#t = Template(text)
print("***printing template rendered****")
print(t.render({"entity_name":"ContactED"}))

#text = env.loader.get_source(env,"dynamic.sql")[0]
#text = env.loader.get_source(env,"entity_def.sql")[0]
text = env.loader.get_source(env,"add_dynamic_content_verb.sql")[0]
#self.env.parse(template_source_text)
tree = t.environment.parse(text)
print("***printing tree****")
#TreeDrawer().print_node(tree)
print("****Generated root function****")
print(generate(tree, t.environment, "pedro", "<<ast>>"))
context =t.new_context({})
#rendered_text =concat(t.root_render_func(context))
print("context looks like "+str(context))
print("context vars looks like "+str(context.vars))
