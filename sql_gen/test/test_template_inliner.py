import pytest
import re
from io import StringIO
from jinja2 import Environment

from sql_gen.docugen.env_builder import EnvBuilder
from sql_gen.docugen.template_inliner import TemplateInliner,IncludedTemplateParser,IncludeClause,PlainText

######Test TemplateInliner####
def make_template(source,filename,fs):
    env = EnvBuilder().set_fs_path("/templates").build()
    fs.create_file("/templates/"+filename,contents=source)
    return env.get_template(filename)

def test_not_included_templates_returns_same_source(fs):
    inliner = TemplateInliner(make_template("Hello Mark","hello_mark.txt",fs))

    assert 'Hello Mark' == inliner.inline()

def test_one_included_template(fs):
    mark_template =make_template("Hello {% include 'name.txt' %}","greeting_person.txt",fs)
    make_template("John","name.txt",fs)
    inliner = TemplateInliner(mark_template)

    assert 'Hello John' == inliner.inline()

def test_multiple_included_template(fs):
    text="{% include 'greeting.txt' %}, {% include 'name.txt' %}"
    mark_template =make_template(text,"greeting_person.txt",fs)
    make_template("Hi","greeting.txt",fs)
    make_template("Mark","name.txt",fs)
    inliner = TemplateInliner(mark_template)

    assert 'Hi, Mark' == inliner.inline()

def test_include_with_double_quotes(fs):
    template =make_template('Hi {% include "name.txt" %}',"greeting_person.txt",fs)
    make_template("David","name.txt",fs)
    inliner = TemplateInliner(template)

    assert 'Hi David' == inliner.inline()

def test_recursive_includes(fs):
    template =make_template('Hi {% include "full_name.txt" %}',"greeting_person.txt",fs)
    make_template("{% include 'first_name.txt' %} {% include 'second_name.txt' %}","full_name.txt",fs)
    make_template("{% include 'title.txt' %} David","first_name.txt",fs)
    make_template("Mr","title.txt",fs)
    make_template("Smith","second_name.txt",fs)
    inliner = TemplateInliner(template)
    assert 'Hi Mr David Smith' == inliner.inline()

######Explore regex####
def test_how_regex_works():
    """"""
    text ="The needle shop sells needles"
    regex = re.compile("needle")
    match =re.search(regex,text)
    assert "needle" == match.group()
    assert 4 == match.start()
    assert 10 == match.end()
    assert (4,10) == match.span()
    matches =list(re.finditer(regex,text))
    assert 2 == len(matches)
    assert (4,10) == matches[0].span()
    assert (22,28) == matches[1].span()

def test_how_match_group_works():
    text="{% include 'name.txt' %}"
    regex = re.compile("{%\s*include (\'|\")(.*?)(\'|\")\s*%}")
    match =re.search(regex,text)
    assert "{% include 'name.txt' %}" == match.group()
    assert "name.txt" == match.groups()[1]


######Test Includes parser####
def parse_segments(text, *expected_segments):
    assert list(expected_segments) == IncludedTemplateParser().parse_segments(text)

def test_empty_template_return_empty_list():
    parse_segments("")

def test_plain_text_returns_same_plain_text():
    parse_segments("Hello", PlainText("Hello"))


def test_parse_multiple_includes():
    text ="""Hello {% include 'name.txt' %}, {% include 'surname.txt' %}
I am {% include 'owner.txt' %}"""
    parse_segments(text,
                  PlainText("Hello "),
                  IncludeClause("name.txt"),
                  PlainText(", "),
                  IncludeClause("surname.txt"),
                  PlainText("\nI am "),
                  IncludeClause("owner.txt")
                  )

def test_parse_double_quotes():
    text ='hi {% include "surname.txt" %} bye'
    parse_segments(text,
                  PlainText("hi "),
                  IncludeClause('surname.txt'),
                  PlainText(" bye"),
                  )

def test_parse_different_spacing():
    text ='{%   include "surname.txt"    %}{%include "names.txt"%}'
    parse_segments(text,
                   IncludeClause('surname.txt'),
                   IncludeClause('names.txt')
                  )
