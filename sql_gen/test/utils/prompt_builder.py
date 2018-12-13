from jinja2 import Template,Environment,DictLoader
from sql_gen.docugen.environment_selection import populate_filters_and_globals
from sql_gen.docugen.prompt_parser import PromptParser

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
        env = Environment(
            loader=DictLoader(self.templates))
        populate_filters_and_globals(env)
        return env

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
        assert None == self._parser().next_prompt(self.template_values)

    def assert_display_msg(self,msg, prompt):
        assert msg +": " == prompt.get_display_text()

