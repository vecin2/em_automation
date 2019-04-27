from sql_gen.test.utils.prompt_builder import _TestPromptBuilder
import pytest


def template(source):
    return _TestPromptBuilder(source)

def test_no_vars_prompts_nothing():
    template("Hello World").with_values({}).does_not_prompt()

def test_var_prompts_var_name():
    template_vars={}
    template("hello {{name}}")\
            .with_values(template_vars)\
            .should_prompt_next("name")
    #it does not modify context
    assert {} == template_vars

def test_should_prompt_vars_until_all_values_are_filled():
    template("hello {{name}} {{last_name}}").with_values({})\
            .should_prompt_next("name")\
            .with_values({"name":"John"})\
            .should_prompt_next("last_name")\
            .with_values({"name":"John", "last_name":"Smith"})\
            .does_not_prompt()

def test_default_zero_should_default_to_zero():
    template("{{name | default (0)}}").with_values({})\
                                       .should_prompt_next("name (default is 0)")

def test_default_displays_default_value():
    template("{{name | default ('World')}}").with_values({})\
                                       .should_prompt_next("name (default is World)")

def test_default_should_resolve_var():
    template("{% set my_name = 'David'%}{{ name | default(my_name)}}")\
            .with_values({})\
            .should_prompt_next("name (default is David)")

def test_default_should_resolve_dict():
    template("{%set dict = {'name':'Pedro'}%} {{name | default(dict['name'])}}")\
            .with_values({})\
            .should_prompt_next("name (default is Pedro)")

def test_default_throws_exception_if_parameter_is_a_function():
    with pytest.raises(ValueError) as e_info:
        template("{% set my_name = 'David'%}{{ name | default(camelcase('david'))}}")\
                .with_values({})\
                .should_prompt_next("")
    assert "Filters at the moment only support" in str(e_info.value)

def test_description_prompts_description_intead_of_var_name():
    template("{{name | description ('Customer name')}}").with_values({})\
                                       .should_prompt_next("Customer name")
def test_descrioption_resolve_vars():
    template("{%set my_name = 'Victor'%}{{name | description(my_name)}}%}").with_values({})\
                                        .should_prompt_next("Victor")

def test_default_piped_with_description_then_desc_overrides_default():
    template("{{ name | default ('Mundo') | description ('World in english')}}").with_values({})\
                                       .should_prompt_next("World in english")

def test_pipe_descripion_default_filters():
    template("{{ name | description ('Customer name') | default ('John')}}").with_values({})\
                                       .should_prompt_next("Customer name (default is John)")

def test_duplicate_var_name_prompts_only_once_and_it_uses_first_one():
    template("{{ name | default ('John')}}, {{name}}").with_values({})\
                                       .should_prompt_next("name (default is John)")

def test_should_not_prompt_var_which_has_value_assigned():
    template("{% set process_descriptor_ref_id = process_descriptor_id %}").with_values({})\
                                       .should_prompt_next("process_descriptor_id")

def test_prompts_var_passed_to_global_function():
    template("{% set name = camelcase(a_var)%}").with_values({})\
                                       .should_prompt_next("a_var")

def test_include_should_prompt_vars_from_included_template_in_order():
    template("{% include 'hello_world' %}.  I am Juan {{last_name}}")\
            .and_template("hello_world","Hello {{name}}")\
            .with_values({})\
            .should_prompt_next("name")

def test_should_not_prompt_var_which_is_set_within_included_template():
    template("{% include 'set_name' %}. I am {{name}} {{last_name}}")\
            .and_template("set_name","{% set name = 'Juan' %}")\
            .with_values({})\
            .should_prompt_next("last_name")

def test_suggest_should_populate_prompt_suggestions():
    template("{{ name | suggest([1,2])}}")\
            .with_values({})\
            .should_prompt_next_suggesting("name",[1,2])

def test_suggest_should_resolve_vars():
    template("{% set suggestions = range(1,4)%}{{ name | suggest(suggestions)}}")\
            .with_values({})\
            .should_prompt_next_suggesting("name",[1,2,3])

def test_if_tag_does_not_prompt_if_condition_not_met():
    template_str="""
{% if enter_user_name %}
    {{ username }}
{% endif %}"""
    template(template_str)\
            .with_values({})\
            .should_prompt_next("enter_user_name")\
            .with_values({"enter_user_name":True})\
            .does_not_prompt()
