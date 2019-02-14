import os

from jinja2 import Environment, FileSystemLoader

from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.ui import MenuOption,select_option
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
class PrintSQLToConsoleCommand(object):
    """Command which generates a SQL script from a template and it prints the ouput to console"""
    def __init__(self, doc_creator=MultipleTemplatesDocGenerator()):
        self.doc_creator = doc_creator

    def run(self):
        self.doc_creator.run()

    def sql_printed(self):
        return self.doc_creator.generated_doc()

class PrintSQLToConsoleDisplayer(object):
    """Prints to console the command output"""
    def __init__(self):
        self.rendered_sql=""

    def write(self,content):
        self.render_sql(content)

    def render_sql(self,sql_to_render):
        print(sql_to_render)
        self._append_rendered_text(sql_to_render)

    def _append_rendered_text(self,text):
        if self.rendered_sql is not "" and\
            text is not "":
           self.rendered_sql+="\n"
        self.rendered_sql+=text

    def current_text(self):
        return self.rendered_text

class PrintSQLToConsoleProdConfig(object):
    def make(self, env_vars=os.environ):
        self.env_vars = env_vars
        return PrintSQLToConsoleCommandBuilder().\
                    with_action_seletor(self._make_action_selector()).\
                    with_doc_writer(self._make_doc_writer()).\
                    build()

    def _make_action_selector(self):
        return TemplateSelector(self._make_template_selector())

    def _make_template_selector(self):
        return SelectTemplateLoader(self._make_template_env())

    def _make_template_env(self):
        return EMTemplatesEnv().get_env(self.env_vars)

    def _make_doc_writer(self):
        return PrintSQLToConsoleDisplayer()

class PrintSQLToConsoleCommandBuilder(object):
    def __init__(self):
        self.sql_renderer=None
        self.action_selector =None
        self.doc_writer =None

    def with_action_seletor(self,action_selector):
        self.action_selector=action_selector
        return self

    def with_doc_writer(self,doc_writer):
        self.doc_writer =doc_writer
        return self

    def build(self):
        return PrintSQLToConsoleCommand(
                    MultipleTemplatesDocGenerator(
                        CreateDocumentFromTemplateCommand(
                            self.action_selector,
                            self.doc_writer
                        )
                    ),
                )
