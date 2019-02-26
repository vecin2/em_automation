![img](https://raw.githubusercontent.com/vecin2/em_automation/master/docs/rewiring_verb.gif)
# sqltask - an sql generator for EM projects
sqltask is command line application that helps users generating SQL scripts. Each script is created as a template, sqltask then parse th template to identify the diferent variables and it prompts them to the user. Once all the variables are entered it renders the template and sends the result to the corresponding output.

Templates are written using [jinja templates syntax](http://jinja.pocoo.org/)  and they should be designed in a way that they provide enough information to users when filling template values, and they should minimize user interactions, avoiding asking for values that could be computed.


# Table Of Contents

- [sqltask - a sql generator for EM projects](#sqltask---an-sql-generator-for-em-projects)
- [Table Of Contents](#table-of-contents)
- [Basic Usage](#basic-usage)
    + [Creating  a SQL Task](#creating--a-sql-task)
    + [Exiting the application](#exiting-the-application)
    + [Show help](#show-help)
    + [Adding New Templates](#adding-new-templates)
      - [Hidding a Template](#hidding-a-template)
- [User installation](#user-installation)
    + [Windows Console Tools](#windows-console-tools)
- [Template Design](#template-design)
  * [Filters](#filters)
    + [Concatenate multiple filters](#concatenate-multiple-filters)
    + [List of Builtin filters](#list-of-builtin-filters)
  * [Global Functions](#global-functions)
  * [List of Global Functions](#list-of-global-functions)
  * [String Python Builtin Functions](#string-python-builtin-functions)
  * [Fomatting and Naming Convention](#fomatting-and-naming-convention)
      - [Inserts](#inserts)
- [Build Extensions](#build-extensions)
    + [Developer Setup](#developer-setup)
      - [Running tests](#running-tests)
    + [Imlementing new Global functions](#imlementing-new-global-functions)
    + [Implementing new  Filters](#implementing-new--filters)

      
# Basic Usage
This section run through the steps of generating a SQL script:

- [Add a new template](#adding-new-templates) called `change_verb_context2.sql`:
```sql
UPDATE EVA_CONTEXT_VERB_ENTRY
SET (CONFIG_ID)= (@CC.{{new_config_id | description("new_config_id (e.g. Home, CustomerPostIdentify, ...)")}})
where CONFIG_ID = @CC.{{old_config_id} | default("NULL")}
and VERB = '{{verb_name}} ';
```
- Run the application by simply typing `sqltask` in the comand line. The new template should show as one of the options.
-  Select the template, and starting filling the values as they are prompted:
```bash
	new_config_id (e.g. Home, CustomerPostIdentify, ...): 
	old_config_id (default is NULL): 
	verb_name: 
```
- Assuming `Customer`, `Home` and `indentifyCustomer` are entered as values the template will be render and printed out as following:
```sql
	UPDATE EVA_CONTEXT_VERB_ENTRY
	SET (CONFIG_ID)= (@CC.Customer)
	where CONFIG_ID = @CC.Home
	and VERB = 'identifyCustomer';
```
### Create  a SQL Task
``` 
sqltask -d modules/ABCustomer/sqlScripts/oracle/updates/Project_R1_0_0/add_policy_to_Customer_table
```
Where `d` value is the SQL task relative path from the current `EM_CORE_HOME`. The template will be rendered to file called `tableData.sql` and an `update.sequence` file will generated as well.

### Exit the application
At any point press `Ctrl+c` or `Ctrl+d` to exit.  When using Gitbash in Windows it might require to hit `Enter` after  `Ctrl+c` or `Ctl+d`.

### Show help
Running `sqltask -h`  to show a help description:
```
optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  It's the directory where the sql task will be
                     written to.
                     Its a relative path from $EM_CORE_HOME to, e.g.
                     modules/GSCCoreEntites...
```
### Add New Templates 

To create a new template:

- Create a file with `.sql` extension under `$SQL_TEMPLATES_PATH`
- Create an empty file with the same name pointing to the previous file under `$SQL_TEMPLATES_PATH/menu` - make sure the names match otherwise it will not show up in the menu when running the application.

#### Hide a Template
Template can be hidden by simply not creating the shorcut

It is a good practice to reuse templates to avoid duplicating SQL code. Therefore a template can be created to support other templates but it shouldn't be displayed to users. Instead display only the wrapping templates.

# User installation

- Install [python3](https://www.python.org/downloads/) and make sure you remember the path where is installed. In windows the default python home installation path is: `%UserProfile%\AppData\Local\Programs\Python\Python37-32`
 - When running the installation make sure to select the checkbox to add python3 to your system path
- Check the python installation folder was added to the the system path. If is not added you can added manually:
 - In windows add the following to you path variable: %PYTHON_HOME%;%PYTHON_HOME%/Scrips;
 - Copy the template folder to some location in your filesystem. For example under the current EM project. 
- Add the following environment variables:
	- `PYTHON_HOME` is the python installation folder. 
	- `EM_CORE_HOME` is the current EM project, e.g. `/opt/em/projects/gsc` 
	- `SQL_TEMPLATES_PATH` is the folder containing the sql templates. e.g. `/opt/em/projects/my_project/sql_templates `

- Install [sqltask](https://test.pypi.org/project/sqltask/) by typing the following  command line:
```
python -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask
```
 
This should install all the required packages including [jinja2 templates](http://jinja.pocoo.org/).  If you find issues when running sqltask where it can't find jinja you can install it manually by running 
`python3 -m pip install Jinja2`.
 
###  Upgrade
The application can be updated by running `python3 -m pip install --upgrade sqltask` 
Otherwise uninstall and intall  by running:

```
python3 -m  pip  uninstall sqltask
python3 -m  pip  install sqltask
``` 

### Multiple versions of python 
 If you have multiple versions of python installed make sure you are using version 3 by running instead:
```
python3 -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask
```

This applies as well when running upgrades and any python command it - e.g `python3 -m pip  install update sqltask`

###  Install builtin Templates
A set of builtin templates are downloaded when running pip install. They are located under `%PYTHON_HOME%/Lib\site-packages\sql_gen\templates`
Copy this folder under your `%EM_HOME_CORE%` so new creates templates are not lost when upgrading. As well committing in the project folder will allow commit it so other developers can benefit from it.

### Windows Console Tools
If you find the Windows console is too slow, e.g no path autocompletion,  hard copy and paste, etc, you can  look at other options:
- [Clink]( http://mridgers.github.io/clink/): very light weight tool which add a set features to the Windows console.
- [git-bash](https://gitforwindows.org/): its a different terminal which allows  bash-style autocompletion as well and several linux commands. 
- [cygwin](https://www.cygwin.com/): a large collection of GNU and Open - Source tools which provide functionality similar to a Linux distribution on Windows. 
 

# Template Design

How template values are prompted to the user is determined entirely by how the template is written. So having a set of well designed templates is the key for generating scripts rapidly. 

The syntax is defined by python jinja templates. Check the [template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/).

## General guidelines
When design templates consider the following:
-  A value should be prompted with enough information so the user knows how to fill it.
- When possible provide a subset of values for the user to pick from.
- Users should NOT be prompted any value that can be computed from some other values - finding the minimum set of values is key. 
- Avoid duplicating SQL code, reuse template by including them within others. So when a product DB table changes it avoids having to change multiple templates.
- Review existing templates or consult this documentation to understand what filters and templates are available.

To design good templates is important to know what elements are available when writting templates. As follows it is documented the current filters and functions that can be used within templates. 
You can check as well the existing templates for a goo understanding on how these elements are applied.

## Filters
Jinja Templates use [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters),  which can modify variables when rendering the template. For example `{{ name|default('NULL') }}`  will use `NULL` if the user doesn't enter any value.

The issue is that in some cases the application should notify users that a filter or a set of filters is apply to that value,  otherwise the user will not understand why his value is changed.  For example  `{{ name|default('NULL') }}` should show a display message  like `name (default is NULL):`, rather than simply `name:`
 
 So sqltask filters mainly affect the text that is shown to the user when prompting for a value.

Altough  we should have almost one sql task filter per each jinja filter, not all the jinja filters have an equivalent filter in our application. To understand which filters are available check the [list of builtin filters](#list-of-builtin-filters) 

### Concatenate multiple filters
Filters can be concatenated:
```sql
#template
{{ my_variable| description('Enter any value' 
              | default('my_variable is not defined')}} 

#prompts
Enter any value (default  is  'my variable is not defined'):

## Notice that description filter will override any other filter
## so if the order of the pipe changes description will override
## everything that was applied before.
```

### List of Builtin filters
In this section we only detail how the filters affect value prompts, we do not explain how it modifies the variable when rendering the template. For details on that check the [list of builtin jinja filters](http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters).

**default**(_value_,  _default_value=u''_,  _boolean=False_)
It appends  `default_value` to the variable name when prompting:
```sql
#template
{{ my_variable| default('my_variable is not defined') }}

#prompts
my_variable (default is 'my variable is not defined'):

```
**description**(_value_,  _description_)
It shows the `description` when prompting the user. 
This is not a builtin jinja filter and it does not modify the variable entered by the user. 

```sql
{{ my_variable| description("Please enter 'my_variable_value`') }}

#prompts
Please enter 'my_variable_value`:
```

## Global Functions
There is a set of builtin global functions which can be used when writting templates.  Functions can be invoke within blocks `{% %}` or within statements `{{ }}`.

### List of Builtin Global Functions
To the existing [list of jinja builtin global functions](http://jinja.pocoo.org/docs/2.10/templates/#builtin-globals) we have added the following:

**camelcase**(_value_)
It  returns the _value_ passed in camelcase:
```sql
#Template
{% set display_name = "Change the address" %}
{% set name = camelcase(display_name) %}
Display Name is  '{{display_name}}'
Name is '{{ camelcase(display_name }}'

#Rendered
Display Name is 'Change the address'
Name is 'changeTheAddress'

```
**prj_prefix**()
It  returns the project prefix of the current `EM_CORE_HOME` project. 
It looks for modules under `$EM_CORE_HOME/repository/default` starting with at least 3 uppercase letters. It throws an exception if it can't find any.
For example with a set modules like
```sql
#With a foder strtuctre like this under $EM_CORE_HOME
/repository/default
				|__ ABCContactHistory
				|__ ABCCasHandling
				|__ ...

#Template
 {% set process_desc_id = prj_prefix()+ entity_def_name %}
Process descriptor id is {{process_desc_id }}

#Rendered
Process descriptor id is ABC
Name is changeTheAddress
```
## String Python Builtin Functions
Python string functions can be used within templates, for example:

**capitalize**()
It returns the current string capitalize. 
```sql
#Template
{% entity_def_id = 'customer' %}
{% set process_desc_id = entity_def_id.capitalize %}
Process descriptor id is {{process_desc_id }}

#Rendered
Process descriptor id is Customer
```
## Include
Include allows wrapping other templates so they can be reuse and avoid SQL code duplication. 
```sql
#Compute descriptor id  which is used in 'add_process_descriptor.sql'
{% set process_descriptor_id = prj_prefix()+ entity_def_id.capitalize() + verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}
{% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'add_process_descriptor_ref.sql' %}
```

##  Fomatting and Naming Convention 
All SQL scripts are written in uppercase with the variables in lower case and snake case. 

#### Inserts
For easy reading the values inserted are indented within the brackets and a comment with the field name added next to it.
```sql
INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) 
VALUES (
        @PDR.{{process_descriptor_ref_id}} --id,
        @PD.{{process_descriptor_id}}, --process_descriptor_id
		@ENV.Dflt, --env_id
		NULL, --config_id
       	'N' --is_shared
       );
```

# Logging
The application logging is configure by default to write to the logs dir within the main application folder. 
Logging configuration can be modify by creatng a file called `logging.yaml` under the app config folder.
This is a example of a valid configuration file:
```yaml
version: 1
disable_existing_loggers: False
formatters:
    simple:
        format: "%(asctime)s - %(levelname)s - %(message)s"
handlers:
    info_file_handler:
        class: sql_gen.log.handlers.MakeRotatingFileHandler
        level: INFO
        formatter: simple
        filename: information.log
        maxBytes: 10485760 # 10MB
        backupCount: 20
        encoding: utf8
loggers:
    app_logger:
        level: INFO
        handlers: [console,info_file_handler, error_file_handler]
        propagate: no
root:
    level: INFO
    handlers: [info_file_handler]
```

# Build Extensions
### Developer Setup

Branch this project and submit merge request. 

Consider create a virtual pyhon  envioronment for this project.   As well, it is recomended to user [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to  manage your virtual environment. 

Make user the sql_gen folder is added to you `PYTHONPATH`:
`export PYTHONPATH=${PYTHONPATH}:/home/dgarcia/dev/python/em_automation/sql_gen`

If you are using virtual environment you can set the `PYTHONPATH` within the `$vitualevn/bin/postactivate` so it only runs when you activate this environment.

The application can be executing by running: `python sql_gen` from project top folder.

#### Running tests
Test can run with pytest: py.test from the project top folder


### Imlementing new Global functions
Globals functions can easily implemented by adding the function to the `globals.py` module. The function is added automatically to the template enviroment and therefore available for templates to use it.

### Implementing new  Filters
 Filters are picked up by the environment by name convention. The system looks for classes under the `/filters` whith the class name matching the capitalize name of the filter +"Filter". For example:
 ```sql
 #Template
 {{ var_name | default("Test default") }}

#Searches for class named "DefaultFilter" under the folder /filters
 ```

Filter can be either:
- Completely new filters, e.g. `DescriptionFilter`
- Wrappers of builtin jinja filters, e.g. `DefaultFilter`

In the first case filters do not need to be added to the environment so implementing `apply` should be enough:

_class_ sql_gen.filters.**DefaultFilter**()
		string :: **apply**(prompt_text)
It takes the prompt text and it changes it accordingly to what it should be display to the user. Multiple filters can be concatenated.

When creating new filter we need to implement  not only `apply` but  `get_template_filter` which is invoked by the application to add the filter to the environment.

_class_ sql_gen.filters.**DescriptionFilter**()
		func :: **get_template_filter**()
It returns the function which implements the jinja filter.
