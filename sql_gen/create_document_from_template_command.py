from sql_gen.ui import prompt,MenuOption,select_option

class TemplateSelector(object):
    def __init__(self,loader,displayer):
        self.displayer = displayer
        self.menu = loader.list_options()

    def select_template(self):
        self.displayer.ask_for_template(self.menu)
        return

class SelectTemplateLoader(object):
    def list_options(self):
        return [MenuOption('1','say_hello.sql'),
                MenuOption('x','Save && Exit')]

class SelectTemplateDisplayer(object):
    def ask_for_template(self,option_list):
        text="Please enter an option ('x' to save && exit): "
        return select_option(text, option_list)

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

