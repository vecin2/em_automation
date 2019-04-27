from jinja2 import Template,Environment,DictLoader
from sql_gen.docugen.prompt_parser import PromptParser
from sql_gen.docugen.env_builder import EnvBuilder
from sql_gen.sqltask_jinja import globals as globals_module
from sql_gen.sqltask_jinja import filters as filters_package

class _TestPromptBuilder(object):
    def __init__(self, source):
        self.source = source
        self.templates = {"one_template":source}
        self.parser = None
        self.last_prompt =None

    def _parser(self):
        if not self.parser:
            template = self._template()
            self.parser= PromptParser(template)
        return self.parser

    def _template(self):
        return self._env().get_template("one_template")

    def _env(self):
        return EnvBuilder().set_loader(DictLoader(self.templates))\
                           .set_globals_module(globals_module)\
                           .set_filters_package(filters_package)\
                           .build()

    def and_template(self, template_name, source):
        self.templates[template_name]=source
        return self

    def with_values(self,template_values):
        self.template_values =template_values
        return self

    def should_prompt_next(self,msg):
        self.last_prompt = self._parser().next_prompt(self.template_values)
        self.assert_display_msg(msg, self.last_prompt)
        return self

    def should_prompt_next_suggesting(self,msg,suggestions):
        self.should_prompt_next(msg)
        assert suggestions == self.last_prompt.completer.suggestions
        return self

    def does_not_prompt(self):
        next_prompt =self._parser().next_prompt(self.template_values)
        if not next_prompt:
            assert True
            return
        assert None == next_prompt.get_display_text()

    def assert_display_msg(self,msg, prompt):
        assert msg +": " == prompt.get_display_text()


