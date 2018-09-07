from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.prompter import Prompter
import pytest

from test.util_test_template_env import test_env
#@pytest.fixture
#def env():
#    return test_env()
env=test_env()

def run_test(display_msgs, template_source_text):
    prompter = Prompter(env)
    prompts = prompter.get_prompts(template_source_text)
    assert_equals_prompt_text_list(display_msgs, prompts)

def assert_equals_prompt_text_list(questions, prompts):
    assert len(questions) == len(prompts)
    counter =0
    for question in questions:
        assert_equal_prompt_text(question,prompts[counter])
        counter+=1

def assert_equal_prompt_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()

def test_prompt_default():
    run_test(["name (default is Mundo)"],
              "Hello {{ name | default ('Mundo') }}!")

def test_prompt_description():
    run_test(["customer name"],
              "Hello {{ name | description ('customer name') }}")


def test_pipe_default_descripion_filters():
    run_test(["prename","World in english (default is Mundo)"],
              "Hello {{ prename }} {{ name | default ('Mundo') | description ('World in english') }}!")

#@pytest.mark.skip
#def test_get_description_value_when_multiple_vars(env):
#    ast = env.parse("Hello {{ prename }} {{ name | description ('first name') }}!")
#    prompter = build_prompter(ast)
#    prompts = prompter.get_prompts()
#
#    assert_display_text("prename", prompts[0])
#    assert_display_text("first name", prompts[1])
#
