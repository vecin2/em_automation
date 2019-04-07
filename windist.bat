echo off

pyinstaller cli.py --onefile --hidden-import sql_gen.log.handlers --hidden-import sql_gen.sqltask_jinja.filters.default --hidden-import sql_gen.sqltask_jinja.filters.codepath --hidden-import sql_gen.sqltask_jinja.filters.description --hidden-import sql_gen.sqltask_jinja.filters.suggest]  --add-data sql_gen/log/logging.yaml;sql_gen/log --name dtask
