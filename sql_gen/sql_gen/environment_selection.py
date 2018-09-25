from jinja2 import Environment, FileSystemLoader, select_autoescape
from sql_gen.sql_gen.filter_loader import load_filters
from sql_gen.ui.cli_ui_util import input_with_validation
from sql_gen.globals import camelcase, dbquery
import os,sys

class TemplateOption(object):
    MENU_FOLDER="menu/"
    WINDOWS_LINK=".lnk"
    def __init__(self,id, template_path):
        #when creating windos links it adds '.lnk'. 
        #we want to remove so template can still be loaded by name
        self.id =id
        self.name =template_path.replace(self.MENU_FOLDER,'').replace(self.WINDOWS_LINK,'')

def list_menu_templates(template_name):
    if TemplateOption.MENU_FOLDER in template_name:
        return True
    return False
class TemplateSelector():
    
    def select_template(self, env):
        template_list = env.list_templates(None,list_menu_templates)
        self.create_options(template_list)
        self.show_options()

        return self.prompt_to_select_template(env)    
    
    def create_options(self, template_list):
        self.template_option_list=[]
        for counter, template_path in enumerate(template_list):
            template_option =TemplateOption(counter, template_path)
            self.template_option_list.append(template_option)
        return self.template_option_list

    def show_options(self):
        for template_option in self.template_option_list:
            print(str(template_option.id) + ". " +template_option.name)

    def prompt_to_select_template(self,env):
        template_number = input_with_validation("\nPlease select template to parse: ")
        template = self.get_template(template_number, env)
        while template is None:
            template_number = input_with_validation("\nPlease select template to parse: ")
            sys.stdout.write('\n')
            self.show_options()
            template = self.get_template(template_number, env)
        return template


    def get_template(self, template_number,env):
        option = self.get_option_by_id(template_number)
        if option is None:
            return option
        template_name = option.name
        try:
            env.loader.get_source(env,template_name)
        except Exception:
            print ("This template does not exist. Make sure there is a matching template under the configured templates folder")
            return None

        return template_name

    def get_option_by_id(self, template_number):
        for template_option in self.template_option_list:
            if template_number == str(template_option.id):
                return template_option
        return None


class EMTemplatesEnv():
    def __init__(self):
        templates_path =os.environ['SQL_TEMPLATES_PATH']
        print("\nLoading templates from '" + templates_path+"':")
        self.env = Environment(
                            loader=FileSystemLoader(templates_path),
                            trim_blocks=True,
                            lstrip_blocks=True,
                            keep_trailing_newline=False #default
                            )
        self.env.globals['camelcase'] = camelcase
        self.env.globals['dbquery'] = dbquery
        load_filters(self.env)
    
    def get_env(self):
        return self.env
