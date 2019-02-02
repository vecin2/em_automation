from jinja2 import Environment, FileSystemLoader, select_autoescape
from sql_gen.ui.cli_ui_util import suggest_prompt
import os,sys
import inspect
import pkgutil
import importlib
from sql_gen import logger

class TemplateOption(object):
    MENU_FOLDER="menu/"
    WINDOWS_LINK=".lnk"
    def __init__(self,id, template_path):
        #when creating windos links it adds '.lnk'. 
        #we want to remove so template can still be loaded by name
        self.id =id
        self.name =template_path.replace(self.MENU_FOLDER,'').replace(self.WINDOWS_LINK,'')
    def __repr__(self):
        return str(self.id) +". "+self.name

def list_menu_templates(template_name):
    if TemplateOption.MENU_FOLDER in template_name:
        return True
    return False
class MenuDisplayer(object):
    def display(self, items):
        for template_option in items:
            print(str(template_option.id) + ". " +template_option.name)
        no_of_options=str(len(items)-1)
        print("\n[0 to "+no_of_options+"]. Create SQLTask\t\tx. Exit")

class TemplateSelector():
    def __init__(self,env=None,displayer=MenuDisplayer()):
        self.env = env
        self.displayer = displayer

    def select_template(self):
        self.show_options()
        return self.prompt_to_select_template()

    def get_env(self):
        return self.env

    def create_options(self, template_list):
        self.template_option_list=[]
        for counter, template_path in enumerate(template_list):
            template_option =TemplateOption(counter, template_path)
            self.template_option_list.append(template_option)
        logger.debug("Option list created with "+str(len(self.template_option_list))+" options")
        return self.template_option_list

    def show_options(self):
        template_list = self.get_env().list_templates(None,list_menu_templates)
        logger.debug("List templated returned "+ str(len(template_list))+" templates")
        self.create_options(template_list)
        self.displayer.display(self.template_option_list)

    def _get_option(self):
        input_text =suggest_prompt(
                            "\nEnter option: ",
                            self.template_option_list)
        if input_text:
            return input_text.split(".")[0]
        return input_text

    def prompt_to_select_template(self):
        #option_key = input_with_validation("\nEnter option: ")
        option_key = self._get_option()
        if option_key =="x":
            return
        template_name = self.get_template_name(option_key)
        while template_name is None:
            option_key = self._get_option()
            if option_key =="x":
                return
            sys.stdout.write('\n')
            self.show_options()
            template_name = self.get_template_name(option_key)
        return self.get_env().get_template(template_name)


    def get_template_name(self, template_number):
        logger.debug("Getting template for option number"+ template_number)
        option = self.get_option_by_id(template_number)
        if option is None:
            return option
        template_name = option.name
        try:
            env=self.get_env()
            env.loader.get_source(env,template_name)
        except Exception as excinfo:
            logger.error(str(excinfo))
            print ("This template does not exist. Make sure there is a matching template under the configured templates folder")
            return None

        logger.debug("Template returned"+ template_name)
        return template_name

    def get_option_by_id(self, template_number):
        for template_option in self.template_option_list:
            if template_number == str(template_option.id):
                return template_option
        return None

