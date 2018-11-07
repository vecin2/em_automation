from jinja2 import Environment, FileSystemLoader, select_autoescape
from sql_gen.ui.cli_ui_util import input_with_validation
import sql_gen.globals as template_globals
import sql_gen.filters as template_filters
import os,sys
import inspect
import pkgutil
import importlib
from sql_gen.logger import logger

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

    def select_template(self):
        logger.debug("Entering select_template")
        env = EMTemplatesEnv().get_env()
        template_list = env.list_templates(None,list_menu_templates)
        logger.debug("List templated returned "+ str(len(template_list))+" templates")
        self.create_options(template_list)
        logger.debug("Option list created with "+str(len(self.template_option_list))+" options")
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
        no_of_options=str(len(self.template_option_list)-1)
        print("\n[0 to "+no_of_options+"]. Create SQLTask\t\tx. Exit")

    def prompt_to_select_template(self,env):
        option_key = input_with_validation("\nEnter option: ")
        if option_key =="x":
            return
        template_name = self.get_template_name(option_key, env)
        while template_name is None:
            option_key = input_with_validation("\nEnter option: ")
            if option_key =="x":
                return
            sys.stdout.write('\n')
            self.show_options()
            template_name = self.get_template_name(option_key, env)
        return env.get_template(template_name)


    def get_template_name(self, template_number,env):
        logger.debug("Getting template for option number"+ template_number)
        option = self.get_option_by_id(template_number)
        if option is None:
            return option
        template_name = option.name
        try:
            env.loader.get_source(env,template_name)
        except Exception:
            print ("This template does not exist. Make sure there is a matching template under the configured templates folder")
            return None

        logger.debug("Template returned"+ template_name)
        return template_name

    def get_option_by_id(self, template_number):
        for template_option in self.template_option_list:
            if template_number == str(template_option.id):
                return template_option
        return None

def populate_globals(env,globals_module=template_globals):
    all_functions = inspect.getmembers(globals_module, inspect.isfunction)
    for name, function in all_functions:
        env.globals[name]=function
    return env
def extract_module_names(package):
    package_path = package.__path__
    prefix = package.__name__+"."
    modules=[]
    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        modules.append(name)
    return modules

def populate_filters(env,filters_package=template_filters):
    module_names = extract_module_names(filters_package)
    for module_name in module_names:
        filter_module =importlib.import_module(module_name)
        #filters which are built in  jinja do not need to be added
        if hasattr(filter_module, "get_template_filter"):
            get_filter_func=getattr(filter_module, "get_template_filter")
            filter_func =get_filter_func()
            env.filters[filter_func.__name__]=filter_func
    return env
def populate_filters_and_globals(env):
    populate_filters(env)
    populate_globals(env)

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
        populate_globals(self.env)
        populate_filters(self.env)
    def get_env(self):
        return self.env
