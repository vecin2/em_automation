![img](https://raw.githubusercontent.com/vecin2/em_automation/master/docs/rewiring_verb.gif)
# sqltask - an sql generator for EM projects
sqltask is command line application that helps users generating SQL scripts. Each script is created as a template, sqltask then parse th template to identify the diferent variables and it prompts them to the user. Once all the variables are entered it renders the template and sends the result to the corresponding output.

Templates are written using [jinja templates syntax](http://jinja.pocoo.org/)  and they should be designed in a way that they provide enough information to users when filling template values, and they should minimize user interactions, avoiding asking for values that could be computed.


# Table Of Contents

- [sqltask - a sql generator for EM projects](#sqltask---an-sql-generator-for-em-projects)
- [Table Of Contents](#table-of-contents)
- [Basic Usage](#basic-usage)
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

## Basic Usage      
### Add New Templates 
To create a new template create a file with `.sql` extension under `$SQL_TEMPLATES_PATH`

#### Hide a Template
A hidden template is not display among the templates to be filled. They are created so they can be reused and included in other templates but they don't make much sense on their own. 
Template can be hidden by adding the template under a folder called "hidden_templates" within the main template folder.

# User installation

- Install [python3](https://www.python.org/downloads/) and make sure you remember the path where is installed. 
 - When running the installation make sure to select the checkbox to add python3 to your system path. For example, In windows the default python home installation path is: `%UserProfile%\AppData\Local\Programs\Python\Python37-32`
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
For EM developement there are a set templates which implement basic tasks, e.g. add a verb, add an entiy, etc...
These Templates will be provided on demand. 

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
## Objects in context
There is a set of objects which included whithin the template context and they provide support when writting templates.

The objects are put into context with underscore (_) prefix this is to avoid clashing with template variables names.

### _keynames
It retrieves a list of relative ids for the key set passed. For example:
 - _keynames.ED: retrieves a list of the entity defintions relative ids
 - _keynames.V: retrieves a list of the verbs relative ids

### _db
It allows to run a predefined set of queries defined within `config/ad_queries.sql`:

**fetch.<<query_name>>**(_\*query_params_)
It returns a `SQLTable` object (list of dictionaries). For example:
 - `_db.list.v_names_by_ed(entitfy_id)`
 - `_db.find.pd_by_ed_n_vname(entity_id, v_name)`
 
**find.<<query_name>>**(_\*query\_params_)
It returns a `SQLTable` object with one row.  Similar to `fetch` but this is used when searching by a unique constraint field and it throws and exception if nonne or more than one record are found. For example
 - `_db.find.pd_by_ed_n_vname(entity_id, v_name)`


### _database
 Same as `_db` but allows running free form queries instead of dictionary queries:
 
**fetch**(_query_string_)
It returns a `SQLTable` object (list of dictionaries). For example:
 -`_database.fetch("SELECT NAME FROM VERB where name like '%create%'")`
 
 **find**(_query_string_)
 -`_database.find("SELECT * FROM VERB where name='my_verb'")`

 
### SQLTable
This object is not in context but is retrieved by `_db.find` or `db.fetch`. It is a list of dictionaries. It has the following method to allow extract data from the query result easily:
**column(name)**
Returns the column as a list:
   `assert [1,2] == table.column("ID")`
    

### _emprj
 It extract different information from the current EM project:
 
**prj_prefix**()
It  returns the project prefix of the current `EM_CORE_HOME` project. 
It looks for modules under `$EM_CORE_HOME/repository/default` starting with uppercase letters which are repited. It returns empty if it can't find any.
For example with a set modules like
```sql
#With a foder strtuctre like this under $EM_CORE_HOME
/repository/default
				|__ ABCContactHistory
				|__ ABCCaseHandling
				|__ ...
#Template
 {% set process_id = __prj.prefix() %}
Process id is {{process_id }}
#Renders
Process id is ABC
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

#Renders
Display Name is 'Change the address'
Name is 'changeTheAddress'
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

#Renders
Process descriptor id is Customer
```
## Include
Include allows wrapping other templates so they can be reused and avoid SQL code duplication.  We might want to set some variables contained within the included template before call that template so it doesn't prompt them.
```sql
#Compute descriptor id  which is used in 'add_process_descriptor.sql'
{% set process_id = __prjprefix + entity_id.capitalize() + verb_name.capitalize() -%}

{% include 'add_descriptor.sql' %}
{% set descriptor_ref_id = descriptor_id %}
{% include 'add_descriptor_ref.sql' %}
```
## Naming Convention 
The following name and convention is used when writing tempaltes:
- Template variables names follow snake case e.g "customer_name"
 - Context config variables, which are defined under `config/context_values.yaml` start with an underscore to distinguish them from template variables
 - Internal variables are named as the variabled but prefixing two underscores. Internal variables are used when we capturing a value that will be used later on within the same template.
```
{% set __entity_display_name = entity_display_name 
								   | default(default_display_name)%}
```

##  Fomatting 
All SQL scripts are written in uppercase with the variables in lower case and snake case. 
#### Inserts
For easy reading the values inserted are indented within the brackets and a comment with the field name added next to it.
```sql
INSERT INTO PROCESS_REFERENCE (ID, PROCESS_ID,CONFIG_ID, IS_SHARED) 
VALUES (
        @PDR.{{process_reference_id}} --id,
        @PD.{{process_descriptor_id}}, --process_descriptor_id
		NULL, --config_id
       	'N' --is_shared
       );
```

# Logging
The application logging is configured by default to write to the logs dir within the main application folder. 
Logging configuration can be modified by creating a file called `logging.yaml` under the app config folder.
This is a example of a valid configuration file:
```yaml
version: 1
disable_existing_loggers: False
formatters:
    simple:
        format: "%(asctime)s - %(levelname)s - %(message)s"
handlers:
    console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple
        stream: ext://sys.stdout

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
        handlers: [console,info_file_handler]
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









<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIxMDUxNTM5OF19
-->

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1NzQyNTAwNCwxNTIwNDE5NzEsMTc1Nz
QzMDY1NSwtMjA5Mzk5NDE2NywtMjEwNTE1Mzk4XX0=
-->