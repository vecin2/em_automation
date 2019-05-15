echo off

pyinstaller sql_gen/__main__.py --onefile --hidden-import sql_gen.log.handlers --hidden-import sql_gen.sqltask_jinja.filters.default --hidden-import sql_gen.sqltask_jinja.filters.codepath --hidden-import sql_gen.sqltask_jinja.filters.description --hidden-import sql_gen.sqltask_jinja.filters.suggest --hidden-import sql_gen.sqltask_jinja.filters.other]  --add-data sql_gen/log/logging.yaml;sql_gen/log --name dtask
