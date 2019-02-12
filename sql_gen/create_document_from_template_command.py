class TemplateLoader(object):
    """"""

class SelectTemplateDisplayer(object):
    def ask_for_template(self,option_list):
        return input("Please enter an option ('x' to save && exit): ")

    """"""

class TemplateSelector(object):
    def __init__(self,loader,displayer):
        self.loader = loader
        self.displayer = displayer
    def select_template(self):
        """"""
        option_list = self.loader.list_options()
        template_input =self.displayer.ask_for_template(option_list)
        if template_input == 'x':
            return
        option = menu.ask_for_option(option_list)
        #template = loader.load_template(template_input)
        return option.get_template()
        #while not template:
        #    self.displayer.show_invalid_template_selected()
        #    template_input =self.displayer.ask_for_template(option_list)
        #    template = loader.load_template(template_input)

    def run(self):
        return None

class SelectTemplateLoader(object):
    def list_options(self):
        return []

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

