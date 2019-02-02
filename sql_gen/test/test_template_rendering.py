from jinja2 import Template,Environment,FileSystemLoader

def test_default_filter():
    t = Template("{{name | default('Julio')}}")
    assert "Julio"== t.render()
    assert "Julio"== t.render()
