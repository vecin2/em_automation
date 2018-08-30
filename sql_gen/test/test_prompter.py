from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.prompter import Prompter
import pytest

from test.util_test_template_env import test_env
@pytest.fixture
def env():
    return test_env()

def build_prompter(ast):
    return Prompter(TemplateSource(ast))
    
def test_prompt_default(env):
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    prompter = build_prompter(ast)

    prompts = prompter.get_prompts()

    assert 1 == len(prompts)
    assert_display_text("name (default is Mundo)", prompts[0])

def test_prompt_description(env):
    ast = env.parse("Hello {{ name | description ('customer name') }}!")
    prompter = build_prompter(ast)

    prompts = prompter.get_prompts()
    assert 1 == len(prompts)
    assert_display_text("customer name", prompts[0])


def test_get_description_value_when_multiple_vars(env):
    ast = env.parse("Hello {{ prename }} {{ name | description ('first name') }}!")
    prompter = build_prompter(ast)
    prompts = prompter.get_prompts()

    assert_display_text("prename", prompts[0])
    assert_display_text("first name", prompts[1])

def test_pipe_default_descripion_filters(env):
    ast = env.parse("Hello {{ prename }} {{ name | default ('Mundo') | description ('World in english') }}!")
    prompter = build_prompter(ast)
    prompts = prompter.get_prompts()

    assert_display_text("prename", prompts[0])
    assert_display_text("World in english (default is Mundo)", prompts[1])

def assert_display_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()
