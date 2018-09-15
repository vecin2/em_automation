from jinja2 import Environment, meta, Template, nodes
import pytest
from sql_gen.sql_gen.filter_loader import load_filters

env = Environment()
load_filters(env)


def test_one_undefined_variable_it_renders_as_empty():
   t = Template("Hello {{ name }}!")
   result = t.render()
   assert "Hello !" == result

def test_simple_variable():
   t = Template("Hello {{ name }}!")
   result = t.render(name="Juan")
   assert "Hello Juan!" == result

def test_two_vars():
   t = Template("Hello {{ name }}. Welcome {{ name_with_title}}!")
   result = t.render(name="Juan",name_with_title="Mr Juan")
   assert "Hello Juan. Welcome Mr Juan!" == result

def test_variable_assignment():
    template_text = """{% set name_with_title = 'Mr '+ name%}
Hello {{ name }}. Welcome {{name_with_title}}!"""
    t = Template(template_text)

    result = t.render(name="Juan")

    assert "\nHello Juan. Welcome Mr Juan!" == result
