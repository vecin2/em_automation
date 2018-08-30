from jinja2 import Environment, meta, Template, nodes
from jinja2.nodes import Stmt,Template,Output,Node
import pytest
from sql_gen.sql_gen.filter_loader import load_filters

env = Environment()
load_filters(env)
hello_welcome_output ="Output(nodes=[TemplateData(data='Hello '), "+\
                          "Name(name='name', ctx='load'), "+\
                          "TemplateData(data=', welcome to '), "+\
                          "Name(name='company_name', ctx='load'), "+\
                          "TemplateData(data='!')"+\
                         "])"

def children(node):
    result=[]
    for child in node.iter_child_nodes():
        result.append(child)
    return result

def child(node, index):
    return children(node)[index]

def number_of_children(node):
    return len(children(node))

def test_template_with_no_variables():
    #   template
    #    /
    #  output
    #   /
    #  template_data("Hola Juan")
    template = env.parse("Hola Juan")
    assert isinstance(template,Node)
    assert isinstance(template,Template)
    assert 1  ==  len(children(template))

    output = children(template)[0]
    assert isinstance(output, Output)
    assert 1 == len(children(output))

    template_data = children(output)[0]
    assert 0 == len(children(template_data))
    assert "Hola Juan" == template_data.data

def test_template_with_one_variable():
    #               template
    #                   |
    #    ___________ output____________________
    #   /                                      \
    #  template_data("Hola Juan")        Name("custome_name") 

    template = env.parse("Hola {{ customer_name }}")
    assert isinstance(template,Node)
    assert isinstance(template,Template)

    output = child(template,0)
    assert 2 == number_of_children(output)
    template_data = child(output,0)
    assert 0 == number_of_children(template_data)

    assert "Hola " == template_data.data
    name_object = child(output, 1) 
    assert 0 == number_of_children(name_object)
    assert "customer_name" == name_object.name

def test_one_variable_with_default_filter():
    #               template
    #                   |
    #          _____ output__________________________
    #         /                                      \
    #  template_data("Hola")         ________Filter("default")___
    #                               /                            \ 
    #                       Const("Jose Smith")               Name("customer_name") 

    template = env.parse("Hola {{ customer_name | default ('Joe Smith') }}")

    output = child(template,0)
    assert 2 == number_of_children(output)

    template_data = child(output,0)
    assert "Hola " == template_data.data
    assert 0 == number_of_children(template_data)

    default_filter = child(output, 1) 
    assert "default" == default_filter.name
    assert 2 == number_of_children(default_filter)
    
    name_object = child(default_filter, 0) 
    assert "customer_name" == name_object.name
    assert 0 == number_of_children(name_object)

    constant = child(default_filter, 1) 
    assert "Joe Smith" == constant.value
    assert 0 == number_of_children(constant)

def test_one_variable_with_description_filter():
    #               template
    #                   |
    #          _____ output__________________________
    #         /                                      \
    #  template_data("Hola")         ________Filter("default")___
    #                               /                            \ 
    #                       Name("customer_name")               Const("its the full name") 

    template = env.parse("Hola {{ customer_name | description ('its the full name') }}")

    output = child(template,0)
    assert 2 == number_of_children(output)

    template_data = child(output,0)
    assert "Hola " == template_data.data
    assert 0 == number_of_children(template_data)

    description_filter = child(output, 1) 
    assert "description" == description_filter.name
    assert 2 == number_of_children(description_filter)
    
    name_object = child(description_filter, 0) 
    assert "customer_name" == name_object.name
    assert 0 == number_of_children(name_object)

    constant = child(description_filter, 1) 
    assert "its the full name" == constant.value
    assert 0 == number_of_children(constant)

def test_one_variable_with_default_pipe_with_description_filter():
    #               template
    #                   |
    #          _____ output_______________
    #         /                           \
    #  template_data("Hola")   __Filter("description")__
    #                         /                          \ 
    #                    ___Filter("default")_    Const("its the full name")
    #                   /                     \
    #                Name("customer_name")    Const("Jose Smith")      
    template = env.parse("Hola {{ customer_name | default('Joe Smith') | description ('its the full name') }}")

    output = child(template,0)
    assert 2 == number_of_children(output)

    template_data = child(output,0)
    assert "Hola " == template_data.data
    assert 0 == number_of_children(template_data)

    description_filter = child(output, 1) 
    assert "description" == description_filter.name
    assert 2 == number_of_children(description_filter)
    
    default_filter = child(description_filter, 0) 
    assert "default" == default_filter.name
    assert 2 == number_of_children(default_filter)

    constant = child(description_filter, 1) 
    assert "its the full name" == constant.value
    assert 0 == number_of_children(constant)

    name_object = child(default_filter, 0) 
    assert "customer_name" == name_object.name
    assert 0 == number_of_children(name_object)

    constant = child(default_filter, 1) 
    assert "Joe Smith" == constant.value
    assert 0 == number_of_children(constant)



@pytest.mark.skip
def test_find_by_node_type_one_stmt_output():
    template = env.parse("Hello {{ name }}, welcome to {{company_name}}!")
    output_node =template.find(Stmt)
    assert hello_welcome_output == str(output_node)
    template = template.find(Template)
    assert None == template


@pytest.mark.skip
def test_iterate_nodes_one_output_node(): 
    template = env.parse("Hello {{ name }}, welcome to {{company_name}}!")
    result =""
    for node in template.iter_child_nodes():
        for sub_node in node.iter_child_nodes():
            result += str(sub_node)



    assert hello_welcome_output == result

@pytest.mark.skip
def test_iterate_nodes():
    template = """Hello {{ name }}, welcome to {{company_name}}!
my name is"""
    template = env.parse(template)
    result=""
    for node in template.iter_child_nodes():
        result += str(node)

    assert hello_welcome_output == result
