REM A couple of issues found when creating distributions in windows:
REM 1. pymsql needs Visual cpp build tools (around 4GBs) to be able to compile and create the whl file
REM    Its possible to download the whl file directly and install it from it
REM    Url is https://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
REM 2. The other issue we might encounter is that setuptools needs to be downgraded to 44.0.0
echo off
REM Please notice that all the dependecies must be installed. If using virtualenvwrapper use windows command line, not powershell
pyinstaller ccdev/__main__.py --onefile --hidden-import sqltask.log.handlers --hidden-import sqltask.sqltask_jinja.filters.default --hidden-import sqltask.sqltask_jinja.filters.codepath --hidden-import sqltask.sqltask_jinja.filters.description --hidden-import sqltask.sqltask_jinja.filters.suggest --hidden-import sqltask.sqltask_jinja.filters.other --hidden-import sqltask.sqltask_jinja.filters.print  --add-data sqltask/log/logging.yaml;sqltask/log --name sqltask
copy dist\sqltask.exe %USERPROFILE%\AppData\Local\Microsoft\WindowsApps
