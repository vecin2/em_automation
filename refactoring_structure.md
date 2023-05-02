database
    database.py (Connector and EMDatabase)
    query_runner.py
    sql

print_sql

mainMenu???

main
    command_factory
    command_line_app
    docopt_parser
    project_home --> move to project

sqltask_templating
    sqltask_env
    context (builds INITIAL context API and has keynames)
    globals
    filters
        codepath
        other

templating
    environment
        env_builder (filesystemloader,envbuilder,traceUndefined)
        source_inspector
    general_filters
        default
        description
        print
        prompt_filter
        
    substitution| filling
        prompt_visitor
        prompt
        template_filler (based on a values_dict, computes the next prompt, inlines and clear var from TraceUndefined) --> Templat
        template_inliner
        template_context (does the actual rendering)

    rendering
        inmemory_template_renderer

    completer --> move to ui

template_rendering
    reder_template_hanlder

    
