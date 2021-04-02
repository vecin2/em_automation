from jinja2 import (
    Environment,
    meta,
    Template,
    nodes,
    FileSystemLoader,
    select_autoescape,
)
from jinja2.nodes import Stmt, Template, Output, Node
from jinja2.visitor import NodeTransformer, NodeVisitor
from anytree import Node as AnyTreeNode
import pytest
import sql_gen.sqltask_jinja.filters as filters_package
from sql_gen.docugen.env_builder import EnvBuilder


env = EnvBuilder().set_fs_path("templates").set_filters_package(filters_package).build()

hello_welcome_output = (
    "Output(nodes=[TemplateData(data='Hello '), "
    + "Name(name='name', ctx='load'), "
    + "TemplateData(data=', welcome to '), "
    + "Name(name='company_name', ctx='load'), "
    + "TemplateData(data='!')"
    + "])"
)


def children(node):
    result = []
    for child in node.iter_child_nodes():
        result.append(child)
    return result


def child(node, index):
    return children(node)[index]


def number_of_children(node):
    return len(children(node))


def test_template_with_no_variables():
    template = env.parse("Hola Juan")
    #   template
    #    /
    #  output
    #   /
    #  template_data("Hola Juan")
    assert isinstance(template, Node)
    assert isinstance(template, Template)
    assert 1 == len(children(template))

    output = children(template)[0]
    assert isinstance(output, Output)
    assert 1 == len(children(output))

    template_data = children(output)[0]
    assert 0 == len(children(template_data))
    assert "Hola Juan" == template_data.data


def test_template_with_one_variable():
    template = env.parse("Hola {{ customer_name }}")
    #               template
    #                   |
    #    ___________ output____________________
    #   /                                      \
    #  template_data("Hola Juan")        Name("custome_name")

    assert isinstance(template, Node)
    assert isinstance(template, Template)

    output = child(template, 0)
    assert 2 == number_of_children(output)
    template_data = child(output, 0)
    assert 0 == number_of_children(template_data)

    assert "Hola " == template_data.data
    name_object = child(output, 1)
    assert 0 == number_of_children(name_object)
    assert "customer_name" == name_object.name


def test_one_variable_with_default_filter():
    template = env.parse("Hola {{ customer_name | default ('Joe Smith') }}")
    #               template
    #                   |
    #          _____ output__________________________
    #         /                                      \
    #  template_data("Hola")         ________Filter("default")___
    #                               /                            \
    #                       Const("Jose Smith")               Name("customer_name")

    output = child(template, 0)
    assert 2 == number_of_children(output)

    template_data = child(output, 0)
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


def test_default_filter_with_variable_as_parameter():
    template = env.parse("Hola {{ customer_name | default ('Joe Smith') }}")
    #               template
    #                   |
    #          _____ output__________________________
    #         /                                      \
    #  template_data("Hola")         ________Filter("default")___
    #                               /                            \
    #                       Const("Jose Smith")               Name("customer_name")

    output = child(template, 0)
    assert 2 == number_of_children(output)

    template_data = child(output, 0)
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
    template = env.parse("Hola {{ customer_name | description ('its the full name') }}")
    #               template
    #                   |
    #          _____ output__________________________
    #         /                                      \
    #  template_data("Hola")         ________Filter("default")___
    #                               /                            \
    #                       Name("customer_name")               Const("its the full name")

    output = child(template, 0)
    assert 2 == number_of_children(output)

    template_data = child(output, 0)
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
    template = env.parse(
        "Hola {{ customer_name | default('Joe Smith') | description ('its the full name') }}"
    )
    #               template
    #                   |
    #          _____ output_______________
    #         /                           \
    #  template_data("Hola")   __Filter("description")__
    #                         /                          \
    #                    ___Filter("default")_    Const("its the full name")
    #                   /                     \
    #                Name("customer_name")    Const("Jose Smith")

    output = child(template, 0)
    assert 2 == number_of_children(output)

    template_data = child(output, 0)
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


