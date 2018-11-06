from sql_gen.sql_gen.template_renderer import TemplateRenderer
from sql_gen.sql_gen.environment_selection import TemplateSelector
import argparse
from sql_gen.emproject import SQLTask
from sql_gen.ui.cli_ui_util import do_not_print_stack_trace_on_ctrl_c

do_not_print_stack_trace_on_ctrl_c()



##main
def run_app():
 # construct the argument parse and parse the arguments
    args = parse_args();
    sql_task_path = args.dir
    sql_task = None
    if sql_task_path:
        try:
            sql_task = SQLTask()
            sql_task.with_path(sql_task_path)
        except AttributeError as e:
            print(str(e))
            exit()
        except FileExistsError as e:
            print("Exiting application")
            exit()
    else:
        print ("\nWARNING: SQL generated will NOT be saved. It only prints to screen. Check --help for options on how to save to a file")

    rendered_text=""
    template_renderer = TemplateRenderer()
    current_parsed_template = template_renderer.run()
    rendered_text +=current_parsed_template+"\n\n"
    while current_parsed_template is not "":
        current_parsed_template = template_renderer.run()
        rendered_text +=current_parsed_template+"\n\n"

    if sql_task:
        sql_task.with_table_data(rendered_text);
        sql_task.write()
    else:
        print("\n"+rendered_text+"\n")

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", help="Its the directory where the sql task will be written to. Its a relative path from  $CORE_HOME to, e.g. modules/GSCCoreEntites...")
    return ap.parse_args()

if __name__ == '__main__':
    main()

