import sys

from prompt_toolkit import prompt as tk_prompt


class TemplateLoader(object):
    """"""

def prompt(text):
    if not sys.stdout.isatty():
        return input(text)
    else:
        return tk_prompt(text)

class SelectTemplateDisplayer(object):
    def ask_for_template(self,option_list):
        return prompt("Please enter an option ('x' to save && exit): ")

    """"""

class TemplateSelector(object):
    def __init__(self,loader,displayer):
        self.displayer = displayer
        self.menu = loader.list_options()

    def select_template(self):
        self._select_option().code
        return

    def _select_option(self):
        option =None
        while option is None:
            template_input =self.displayer.ask_for_template(self.menu)
            option = self._parse_input(template_input)
        return option

    def _parse_input(self,input_entered):
        for option in self.menu:
            if option.code == input_entered:
                return option
        return None


class SelectTemplateLoader(object):
    def list_options(self):
        return [MenuOption('x','Save && Exit')]

class MenuOption(object):
    def __init__(self,code, name):
        self.code =code
        self.name =name
    def __repr__(self):
        return str(self.code) +". "+self.name

class TemplateFiller(object):
    def fill(self):
        """"""


class CreateDocumentFromTemplateCommand(object):
    def __init__(self,selector,template_filler):
        self.selector = selector
        self.template_filler= template_filler

    def run(self):
        template =self.selector.select_template()
        if template:
            return self.template_filler.fill(template)
        return ""

