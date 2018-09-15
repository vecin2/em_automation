from sql_gen.sql_gen.prompter import PromptVisitor
from jinja2 import Template
import pytest

t = Template("")
def parse(template_text):
    return  t.environment.parse(template_text)

def get_prompts(ast):
    return PromptVisitor(ast).visit(ast)

def test_visit_Default_add_default_val_to_display_text_is_param_is_a_constant():
        prompts = get_prompts(parse("{{name | default('david')}}"))
        assert "name (default is david): " == prompts['name'].get_diplay_text()

def test_visit_Default_allow_constant_exp():
        prompts = get_prompts(parse("{{name | default('david' + ' alvarez') }}"))
        assert "name (default is david alvarez): " == prompts['name'].get_diplay_text()

def test_visit_Default_throws_exception_if_parameter_is_a_variable():
    with pytest.raises(ValueError) as e_info:
        prompts = get_prompts(parse("{% set variable = 'Jose' %} {{name | default(variable) }}"))
        prompts['name'].get_diplay_text()
    assert "Default Filters at the moment only support constant values" in str(e_info.value)

