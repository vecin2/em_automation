# Developer Guide


### Developer Setup

Branch this project and submit merge request.

Consider creating a virtual python environment for this project. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) can be used to manage your virtual environment.

In ubuntu,ensure the following packages are installed as they required to build pyodbc: `sudo apt-get install unixodbc unixodbc-dev`
Within your virtualenv run: pip install -r requirements.txt

#### Linux
If you are using `virtualenvwrapper`  for Linux systems you add the above line to `<virtualenv.home>/bin/postactivate`

Make sure the `ccdev`  is  reachable from your `PYTHONPATH`:
`export PYTHONPATH=${PYTHONPATH}:/home/dgarcia/dev/python/em_automation`

#### Windows

Install virtualenvwrapper-win: C:\Python38\python.exe -m pip install virtualenvwrapper-win
virtualenvwrapper-win does not have `postactivate` modify `Scripts\activate.bat` and add the following:
```
@set "PYTHONPATH=%PYTHONPATH%;C:\\Users\\dgarcia\\dev\\python\\em_automation"
```

#### Running tests
Run: `pytest` from the project's root folder and, make sure test are passing

To execute application run `python ccdev` from root folder.


### Imlementing new Global functions

Global functions can be implemented by adding a new function to the `globals.py` module. The function is added automatically to the template environment and therefore will be available for templates to use it.

### Implementing new Filters

Filters are picked up by the environment by name convention. The system looks for classes under the `/filters` with class name matching the capitalize name of the filter +"Filter". For example:

```sql
#Template
{{ var_name | default("Test default") }}

#Searches for class named "DefaultFilter" under the folder /filters
```

Filter can be either:

- Completely new filters, e.g. `DescriptionFilter`
- Wrappers of builtin jinja filters, e.g. `DefaultFilter`

Wrappers which part of the builtin jinja filters do not need to be added to the environment so implementing `apply` should be enough:

_class_ sql_gen.filters.**DefaultFilter**()
string :: **apply**(prompt_text)
It takes the prompt text and it changes it accordingly to what it should be display to the user. Multiple filters can be concatenated.

When creating a new filter we need to implement not only `apply` but `get_template_filter` which is invoked by the application to add the filter to the environment.

_class_ sql_gen.filters.**DescriptionFilter**()
func :: **get_template_filter**()
It returns the function which implements the jinja filter.

### Create Windows Executables

On Windows machine:

- Install python 3.8.1: choco install python --version=3.8.1
- Install virtualenvwrapper on that python installation: C:\Python38\python.exe -m pip install virtualenvwrapper-win
- Create a virtualenv em_automation
- pip install -r py_installer_requirements.text

If a package fails to compile .e.g cx_oracle you can downloaded the .whl file directly from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/
Copy the file to project location and run: pip install <<filename>>

#### Troubleshooting

Py_installer compatibility issues with 3.8 or above at October 24th 2022: https://github.com/pyinstaller/pyinstaller/issues/4265#issuecomment-554624172
Python 3.10 has a comptability issue with py_installer ends up with following error: ImportError: No module named \_bootlocale

To fix this, run `pyinstaller.exe app.py --exclude-module _bootlocale`
