from jinja2 import Environment, FileSystemLoader, select_autoescape
from sql_gen.template_source import TemplateSource
from sql_gen.filter_loader import load_filters
import os

class TemplateOption(object):
    def __init__(self,id, name):
        self.id =id
        self.name =name

class TemplateSelector():
    def select_template(self, env):
        template_list = env.list_templates(".sql")
        self.create_options(template_list)
        self.show_options()

        template_number = self.prompt_to_select_template()    
        template_name = self.get_option_by_id(template_number).name
        return self.build_template_source(template_name,env)
    
    def create_options(self, template_list):
        self.template_option_list=[]
        for counter, template in enumerate(template_list):
            template_option =TemplateOption(counter, template)
            self.template_option_list.append(template_option)
        return self.template_option_list

    def show_options(self):
        for template_option in self.template_option_list:
            print(str(template_option.id) + ". " +template_option.name)

    def prompt_to_select_template(self):
        template_number = input("Please select template to parse: ")
        while self.get_option_by_id(template_number) is None:
            template_number = input("Please select template to parse: ")
            self.show_options()
        return template_number

    def get_option_by_id(self, template_number):
        for template_option in self.template_option_list:
            if template_number == str(template_option.id):
                return template_option
        return None

    def build_template_source(self, template_name, env):
        source = env.loader.get_source(env,template_name)[0]
        template_source = TemplateSource(env.parse(source))
        template_source.template_name = template_name
        return template_source

class EMTemplatesEnv():
    def __init__(self):
        templates_path =os.environ['SQL_TEMPLATES_PATH']
        print("the path:" + templates_path)
        self.env = Environment(
        loader=FileSystemLoader(templates_path),
                         autoescape=select_autoescape(['html', 'xml']))
        load_filters(self.env)
    
    def get_env(self):
        return self.env
