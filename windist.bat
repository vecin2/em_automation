REM A couple of issues found when creating distributions in windows:
REM 1. pymsql needs Visual cpp build tools (around 4GBs) to be able to compile and create the whl file
REM    Its possible to download the whl file directly and install it from it 
REM    Url is https://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
REM 2. The other issue we might encounter is that setuptools needs to be downgraded to 44.0.0
echo off
pyinstaller ccdev/__main__.py --onefile --hidden-import sql_gen.log.handlers --hidden-import sql_gen.sqltask_jinja.filters.default --hidden-import sql_gen.sqltask_jinja.filters.codepath --hidden-import sql_gen.sqltask_jinja.filters.description --hidden-import sql_gen.sqltask_jinja.filters.suggest --hidden-import sql_gen.sqltask_jinja.filters.other --hidden-import sql_gen.sqltask_jinja.filters.print  --add-data sql_gen/log/logging.yaml;sql_gen/log --name sqltask
