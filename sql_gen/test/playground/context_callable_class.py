from jinja2 import Template

text ='''
{% set martin_name = "Juan"%}
martin is {{name | default(martin_name)}}
Callable class is: {{callableclass("martin_name")}}
'''

from jinja2.utils import contextfunction
class CallableClass(object):
    @contextfunction
    def __call__(self, ctx,var_name):
        return ctx.resolve(var_name)

def test_my_test():
    tpl = Template(text)
    output = tpl.render(callableclass=CallableClass(),martin_name ="Fran")
    assert "fra" ==output

