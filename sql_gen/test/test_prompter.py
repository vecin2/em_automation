import pytest
from sql_gen.sql_gen.prompter import Prompter
from jinja2 import DictLoader,Environment
from sql_gen.sql_gen.environment_selection import populate_filters

def assert_display_msgs_for_first_template(display_msgs,templates):
    env = Environment(
        loader=DictLoader(templates))
    populate_filters(env)
    template_name =next(iter(templates))
    prompter = Prompter(env.get_template(template_name))
    prompts = prompter.get_template_prompts()
    assert_equals_prompt_text_list(display_msgs, prompts)

def assert_equal_prompts( expected_prompts, actual_prompts):
    assert len(expected_prompts) == len(actual_prompts)
    for expected_prompt in expected_prompts:
        actual_prompt = actual_prompts[expected_prompt[0]]
        assert expected_prompt[1]+": " == actual_prompt.get_diplay_text() 
        assert expected_prompt[2] == actual_prompt.get_suggestions()

def get_prompts_for_first_template(templates):
    env = Environment(
        loader=DictLoader(templates))
    populate_filters(env)
    template_name =next(iter(templates))
    prompter = Prompter(env.get_template(template_name))
    return prompter.get_template_prompts()

def get_prompts(template_text):
    templates={'one_template':template_text}
    return get_prompts_for_first_template(templates)

def assert_display_msgs(display_msgs, template_text):
    prompts = get_prompts(template_text)
    assert_equals_prompt_text_list(display_msgs, prompts)

def assert_equals_prompt_text_list(questions, prompts):
    assert len(questions) == len(prompts)
    counter =0
    for key in prompts:
        assert_equal_prompt_text(questions[counter],prompts[key])
        counter+=1

def assert_equal_prompt_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()

def test_no_vars_prompts_nothing():
    assert_display_msgs([],
                 "Hello World!")

def test_var_prompts_var_name():
    assert_display_msgs(['name'],
                 "Hello {{name}}!")

def test_default_displays_default_value(): 
    assert_display_msgs(["name (default is Mundo)"],
                 "Hello {{ name | default ('Mundo') }}!")

def test_description_prompts_description_intead_of_var_name():
    template_text="Hello {{ name | description ('customer name') }}"
    display_msgs=['customer name']
    assert_display_msgs(display_msgs, template_text)

def test_default_piped_with_description_then_desc_overrides_default():
    template_text="Hello {{ prename }} {{ name | default ('Mundo') | description ('World in english')}}!"
    display_msgs=["prename","World in english"]
    assert_display_msgs(display_msgs, template_text)

def test_pipe_descripion_default_filters():
    template_text="Hello {{ prename }} {{ name | description ('World in english') | default ('Mundo')}}!"
    display_msgs=["prename","World in english (default is Mundo)"]
    assert_display_msgs(display_msgs, template_text)

def test_duplicate_var_name_prompts_only_once_and_it_uses_first_one():
    template_text='Hola {{name | default("Marco")}}!,  {{name}}'
    display_msgs=['name (default is Marco)']
    assert_display_msgs(display_msgs, template_text)

def test_should_not_prompt_var_which_has_value_assigned():
    template_text= "{% set process_descriptor_ref_id = process_descriptor_id %}"
    display_msgs=["process_descriptor_id"]
    assert_display_msgs(display_msgs, template_text)

def test_prompts_var_passed_to_global_function():
    template_text="{% set name = camel(a_var)%}"
    display_msgs=["a_var"]
    assert_display_msgs(display_msgs, template_text)

def test_include_should_prompt_vars_from_included_template_in_order():
    templates={
     "main_template" : "{% include 'hello_world' %}.  I am Juan {{last_name}}",
     "hello_world"   : "Hello {{ name }}!"
     }
    display_msgs=["name","last_name"]
    assert_display_msgs_for_first_template(display_msgs,templates)

def test_should_not_prompt_var_which_is_set_within_included_template():
    templates={
     "main_template" : "{% include 'set_name' %}.  I am Juan {{last_name}}",
     "set_name"      : "{% set name = 'Juan' %}!"
     }
    display_msgs=["last_name"]
    assert_display_msgs_for_first_template(display_msgs,templates)

def test_suggest_should_populate_prompt_suggestions():
    template_text="{{ name | suggest([1,2])}}"
    expected_prompts = [["name","name",[1,2]]]
    prompts = get_prompts(template_text)
    #test that when inovke multiple times does not kep adding
    #display text or suggestions
    prompts["name"].get_diplay_text()
    assert_equal_prompts(expected_prompts, prompts)

@pytest.mark.skip
def test_suggest_should_populate_prompt_suggestions_from_vars():
    template_text="{%set suggestions =['David','John']%} {{ name | suggest(suggestions)}}"
    expected_prompts = [["name","name",[1,2]]]
    prompts = get_prompts(template_text)
    #test that when inovke multiple times does not kep adding
    #display text or suggestions
    prompts["name"].get_diplay_text()
    assert_equal_prompts(expected_prompts, prompts)
    
