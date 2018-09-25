import sys,os
from jinja2 import Environment, meta, Template, nodes
from jinja2.nodes import Stmt,Template
from anytree import Node
from sql_gen.sql_gen.filter_loader import load_filters
import pytest


env = Environment()
load_filters(env)

def test_include_templates():
    ast = env.parse("{% include 'add_process_descriptor.sql' %} hola marco")
    template_vars = meta.find_undeclared_variables(ast)
    assert 0  == len(template_vars)
    for field, value in ast.iter_fields():
        assert "body" == field
        assert "Include(template=Const(value='add_process_descriptor.sql'), "+\
                        "with_context=True, "+\
                        "ignore_missing=False)" == str(value[0])

       # assert  "Hello " == value[0]

def test_list_variable_names():
    ast = env.parse('Hello {{ name }}!')
    template_vars = meta.find_undeclared_variables(ast)
    assert "name" == list(template_vars)[0]

def test_fields_and_attribute():
    ast = env.parse('Hello {{ name }}! \n pepe')
    fields=""
    assert 1 == ast.lineno
    for field in ast.fields:
        fields = fields + field
    assert "body" == fields

def test_template_body_structure():
    ast = env.parse('Hello {{ name }}!')
    for field, value in ast.iter_fields():
        assert "body" == field
        assert value == ast.body
        assert "[Output(nodes=[TemplateData(data='Hello '), Name(name='name', ctx='load'), TemplateData(data='!')])]" == str(value)
        assert  "Hello " == value[0].nodes[0].data
        assert  "name" == value[0].nodes[1].name
        assert  "!" == value[0].nodes[2].data


def test_get_description_value():
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    body_string="Output(nodes=[TemplateData(data='Hello '), "+ \
                              "Filter(node=Name(name='name', ctx='load'), "+\
                                     "name='default', "+\
                                     "args=[Const(value='Mundo')], "+\
                                     "kwargs=[], "+\
                                     "dyn_args=None, "+\
                                     "dyn_kwargs=None"+\
                                     "), "+\
                              "TemplateData(data='!')])"
    assert body_string ==str(ast.body[0])
    #field, value = ast.iter_fields()
    for field, value in ast.iter_fields():
        assert "body" == field
        assert  body_string == str(value[0])
        assert  "Hello " == value[0].nodes[0].data
        assert  "default" == value[0].nodes[1].name
        assert  "name" == value[0].nodes[1].node.name
        assert  "!" == value[0].nodes[2].data

def test_pipe_default_descripion_filters():
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    body_string="Output(nodes=[TemplateData(data='Hello '), "+ \
                              "Filter(node=Filter(" +\
                                        "node=Name(name='name', ctx='load'), "+\
                                        "name='default', "+\
                                        "args=[Const(value='Mundo')], "+\
                                        "kwargs=[], "+\
                                        "dyn_args=None, "+\
                                        "dyn_kwargs=None"+\
                                        "), "+\
                                      "name='description', "+\
                                      "args=[Const(value='World in english')], "+\
                                      "kwargs=[], dyn_args=None, "+\
                                      "dyn_kwargs=None"+\
                                      "), "+\
                              "TemplateData(data='!')])"
    

    assert body_string ==str(ast.body[0])

def test_globals():
    ast = env.parse("{% set name = camel()%}Name is {{name}}")
    body_string= "Assign(target=Name(name='name', ctx='store'), "+\
                 "node=Call(node=Name(name='camel', ctx='load'), "+\
                            "args=[], "+\
                            "kwargs=[], "+\
                            "dyn_args=None, "+\
                            "dyn_kwargs=None)"+\
                          ")"

    assert body_string ==str(ast.body[0])

def test_anytree_node():
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    filter_node =ast.body[0].nodes[1]
    assert "description" ==filter_node.name

    description_node = Node("description")
    nameNode = Node("name", parent=description_node, value=filter_node)

    assert "name"== description_node.children[0].name
    assert "description"== description_node.children[0].value.name

    
