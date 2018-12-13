from sql_gen.docugen.template_renderer import TemplateRenderer
from sql_gen.docugen.environment_selection import TemplateSelector
import argparse
from sql_gen.emproject import SQLTask
from sql_gen import app
import sys
from sql_gen.sqltask_jinja import initial_context

logger =app.logger
##main
def run_app():
    try:
        do_run_app()
    except KeyboardInterrupt as excinfo:
        logger.exception(excinfo)
        print( '\n KeyboardInterrupt exception')
    except Exception as excinfo:
        logger.exception(excinfo)
        print(excinfo)

def do_run_app():

# construct the argument parse and parse the arguments
    args = parse_args();
    logger.info("Arguments passed: "+str(sys.argv))
    sql_task_path = args.dir

    sql_task = None
    if sql_task_path:
        try:
            sql_task = SQLTask(root=app.root,config=app.config)
            sql_task.with_path(sql_task_path)
        except AttributeError as e:
            logger.error(str(e))
            exit()
        except FileExistsError as e:
            print("Exiting application")
            exit()
    else:
        print ("\nWARNING: SQL generated will NOT be saved. It only prints to screen. Check --help for options on how to save to a file")

    rendered_text=""
    template_renderer = TemplateRenderer()
    current_parsed_template = template_renderer.run(dict(initial_context))
    rendered_text +=current_parsed_template+"\n\n"
    while current_parsed_template is not "":
        current_parsed_template = template_renderer.run(dict(initial_context))
        rendered_text +=current_parsed_template+"\n\n"
    logger.debug("No more sql task to run")
    if sql_task:
        logger.debug("About to write sqltask to disk")
        sql_task.with_table_data(rendered_text);
        sql_task.write()
    else:
        logger.debug("About to print to screen")
        print("\n"+rendered_text+"\n")
    logger.debug("Exiting sqltask")

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
    return ap.parse_args()

if __name__ == '__main__':
    main()

