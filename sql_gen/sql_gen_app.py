from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource
from sql_gen.prompter import Prompter
from sql_gen.environment_selection import TemplateSelector, EMTemplatesEnv
import argparse
from sql_module.em_project import SQLTask
import os


##main
def run_app():
 # construct the argument parse and parse the arguments
    args = parse_args();
    sql_task_path = args.dir

    env = EMTemplatesEnv().get_env()
    print("hola" + str(env.get_template("add_process_descriptor.sql")))
    templates_path =os.environ['SQL_TEMPLATES_PATH']
    print(templates_path)
    template_selector = TemplateSelector()
    template_source= template_selector.select_template(env)
    prompter = Prompter(template_source)
    context = prompter.build_context()
    template = env.get_template(template_source.template_name)

    template_parsed =template.render(context)

    if sql_task_path:
        sql_task = SQLTask.make().path(sql_task_path).with_table_data(template_parsed);
        sql_task.write()
    else:
        print(template_parsed)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
    return ap.parse_args()
    

if __name__ == '__main__':
    main()

