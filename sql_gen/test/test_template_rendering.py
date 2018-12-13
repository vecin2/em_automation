from jinja2 import Template,Environment,FileSystemLoader
from sql_gen.docugen.environment_selection import EMTemplatesEnv

def test_default_filter():
    env = Environment(
                            loader=FileSystemLoader("/home/dgarcia/dev/python/em_automation/sql_gen/templates"
),
                            trim_blocks=True,
                            lstrip_blocks=True,
                            keep_trailing_newline=False #default
                            )
    env =EMTemplatesEnv()
    #t =env.get_template("test_default.sql")
    t = Template("{{name | default('Julio')}}")
    assert "Julio"== t.render()
    assert "Julio"== t.render()
