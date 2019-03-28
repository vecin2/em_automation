from jinja2 import Environment, meta, Template, nodes,FileSystemLoader
import pytest
import os
env = Environment()


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

def test_does_not_strip_block_spaces_by_default():
    env = Environment()
    text='''Hola juan
    {% set name = "pedro" %}
    hola {{name}}
    '''
    t = env.from_string(text)
    assert "Hola juan\n    \n    hola pedro\n    " == t.render({})

def test_strip_block_spaces():
    env = Environment(trim_blocks=True,
                      lstrip_blocks=True,
                      keep_trailing_newline=False #default
                      )
    text='''Hola juan
    {% set name = "pedro" %}
    hola {{name}}
    '''
    
    t = env.from_string(text)
    rendered_text = t.render({})
    print(rendered_text)
    assert "Hola juan\n    hola pedro\n    " == rendered_text

def test_keep_trailing_newline_doesnot_work():
    env = Environment(trim_blocks=True,
                      lstrip_blocks=True,
                      keep_trailing_newline=False #default
                      )
    text='''hola juan
    {% set name = "pedro" %}

    hola {{name}}'''
    
    t = env.from_string(text)
    rendered_text = t.render({})
    print(rendered_text)
    assert "hola juan\n\n    hola pedro" == rendered_text

def test_replicate_issue():
    env = Environment( trim_blocks=True,
                        lstrip_blocks=True
                        )
    #env.globals['camelcase'] = camelcase
    #env.globals['dbquery'] = dbquery
    text='''Hola juan
    {% set name = "pedro" %}
    hola {{name}}
    '''
    t = env.from_string(text)
    assert "Hola juan\n    hola pedro\n    " == t.render({})

def test_string_filter():
    env = Environment(trim_blocks=True,
                      lstrip_blocks=True,
                      keep_trailing_newline=False #default
                      )
    text='{{ None or "pedro"}}'
    t = env.from_string(text)
    rendered_text = t.render({})
    print(rendered_text)
    assert "pedro" == rendered_text


