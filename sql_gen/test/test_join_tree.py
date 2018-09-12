from sql_gen.sql_gen.prompter import Prompter, TemplateJoiner
from jinja2 import Template,meta
from test.util_test_template_env import test_env

env = test_env()
def test_d():
    template_name="include_reuse_var_value.sql"
    template_source_text = env.loader.get_source(env,template_name)[0]
    ast = env.parse(template_source_text)
    undeclare_variables = meta.find_undeclared_variables(ast)
    assert {"last_name","name"} == undeclare_variables
    TemplateJoiner(env).visit(ast)
    undeclare_variables = meta.find_undeclared_variables(ast)
    assert {"last_name","name"} == undeclare_variables

