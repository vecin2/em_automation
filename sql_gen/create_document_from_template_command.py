from jinja2 import Environment, FileSystemLoader

from sql_gen.ui import prompt,MenuOption,select_option
from sql_gen.docugen.template_renderer import TemplateRenderer
from sql_gen.docugen.template_filler import TemplateFiller
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
                                       self.environment,
                                       TemplateFiller())
            template_option =MenuOption(counter +1,
                                        template_path,
                                        action)
            self.template_option_list.append(template_option)
        return self.template_option_list

class MultipleTemplatesDocGenerator(object):
    def __init__(self,single_doc_generator):
        self.single_doc_generator = single_doc_generator

    def run(self):
        filled_template = self.single_doc_generator.run()
        while filled_template is not "":
            filled_template = self.single_doc_generator.run()
        return
    def generated_doc(self):
        return self.single_doc_generator.generated_doc()


class CreateDocumentFromTemplateCommand(object):
    def __init__(self,selector,writer):
        self.selector = selector
        self.writer =writer

    def run(self):
        filled_template = self.selector.select_action().run()
        self.writer.write(filled_template)
        return filled_template

    def generated_doc(self):
        return self.writer.current_text()

