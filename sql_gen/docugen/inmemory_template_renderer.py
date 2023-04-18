from jinja2 import DictLoader

from sql_gen.docugen.env_builder import EnvBuilder
from sql_gen.docugen.template_filler import TemplateFiller
from sql_gen.sqltask_jinja import filters as filters_package
from sql_gen.sqltask_jinja import globals as globals_module


class InMemoryTemplateRenderer(object):
    def render(self, template_content, context):
        template = self._make_template_from_content(template_content)
        template_filler = TemplateFiller(initial_context=context)
        return template_filler.fill_and_render(template)

    def _make_template_from_content(self, template_content):
        templates = {"template": template_content}
        env = (
            EnvBuilder()
            .set_loader(DictLoader(templates))
            .set_globals_module(globals_module)
            .set_filters_package(filters_package)
            .build()
        )
        return env.get_template("template")
