from jinja2 import Environment, FileSystemLoader

from sql_gen.ui import prompt,MenuOption,select_option
from sql_gen.docugen.template_renderer import TemplateRenderer
from sql_gen.actions import ExitAction, FillTemplateAction 

class TemplateSelector(object):
    def __init__(self,loader):
        self.loader = loader

    def select_action(self):
        options = self.loader.list_options()
        text="Please enter an option ('x' to save && exit): "
        return select_option(text, options)

class SelectTemplateLoader(object):
    def __init__(self, environment):
        self.environment=environment

    def list_options(self):
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
            action =FillTemplateAction(template_path,
                                       self.environment)
            template_option =MenuOption(counter +1,
                                        template_path,
                                        action)
            self.template_option_list.append(template_option)
        return self.template_option_list


class CreateDocumentFromTemplateCommand(object):
    def __init__(self,selector):
        self.selector = selector

    def run(self):
        return self.selector.select_action().run()

