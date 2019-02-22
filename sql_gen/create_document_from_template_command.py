import os

from jinja2 import Environment, FileSystemLoader

from sql_gen.app_project import AppProject
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.sqltask_jinja.context import init
from sql_gen.ui import prompt,MenuOption,select_option
from sql_gen.docugen.template_renderer import TemplateRenderer
from sql_gen.docugen.template_filler import TemplateFiller

class TemplateSelector(object):
    def __init__(self,env_vars):
        templates_path=EMTemplatesEnv().extract_templates_path(env_vars)
        self.loader= SelectTemplateLoader(templates_path)

    def select_template(self):
        options = self.loader.list_options()
        text="Please enter an option ('x' to save && exit): "
        option =  select_option(text, options)
        if option.code == 'x':
            return None
        return self.loader.load_template(option.name)

class SelectTemplateLoader(object):
    def __init__(self, templates_path):
        self.environment= EMTemplatesEnv().make_env(templates_path)

    def load_template(self,name):
        return self.environment.get_template(name)

    def list_options(self):
        saveAndExit=MenuOption('x','Save && Exit')
        result = self._template_options()
        result.append(saveAndExit)
        return result

    def _template_options(self):
        template_names =self.environment.list_templates(None,self.list_templates_filter)
        return self._to_options(template_names)

    def list_templates_filter(self,template_name):
        if "hidden_templates" not in template_name:
            return True

    def _to_options(self, template_list):
        self.template_option_list=[]
        for counter, template_path in enumerate(template_list):
            template_option =MenuOption(counter +1,
                                        template_path)
            self.template_option_list.append(template_option)
        return self.template_option_list

class CreateDocumentFromTemplateCommand(object):
    def __init__(self,
                 env_vars=os.environ,
                 writer=None,
                 initial_context={}):
        self.selector = TemplateSelector(env_vars)
        self.writer =writer
        self.initial_context=initial_context 

    def run(self):
        template = self.selector.select_template()
        filled_template=""
        while template:
            filled_template =TemplateFiller().fill(template,dict(self.initial_context))
            self.writer.write(filled_template)
            template = self.selector.select_template()

