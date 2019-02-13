from jinja2 import Environment, FileSystemLoader

from sql_gen.ui import prompt,MenuOption,select_option
from sql_gen.docugen.template_renderer import TemplateRenderer

class TemplateSelector(object):
    def __init__(self,loader,displayer):
        self.displayer = displayer
        self.loader = loader

    def select_template(self):
        actions = self.loader.list_actions()
        action = self.displayer.ask_for_template(actions)
        if action.code is 'x':
            return None
        return self.loader.load_template(action.name)

class ExitAction():
    def run():
        """Does nothing and exits"""

class SelectTemplateLoader(object):
    def __init__(self, environment):
        self.environment=environment

    def load_template(self,name):
        return self.environment.get_template(name)

    def list_actions(self):
        saveAndExit=MenuOption('x','Save && Exit',ExitAction())
        result = self._template_options()
        result.append(saveAndExit)
        return result

    def _template_options(self):
        template_names =self.environment.list_templates()
        return self._to_options(template_names)

    def _to_options(self, template_list):
        self.template_option_list=[]
        for counter, template_path in enumerate(template_list):
            template_option =MenuOption(counter, template_path)
            self.template_option_list.append(template_option)
        return self.template_option_list


class SelectTemplateDisplayer(object):
    def ask_for_template(self,option_list):
        text="Please enter an option ('x' to save && exit): "
        return select_option(text, option_list)

class TemplateFiller(object):
    def fill(self,template):
        return template.render({})
        #return TemplateRenderer(None,None).fill_template(template,
        #            {})


class CreateDocumentFromTemplateCommand(object):
    def __init__(self,selector,template_filler):
        self.selector = selector
        self.template_filler= template_filler

    def run(self):
        template =self.selector.select_template()
        if template:
            return self.template_filler.fill(template)
        return ""

