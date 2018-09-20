from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.sql_gen_app import run_app
 
##main
def main():
    run_app()

if __name__ == '__main__':
    main()

