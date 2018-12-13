import pytest
from jinja2 import Template,Environment
from jinja2.utils import concat
from sql_gen import logger
from sql_gen.docugen.template_context import TemplateContext



def test_resolve_eval_var():
    text ="{%set name= 'David' %} {{name}}"
    template = Template(text)
    context = TemplateContext(template)

    assert "David" == context.resolve("name")

def test_resolve_var_passed():
    initial_context={"name":"John"}
    template = Template("display_name | default(name)")
    context = TemplateContext(template, initial_context)
    assert "John" == context.resolve("name")

def test_wrong_design_template_throw_exception():
    #we are  writting a template as if name would be an object and present
    #in the context already, but that should fail
    template = Template("hola {{name.value}}")
    context = TemplateContext(template)
    with pytest.raises(Exception) as exc_info:
       context.resolve("name")

    assert "'name' is undefined" == str(exc_info.value)

def test_resolve_should_not_exc_if_error_occurs_after_var_is_resolve():
    text ="{%set greeting= 'hello'%} {{greeting }}{{name.capitalize()}}"
    env = Environment()
    template = Template(text)
    context = TemplateContext(template)
    assert "hello" == context.resolve("greeting")


def test_check_value_is_already_in_context():
    initial_context={"name":"John"}
    context = TemplateContext(None,initial_context)
    assert "name" in context

