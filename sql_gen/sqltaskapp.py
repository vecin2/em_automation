from sql_gen.docugen.template_renderer import TemplateRenderer
from sql_gen.docugen.environment_selection import TemplateSelector
import argparse
from sql_gen.emproject import SQLTask
from sql_gen.app_project import AppProject
import sys
import os
#from sql_gen.sqltask_jinja import initial_context
import sql_gen.sqltask_jinja.context as jinjacontext
from sql_gen.docugen.environment_selection import TemplateSelector
from sqltask_jinja.sqltask_env import EMTemplatesEnv

app = None
logger =None
def init():
    global app, logger
    app = AppProject()
    logger = app.setup_logger()
    logger.info("Initializing app which is pointing currently to '"+app.emproject.root+"'")

def run():
    try:
        do_run_app()
    except KeyboardInterrupt as excinfo:
        logger.exception(excinfo)
        print( '\n KeyboardInterrupt exception')
    except Exception as excinfo:
        logger.exception(excinfo)
        raise(excinfo)

class TemplateFillerApp(object):
    def __init__(self,env, listener):
        self.listener = listener
        self.env = env

    def run(self):
        template_selector = TemplateSelector(self.env)
        template_renderer = TemplateRenderer(self,template_selector)
        initial_context= jinjacontext.init(app)
        template_renderer.run(dict(initial_context))

    def template_filled(self, template,context):
        self.listener.template_filled(template,context)
        self.run()

    def finished(self):
        """this is  called when user press x to exit"""
        self.listener.finished()

class SQLTaskApp(object):
    def __init__(self,sqltask):
        self.sqltask =sqltask

    def run(self):
        env = EMTemplatesEnv().get_env(os.environ)
        template_filler_app = TemplateFillerApp(env,self)
        template_filler_app.run()

    def template_filled(self, template,context):
        self.sqltask.template_filled(template,context)

    def finished(self):
        """this is  called when user press x to exit"""
        self.sqltask.write()



def do_run_app():
# construct the argument parse and parse the arguments
    logger.info("Application invoked with these arguments: "+str(sys.argv))
    args = parse_args();
    sql_task_path = args.dir
    try:
        sqltask = SQLTask.make(sql_task_path)
    except AttributeError as e:
        logger.error(str(e))
        exit()
    except FileExistsError as e:
        print("Exiting application")
        exit()

    if not sql_task_path:
        print ("\nWARNING: SQL generated will NOT be saved. It only prints to screen. Check --help for options on how to save to a file")

    sqltaskApp = SQLTaskApp(sqltask)
    sqltaskApp.run()

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
    return ap.parse_args()

if __name__ == '__main__':
    main()

