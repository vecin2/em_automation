![img](https://raw.githubusercontent.com/vecin2/em_automation/master/docs/example.gif)
# sqltask - an sql generator for EM projects
`sqltask` is command line application that helps users generating SQL scripts.

User creates a template for each SQL script,  then `sqltask` parses the template variables variables and it prompts them to the user.

After user enters the values `sqltask` renders the template and it generates the final SQL script, which can be either printed, saved as an SQL task or run in the database.

Templates are written using [jinja templates syntax](http://jinja.pocoo.org/)  and they should be designed in a way that they provide enough information to users when filling the values, and they minimize user interactions and avoid asking for values that could be computed.


# Table Of Contents
- [sqltask - an sql generator for EM projects](#sqltask---an-sql-generator-for-em-projects)
- [Table Of Contents](#table-of-contents)
  * [Basic Usage](#basic-usage)
  * [Tutorials](#tutorials)
  *  [Key Shortcuts](#key-shortcuts)
- [User installation](#user-installation)
  * [Quick installation](#quick-installation)
- [Template Design](#template-design)
  * [General guidelines](#general-guidelines)
  * [Filters](#filters)
    + [Concatenate multiple filters](#concatenate-multiple-filters)
    + [List of Builtin filters](#list-of-builtin-filters)
  * [Objects in context](#objects-in-context)
    + [_keynames](#-keynames)
    + [_db](#-db)
    + [_database](#-database)
    + [_emprj](#-emprj)
  * [More Available Objects](#more-available-objects)
    + [SQLTable](#sqltable)
    + [SQLRow](#sqlrow)
  * [Global Functions](#global-functions)
    + [List of Builtin Global Functions](#list-of-builtin-global-functions)
  * [String Python Builtin Functions](#string-python-builtin-functions)
  * [Include](#include)
  *  [Hidden Templates](#hidden-templates)
  * [Organizing Templates](#organizing-templates)
  * [Naming Convention](#naming-convention)
  * [Fomatting](#fomatting)
      - [Inserts](#inserts)
- [Logging](#logging)
- [Build Extensions](#build-extensions)
    + [Developer Setup](#developer-setup)
      - [Running tests](#running-tests)
    + [Imlementing new Global functions](#imlementing-new-global-functions)
    + [Implementing new  Filters](#implementing-new--filters)


## Basic Usage
Create a `hello_world.sql` file under within the`$EM_PROJECT/project/sqltask/templates` folder.
Add the following text:   `Hello {{ name }}!`
Run sqltask print-sql and when prompt select the template `hello_world.sql`. You should see you  `name` being prompted.

## Tutorials
Within the templates there is a set of tutorials templates They provide good guide and practical examples on how templates are created. Feel free to change them to see how it impacts the prompting.

## Controls
-	"<": If user enters "<" when is prompted a value, the application will go back and prompt the previous value.
-	Ctrl + n: Navigate to the "next" option within a list of suggestions.
-	Ctrl + p: Navigate to the "previous" option within a list of suggestions.
-	TAB: pops up a list of suggestion if there is one or navigate to the next one if the list is already showing.
-	Shift + TAB: Navigate to the previous option within a list of suggestions.
-	Ctrl + w: Removes the previous word that was typed.

# User installation
## Quick installation
 1. Unzip  "sqltask.zip" into your `$EM_PROJECT/project` folder.
 2. Within the `config/core.properties` file:
	 -  Change the environment, container and machines names to point to your local environment.
	 - Change the `db.release.version`  property to point to your current AD release version.
 3. Drop the executable file within your `bin` folder of your current EM project (next to your ccadmin)
 4. Run `sqltask test-sql` from the command line. You should see a bunch of test running and you are ready to go!

***Note:** you might get some failures when running the tests depending on the current version of the EM product you are running. This is fine, it shows the tool is running as it should and that you might have to make adjustments to fix those templates if you want to use them.*

## Install as a python module
If you are familiar with python another alternative is to install it as a python module:
- Install [python3](https://www.python.org/downloads/) and make sure you remember the path where is installed.
 - When running the installation make sure to select the checkbox to add python3 to your system path. For example, In windows the default python home installation path is: `%UserProfile%\AppData\Local\Programs\Python\Python37-32`
- Check the python installation folder was added to the the system path. If is not added you can added manually:
	 - In windows can add it by adding the following to your path variable: %PYTHON_HOME%;%PYTHON_HOME%/Scrips;
 - Copy the template folder to some location in your filesystem. For example under the current EM project.
- Add the following environment variables:
	- `PYTHON_HOME` is the python installation folder.
- Install [sqltask](https://test.pypi.org/project/sqltask/) by typing the following  command line:
```
python -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask
```
-  Unzip  "sqltask.zip" into your `project` folder.
-  Within the `config/core.properties` file:
	 -  Change the environment, container and machines names to point to your local environment.
	 - Change the `db.release.version`  property to point to your current AD release version. A

**Multiple versions of python **
 If you have multiple versions of python installed make sure you are installing it under version 3 by running instead:
```
python3 -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask
```

This applies as well when running upgrades and any python command it - e.g `python3 -m pip  install update sqltask`
# Template Design

How template values are prompted to the user is determined entirely by how the template is written. So having a set of well designed templates is the key for generating scripts rapidly.

The syntax is defined by python jinja templates. Check the [template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/).

## General guidelines
When design templates consider the following:
-  A value should be prompted with enough information so the user knows how to fill it.
- When possible provide a subset of values for the user to pick from.
- Users should NOT be prompted any value that can be computed from some other values - finding the minimum number of prompted values is key for a good template.
- Avoid duplicating SQL code, reuse template by including them within others. So when a product DB table changes it avoids having to change multiple templates.
- Review existing templates or consult this documentation to understand what filters and templates are available.

To design good templates is important to know what elements are available when writting templates. As follows it is documented the current filters and functions that can be used within templates.
You can check as well the existing templates for a good understanding on how these elements are applied.

## Filters
Jinja Templates use [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters),  which modify variables when rendering the template. For example `{{ name|default('NULL') }}`  will use `NULL` if the user doesn't enter any value.

`sqltask` uses filters to modify and enrich the template values that are prompted to the user.  For example  `{{ name|default('NULL') }}` displays message  like `name (default is NULL):`, rather than simply `name.`

 Jinja have many [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters) that can be used when rendering the template.
 In this documentation we describe only the filters implemented in `sqltask` which are the ones that change the way the value is prompted to the user. These filters are explained within the [list of builtin filters](#list-of-builtin-filters)

### Concatenate multiple filters
Filters can be concatenated:
```sql
#template
{{ my_variable| description('Enter any value')
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
**codepath**(_value_)

It autocompletes the repository paths from both product and project.
This is not a builtin jinja filter and it does not modify the variable entered by the user.

```sql
{{ object_path| codepath() }}

#prompts and when the user start typing it autocompletes
'object`: Customer.Objects.
```
**suggest**(_value_, suggestions)

It takes a list of suggestions which are prompted to the user when asking for the value.
```sql
{{ object_name| suggest(["Customer","Chat"]) }}
```
**split_uppercase**(_value_, )

This filter does not affect the prompted text. It modifies the variable splitting the words when it finds an upper case letter
It takes a list of suggestions which are prompted to the user when asking for the value.
```sql
{% verb_keyname = "customerInlineSearch" |split_uppercase() }}
# Sets verb keyname to "Customer Inline Search"

```
**objectname**(_path_)

It extract the object name from a logical object path
```sql
{% set logical_object_path = 'Customer.Implementation.Customer' %}
Object name is  {{ logical_object_path | objectname() }} == 'Customer'
```
**objectdir**(_path_)

It extract the object dir from a logical object path
```sql
{% set logical_object_path_2 = 'Customer.Implementation.Customer' %}
Object dir is  {{ logical_object_path_2 | objectdir() }} == 'Customer.Imlementation'
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
It returns a [SQLTable](#sqltable)  object (list of dictionaries). For example:
 - `_db.fetch.v_names_by_ed(entity_id)`


**find.<<query_name>>**(_\*query\_params_)
It returns a  [SQLRow](#sqlrow) object. It is similar to `fetch` but this is used when searching by a unique constraint field and it throws and exception if none or more than one record are found. For example
 - `_db.find.pd_by_ed_n_vname(entity_id, v_name)`


### _database
 Same as `_db` but allows running free form queries instead of dictionary queries:

**fetch**(_query_string_)
Similar to `_db.fetch` but it takes an SQL string instead. For example:
 `_database.fetch("SELECT NAME FROM VERB where name like '%create%'")`

 **find**(_query_string_)
 Similar to `_db.find` but it takes an SQL string instead. For example:
 `_database.find("SELECT * FROM VERB where name='my_verb'")`

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
### _emprj
 It extract different information from the current EM project:


## More Available Objects
### SQLTable
This object is not in context but is retrieved by `_db.find` or `db.fetch`. It is a list of dictionaries. As a list you access it with python list methods, for example:
   ```
   table =_db.fetch.v_names_by_ed(entity_id)`
   assert {"ID":1, "NAME":"search"} == table[0]
   ```
 It has the following method to allow extract data from the query result easily:

**column(name)**
Returns the column as a list:
   ```
   table =_db.fetch.v_names_by_ed(entity_id)`
   assert [1,2] == table.column("ID")
   ```

   **str()**
The string method has been override to use prettyTables:
   ```
   table =_db.fetch.v_names_by_context(context_id)`
   {% set context_verbs_desc = table | string %}
   {{ display_name | description(context_verbs_desc) }}

{# Displays #}
+------------------------+------------------------+
|      DISPLAY_NAME      |          VERB          |
+------------------------+------------------------+
|       Agent Chat       |   agentChatStart       |
|        Make Call       |     makeCall   		  |
|      Create Case       |    createCase  		  |
|      Get Call          |      getCall  	  	  |
|    Handle Whitemail    |    handleEmail         |
+------------------------+------------------------+
```

### SQLRow
`SQLTable` object is composed of a list of `SQLRow` objects. It is an extension of a dictionary so you can access it with regular python dictionary methods:
   ```
   row =_db.find.v_by_id(id)`
   assert 1 == row["ID"]
   ```
It has two methods overriden:

 **[_<<var_name>>_]**
 It retrieves `NULL` as a string if no value is found within the dictionary.

**str()**
As a list it is overriden to use prettytable which prints the keys and the values as the following:
```
+------------------------+---------------------+
|      NAME			     |         ID    	   |
+------------------------+---------------------+
|       Agent Chat     	 |   		1      	   |
+------------------------+---------------------+
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

## Organizing Templates
Templates can all be drop in one folder or they can be grouped and put into folders.
For example we could match a similar grouping to the EM admin screens:
```
/templates
	|__ manage_context
		|__ add_activity_to_perspective.sql
		|__ remove_activity_from_perspetive.sql
	|__ manage_entity_definitions
		|__ add_entity_definition.sql
		|__ extend_entity.sql
		|__ remove_entity_definition.sql
	|__ ...
```
## Hidden Templates
A hidden template is not display among the templates to be filled. They are created so they can be reused and included in other templates but they don't make much sense on their own.
Template can be hidden by adding the template under a folder called `hidden_templates` within the main template folder.


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
eyJoaXN0b3J5IjpbLTExNjg4MzAxMDgsMTgzNjUxNzIwNF19
-->