def test_variable_assignment():
    template_text = """{% set name_with_title = 'Mr '+ name%}
Hello {{ name_with_title}}!"""
    template = env.parse(template_text)
    #               template
    #                   |
    #          _____Assign_______________
    #         /                           \
    #  template_data("Hola")   __Filter("description")__
    #                         /                          \
    #                    ___Filter("default")_    Const("its the full name")
    #                   /                     \
    #                Name("customer_name")    Const("Jose Smith")

    assert 2 == number_of_children(template)

    assign = child(template, 0)
    assert 2 == number_of_children(assign)

    target = child(assign, 0)
    assert "name_with_title" == target.name
    assert "store" == target.ctx
    assert 0 == number_of_children(target)

    add = child(assign, 1)
    assert 2 == number_of_children(add)

    left = child(add, 0)
    assert "Mr " == left.value
    right = child(add, 1)
    assert "name" == right.name
    assert "load" == right.ctx

    output = child(template, 1)
    assert "Hello " == child(output, 0).data
    assert "name_with_title" == child(output, 1).name
    assert "!" == child(output, 2).data


template_text = "{% include 'hello_world.sql' %} Hola {{ jesus | default ('fran') }}!"
template_text = "Hello {{ prename }} {{ name | description ('World in english') | default ('Mundo')}}!"
template = env.parse(template_text)
#               template
#                   |
#          _____Assign_______________
#         /                           \
#  template_data("Hola")   __Filter("description")__
#                         /                          \
#                    ___Filter("default")_    Const("its the full name")
#                   /                     \
#                Name("customer_name")    Const("Jose Smith")


def draw_node(tree):
    return str(tree)


def recursive_draw_string(tree, spacer):
    if number_of_children(tree) == 0:
        return spacer + draw_node(tree) + "\n"

    result = spacer + draw_node(tree) + "\n"
    spacer = "    " + spacer
    children_string = ""
    for node in tree.iter_child_nodes():
        children_string += recursive_draw_string(node, spacer)
    return result + children_string


def draw_string(tree):
    spacer = "+--"
    return recursive_draw_string(tree, spacer)


def draw(tree):
    print(draw_string(template))


print("***")
draw(template)


class TreeDrawer(object):
    def __init__(self):
        self.draw = ""

    def get_drawer(self, node):
        """Return the visitor function for this node or `None` if no visitor
        exists for this node.  In that case the generic visit function is
        used instead.
        """
        method = "draw_" + node.__class__.__name__
        return getattr(self, method, None)

    def draw_Include(self, node):
        return "Include(" + node.template.value + ")"

    def draw_Filter(self, node):
        return "Filter(" + node.name + ")"

    def draw_node(self, node):
        draw_func = self.get_drawer(node)
        if draw_func is not None:
            return draw_func(node)
        return self.generic_draw(node)

    def generic_draw(self, node):
        return str(node)

    def visit(self, node):
        self.generic_visit(node, "+--")

    def print_node(self, node):
        self.visit(node)
        print(self.draw)

    def generic_visit(self, node, spacer):
        self.draw += spacer + self.draw_node(node) + "\n"
        spacer = "    " + spacer
        for node in node.iter_child_nodes():
            self.generic_visit(node, spacer)


draw_visitor = TreeDrawer()
draw_visitor.print_node(template)
print(draw_visitor.draw)


class RewriteAsAnyTree(NodeTransformer):
    def visit_Include(self, node):
        node.parent = node
        return node


def convert_to_any_tree(jinja_node):
    r = RewriteAsAnyTree()
    return r.visit(jinja_node)


# print("before is "+str(template.body[0].parent))
print("then after")
print("Include is " + str(template.body[0]))
any_tree_template = convert_to_any_tree(template)
print(str(any_tree_template))
# print(str(template.body[0].parent))
