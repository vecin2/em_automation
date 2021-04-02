from sql_gen.test.utils.draw_trees import TreeDrawer
from jinja2 import Environment, Template
from jinja2.lexer import Lexer
from sql_gen.sql_gen.environment_selection import populate_filters

td = TreeDrawer()
env = Environment()
populate_filters(env)
tmpl_source = """
{% set old_pocess_descriptor = adquery("SELECT * FROM EVA_VERB V, EVA_PROCESS_DESCRIPTOR PD, EVA_PROCESS_DESC_REFERENCE PDR, CCADMIN_IDMAP IDMAP WHERE V.PROCESS_DESC_REF_ID = PDR.ID AND PDR.PROCESS_DESCRIPTOR_ID = PD.ID AND IDMAP.ID = V.ENTITY_DEF_ID and IDMAP.KEYSET ='ED' AND V.NAME ='"+verb_name+"' and IDMAP.KEYNAME = '"+entity_def_id+"'") %}
{{config_id | default(old_pocess_descriptor["CONFIG_ID"])}}
{{config_id | default(name)}}
{%set dict = {"name":"pedro"}%}
{{config_id | default(dict["name"])}}
"""
tmpl = env.from_string(tmpl_source)

ast = env.parse(tmpl_source)
td.print_node(ast)
