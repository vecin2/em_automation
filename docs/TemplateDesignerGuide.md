[templates]: https://github.com/vecin2/sqltask-templates/blob/master/docs/LibraryByFolder.md
[tutorials]: https://github.com/vecin2/sqltask-templates/blob/master/docs/LibraryByFolder.md#tutorials
# Template Design

How template values are prompted to the user is determined entirely by how the template is written.  

Templates should be designed in a way that provide enough information to users when filling the values, minimizing user prompts and, avoiding asking for values that could be computed from values already entered.

The syntax is defined by python jinja templates. Check the [jinja template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/).

## Table Of Content
  * [General guidelines](#general-guidelines)
  * [Tutorials](#tutorials)
  * [Filters](#filters)
    + [Concatenate multiple filters](#concatenate-multiple-filters)
    + [List of Builtin filters](#list-of-builtin-filters)
  * [Objects in context](#objects-in-context)
    + [\_keynames](#--keynames)
    + [\_db](#--db)
    + [\_database](#--database)
  * [More Available Objects](#more-available-objects)
    + [SQLTable](#sqltable)
    + [SQLRow](#sqlrow)
  * [Global Functions](#global-functions)
    + [List of Builtin Global Functions](#list-of-builtin-global-functions)
  * [String Python Builtin Functions](#string-python-builtin-functions)
  * [Include](#include)
  * [Organizing Templates](#organizing-templates)
  * [Hidden Templates](#hidden-templates)
  * [Naming Convention](#naming-convention)
  * [Formatting](#formatting)
      - [Inserts](#inserts)

- [Build Extensions](#build-extensions)
    + [Create Windows Executables](#create-windows-executables)
      - [Troubleshooting](#troubleshooting)
    + [Developer Setup](#developer-setup)
      - [Windows](#windows)
      - [Running tests](#running-tests)
    + [Imlementing new Global functions](#imlementing-new-global-functions)
    + [Implementing new Filters](#implementing-new-filters)



## General guidelines

When designing templates consider the following:

- A value should be prompted with enough information to avoid the user from making further DB queries.
- When possible, prompts should have a list of suggestions.
- Users should NOT be prompted with any value that could be computed from values already entered. Reducing the number of prompted values to the minimum is key for a well designed template.
- Avoid duplicating SQL code. Instead, use [include](#include) template so when a product DB table changes, avoids having to change multiple templates.
- Follow the existing [templates] design and check the [tutorials](#tutorials) to understand what filters and objects are available.


## Tutorials

Within the templates there is a set of [tutorials] templates. They provide good guide and practical examples on how templates can be created. 

Making changes to the existing tutorial templates and see how it impacts the prompting is a great way to learn the syntax.


## Filters

Jinja Templates use [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters) to modify variables when rendering the template. For example `hello {{ name | default('Daniel') }}` renders to `hello Daniel` when no value is entered for `name`.

In addition to this, `sqltask` uses filters to modify how template values are prompted to the user. For example `{{ name | default('Daniel') }}`,  displays  `name (default is Daniel):` when prompting to enter a value for `name` .

Jinja have many [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters) that can be used when rendering the template.
In this documentation we describe only the filters implemented in `sqltask` which are the ones that modify the way the value is prompted to the user. These filters are explained within the [list of builtin filters](#list-of-builtin-filters)

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

In this section we only detail how the filters affecting value prompts. Here is the full [list of builtin jinja filters](http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters).

**default**(_value_, _default_value=u''_, _boolean=False_)

It appends `default_value` to the variable name when prompting:
If the user does not enter a value the default value is used when rendering the template.
```sql
#template
{{ my_variable| default('my_variable is not defined') }}

#prompts
my_variable (default is 'my variable is not defined'):

```

**description**(_value_, _description_)

It shows the `description` when prompting the user.
This is not a builtin jinja filter and it does not modify the variable entered by the user.

```sql
{{ my_variable| description("Please enter 'my_variable_value`') }}

#prompts
Please enter 'my_variable_value`:
```
**print**(_value_, _text_)
It shows the `text` in a line above the value prompt. 
This is not a builtin jinja filter and it does not modify the variable entered by the user.

```sql
{{ entity_name| print("Entity names will normally finish with 'ED'") }}

#prompts
Entity names will normally finish with 'ED'
'entity_name`:
```
If an object is passed it calls the `str` method on it, so it could take [SQLTable](#sqltable) or [SQLRow](#sqlrow) and it will display the data using pretty printing. An example of this can be found in 


**codepath**(_value_)

It autocompletes the repository paths from both product and project.
This is not a builtin jinja filter and it does not modify the variable entered by the user.

```sql
{{ object_path| codepath() }}

#prompts and when the user start typing it autocompletes
'object`: Customer.Objects.
```

**suggest**(_value_, suggestions)

It takes a list of suggestions which are displayed to the user when this value is prompted.

```sql
{{ object_name| suggest(["Customer","Chat"]) }}
```

**split_uppercase**(_value_, )

This filter does not affect the prompted text. It modifies the variable splitting the words when it finds an upper case letter


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

The objects are put into context with underscore (\_) prefix this is to avoid clashing with template variables names.

### \_keynames

It retrieves a list of relative ids for the key set passed. For example:

- \_keynames.ED: retrieves a list of the entity defintions relative ids
- \_keynames.V: retrieves a list of the verbs relative ids

### \_db

It allows to run queries from the agent desktop queries file `<<sqltask.library.path>>/config/ad_queries.sql`:


**fetch.<<query_name>>**(_\*query_params_)
It returns a [SQLTable](#sqltable) object (list of dictionaries). For example:

- `_db.fetch.v_names_by_ed(entity_id)`

**find.<<query_name>>**(_\*query_params_)
It returns a [SQLRow](#sqlrow) object. It is similar to `fetch` but this is used when searching by a unique constraint field and it throws and exception if none or more than one record are found. For example

- `_db.find.pd_by_ed_n_vname(entity_id, v_name)`

### \_tps

It allows to run queries from the `tps` queries file `<<sqltask.library.path>>/config/tps_queries.sql`


### \_database

Same as `_db` but allows running raw SQL instead of dictionary queries:

**fetch**(_query_string_)
Similar to `_db.fetch` but it takes an SQL string instead. For example:
`_database.fetch("SELECT NAME FROM VERB where name like '%create%'")`

**find**(_query_string_)
Similar to `_db.find` but it takes an SQL string instead. For example:
`_database.find("SELECT * FROM VERB where name='my_verb'")`

### \_tpsdatabase

Same as `_tps` but allows running raw SQL instead of dictionary queries.

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
It is implemented using python library `prettyTable` :

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

[SQLTable](#sqltable) object is composed of a list of `SQLRow` objects. It is an extension of a dictionary so you can access it with regular python dictionary methods:

```
row =_db.find.v_by_id(id)`
assert 1 == row["ID"]
```

It has two methods overridden:

**[_<<var_name>>_]**
It retrieves `NULL` as a string if no value is found within the dictionary.

**str()**
It is implemented using python library `prettyTable`. For example one row is printed as following:
```
+------------------------+---------------------+
|      NAME			     |         ID    	   |
+------------------------+---------------------+
|       Agent Chat     	 |   		1      	   |
+------------------------+---------------------+
```

## Global Functions

There is a set of builtin global functions which can be used when writting templates. Functions can be invoke within blocks `{% %}` or within statements `{{ }}`.

### List of Builtin Global Functions

To the existing [list of jinja builtin global functions](http://jinja.pocoo.org/docs/2.10/templates/#builtin-globals) we have added the following:

**camelcase**(_value_)
It returns the _value_ passed in camelcase:

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

Include allows wrapping other templates so they can be reused and avoid SQL code duplication. 
Typically, we would set some variables contained within the included template before call that template so it doesn't prompt them:

```sql
#Compute descriptor id  which is used in 'add_process_descriptor.sql'
{% set process_id = __prjprefix + entity_id.capitalize() + verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}
{% set descriptor_ref_id = descriptor_id %}
{% include 'add_process_descriptor_ref.sql' %}
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
Adding a template under a folder  `templates/hidden_templates` will not show the template when the application asks to select a template.

These templates can be included within other templates but they don't make much sense on their own.


## Naming Convention

The following name and convention is used when writing templates:

- Template variables names follow snake case e.g "customer_name"
- Context config variables, which are defined under `config/context_values.yaml` start with an underscore to distinguish them from template variables, e.g `_keynames, _db`
- Displayed Template variables  do not start with `_` :
```sql
{{ entity_display_name | default(default_display_name) }} --ENTITY_NAME
```
- Inner Template variables are named as the displayed variable but prefixed with two underscores. Inner variables are used when we capturing a value that will be used later on within the same template.

```
{% set __entity_display_name = entity_display_name
								   | default(default_display_name)%}
```

## Formatting

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



