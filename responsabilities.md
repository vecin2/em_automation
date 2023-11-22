# Find a template
The system provides a fuzzy finder to find a specific template
System provides information about a template to help the user make an inform decision on what template to pick



## TaskSelector


The system reads from  a library of templates
Different actions can 
Multiple Templates can be selected output will com


input is entered

    args =parser.parse(input)
    RunSQLHandler
        getAction(args).run(args.template)
        
    if args.template

    

Input is entered on a prompt
As text is entered suggestions show up:
If user is entering first words, then list of all the actions should show up.
Once the user entered the first word it should display the suggestions for the actions

The completer needs to get the command from the first word entered. The comp
Completer:
    - Completes both actions(template names +exit) and args
    - Completer needs access to the list of commands

System must parse the input to find the command (action)


## Modules

- cli_template/interactive_temlate/template_filling/template_prompting: Interactive jija templates. Using jinja library, it finds the undefined template vars and it prompts the to the user on the command line. Provides a framework easily adding other filters into the environment and to modify the initial context.
    - jinja
        - builtin filters: default, description,filepath,print , prompt, suggest
        - engine: prompt_visitor,template_context, template_inliner
    - builtin completions: filepath,database_fetches
    - collection/library: manages a collections of templates (find)
    - commands:
        - render: prompts for template values and when it's finished it return the template rendered with those values
        - test: provides a mechanism to test templates by running the template with test values passed in an comparing the output against an expected text.

- sql: everything related with sql templates. SQL templates a
puts a database object into ijinja context which allows to run the template against a database and also to provide suggestions while filling up the template
- library: everything related with managing a collection of templates:
    - find a template including prompt to select template with help methods (view,edit)
    - view, edit use test, test specific to 
    - generate docs
    - library of templates which have metadata
- em: everything related with an em project that includes:
    - create-sql command

