from sql_gen.sql_gen.template_source import TemplateSource
from anytree import Node
import pytest
from test.util_test_template_env import test_env
@pytest.fixture
def env():
    return test_env()
     
def test_anytree_node(env):
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    filter_node =ast.body[0].nodes[1]
    assert "description" ==filter_node.name

    description_node = Node("description")
    nameNode = Node("name", parent=description_node, value=filter_node)

    assert "name"== description_node.children[0].name
    assert "description"== description_node.children[0].value.name

def test_find_undeclared_variables_in_the_order_they_appear_within_template(env):
    ast = env.parse("Hello {{ name }}, welcome to {{company_name}}!")
    template_source = TemplateSource(ast)
   
    result = template_source.find_undeclared_variables()
    assert ["name", "company_name"] == result

    description_node = Node("description")
    nameNode = Node("name", parent=description_node, value=filter_node)

    assert "name"== description_node.children[0].name
    assert "description"== description_node.children[0].value.name


def test_traverse_template_nodes(env):
    ast = env.parse("Hello {{ prename }} {{ name | default ('Mundo') | description ('World in english') }}!")
    template_source = TemplateSource(ast)
    root_node = template_source.get_root_node()
    assert "Node('/templateRoot')" == str(root_node)
    assert "Name(name='prename', ctx='load')" == str(root_node.children[0].value)
    assert "Filter(node=Filter(node=Name(name='name', ctx='load'), "+\
                               "name='default', "+\
                               "args=[Const(value='Mundo')], "+\
                               "kwargs=[], "+\
                               "dyn_args=None, "+\
                               "dyn_kwargs=None), "+\
                   "name='description', "+\
                   "args=[Const(value='World in english')], "+\
                   "kwargs=[], "+\
                   "dyn_args=None, "+\
                   "dyn_kwargs=None)" == str(root_node.children[1].value)
    assert "Filter(node=Name(name='name', ctx='load'), "+\
                  "name='default', "+\
                  "args=[Const(value='Mundo')], "+\
                  "kwargs=[], "+\
                  "dyn_args=None, "+\
                  "dyn_kwargs=None)" == str(root_node.children[1].children[0].value)
    assert "Name(name='name', ctx='load')" == str(root_node.children[1].children[0].children[0].value)

@pytest.mark.skip(reason="until refactored complete")
def test_find_undeclared_variables_finds_nclude_templates(env):
    ast = env.parse("{% include 'introduction.sql' %}")
    templateSource = TemplateSource(ast)
    variables = templateSource.find_undeclared_variables()
    assert 2 == len(variables)
    

