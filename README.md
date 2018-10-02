# sqltask - an sql generator for EM projects

sqktask is command line application which helps users generating SQL scripts commonly needed within EM developement. 
It works from a set of SQL templates, prompting users with the neccesary values to render the template. 
Templates are written using [jinja templates syntax](http://jinja.pocoo.org/)  and they should be designed to provide good information to users when entering values and to minimize user interactions. So if a value can computed, it should not be prompted.


 

# Table Of Contents

- [sqltask - an sql generator for EM projects](#sqltask---an-sql-generator-for-em-projects)
- [Basic Usage](#basic-usage)
    + [Redirect output to SQLTask](#redirect-output-to-sqltask)
    + [Exiting the application](#exiting-the-application)
    + [Show help](#show-help)
    + [Adding New Templates](#adding-new-templates)
      - [Hidden templates](#hidden-templates)
- [User installation](#user-installation)
    + [Environment variables](#environment-variables)
    + [Initial Set of Templates](#initial-set-of-templates)
    + [Windows Console](#windows-console)
- [Template Design](#template-design)
  * [Filters](#filters)
    + [Concatenate multiple filters](#concatenate-multiple-filters)
    + [List of Builtin filters](#list-of-builtin-filters)
  * [Globals Functions](#globals-functions)
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
This section runs through a basic use case:

- [Add a new template](#adding-new-templates) called `change_verb_context2.sql`:
```sql
UPDATE EVA_CONTEXT_VERB_ENTRY
SET (CONFIG_ID)= (@CC.{{new_config_id | description("new_config_id (e.g. Home, CustomerPostIdentify, ...)")}})
where CONFIG_ID = @CC.{{old_config_id} | default("NULL")}
and VERB = '{{verb_name}} ';
```
- Create a shorcut with the same name under `SQL_TEMPLATES_PATH/menu/`:
- Run the application by simply typing `sqltask` in the comand line. The new template should show as one of the options.
-  Select the template. The application will prompt the following three values:
```bash
	new_config_id (e.g. Home, CustomerPostIdentify, ...): 
	old_config_id: 
	verb_name: 
```
- Assuming the user enters `Customer`, `Home` and `indentifyCustomer`, the following will be print out:
```sql
	UPDATE EVA_CONTEXT_VERB_ENTRY
	SET (CONFIG_ID)= (@CC.Customer)
	where CONFIG_ID = @CC.Home
	and VERB = 'identifyCustomer';
```
### Redirect output to SQLTask
``` 
sqltask -d modules/ABCustomer/sqlScripts/oracle/updates/Project_R1_0_0/add_policy_to_Customer_table
```
It generates and SQL task under the current `EM_CORE_HOME`, which include both files `tableData.sql` and `update.sequence`.

### Exiting the application
At any point press `Ctrl+c` or `Ctrl+d` to exit. 
Note that if you are using Gitbash you might have to press `Enter` after  `Ctrl+c` or `Ctl+d`.

### Show help
Running `sqltask -h`  produces help text on how run the command
```
optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Its the directory where the sql task will be
                     written to.
                     Its a relative path from $EM_CORE_HOME to, e.g.
                     modules/GSCCoreEntites...
```
### Adding New Templates 
To create a new template:
- Create a file with `.sql` extension (only sql files are read) under `$SQL_TEMPLATES_PATH`
- Create a shortcut with the same name pointing to the previous file under `$SQL_TEMPLATES_PATH/menu`. Make sure the shorcut name matches the template name otherwise it will not show up in the menu when running the application. 

#### Hidden templates
Some templates might not want to be show as option to the user, however they are still needed. For example a template A be included within templates B and C, where B and C are shown to the user but A is not really a use case and therefore it  shouldn't be shown.

This can be achieved by simply not creating the shorcut. 

# User installation

Install [python3](https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe). 

Add Python installation folder to the system path
Make sure the environment variable `PYTHON_HOME` is set to the  installation folder.
If you have multiple versions of python installed make sure you are using verion 3. 

Install [sqltask](https://test.pypi.org/project/sqltask/) by typing the command line:
```python3 -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask```

The command above installs all the require packages including [jinja2 templates](http://jinja.pocoo.org/).  If you get issues when running sqltask where it can find this package you can install manually by running 
`python3 -m pip install Jinja2`.

 
### Environment variables
The following env variables need to be setup:
- `EM_CORE_HOME`it should point to your project, e.g. `/opt/em/projects/gsc` 
- `SQL_TEMPLATES_PATH` it should point to the folder containing the sql templates, e.g. `/opt/em/projects/gsc/sql_templates `

### Initial Set of Templates
You can copy the templates folder within this project under you em project folder which will provide with the initial set of templates.

### Windows Console
Windows console its vary basic and it doesn't provide many feature as easy path autocompletion, easy copy and paste, etc. You can  look at installing one the following:
- [Clink]( http://mridgers.github.io/clink/): very light weight tool which add a set features yo you Windows console.
- [git-bash](https://gitforwindows.org/): its a different terminal which allows  bash-style autocompletion as well and several linux commands. 
- [cygwin](https://www.cygwin.com/): a large collection of GNU and Open - Source tools which provide functionality similar to a Linux distribution on Windows. 
 

# Template Design

How template values are prompted to the user is determined entirely by how the template is written. So having a set of well design template is the key for the application to work well.

The syntax is defined by python jinja templates. Check their [template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/).

When design templates consider:
-  A value shouuld be prompted with enough information so the user knows how to populate it.
- When possible provide a subset of values for the user to pick from.
- Users should NOT be prompted a value if the value can be computed from some other value.
- Templates should be reused so if one DB table changes then it it is easy to update the templates to reflect that.
- Review existing templates or consult this documentation to undestand what filters and templates are available.

To design good templates is important to know what elements are available when writting templates. As follows it is documented the current filters and functions that can be used within templates. 
You can check as well the existing templates for a goo understanding on how these elements are applied.

## Filters
Jinja Templates use [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters),  which can modify variables when rendering the template. For example `{{ name|default('NULL') }}`  will use `NULL` if the user doesn't enter any value.

The issue is that in some cases the application should notify users that a filter or a set of piped filters is apply to that value otherwise the user will not benefit from it.  For example  `{{ name|default('NULL') }}` should show a display message  like `name (default is NULL):`, rather than simply `name:`
 
Not all the jinja filters have an equivalent filter that modifies the displays text, to understand which ones are available check the [list of builtin filters](#list-of-builtin-filters) 

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

## Globals Functions
There is a set of builtin global functions which can be used when writting templates.  Functions can be invoke within blocks `{% %}` or within statements `{{ }}`.

## List of Global Functions
To the existin [list of jinja builtin global functions](http://jinja.pocoo.org/docs/2.10/templates/#builtin-globals) we have added the following:

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
Globals functions can easily implemented by adding the function to the `globals.py` module and then adding the function to the environment when the environment is created:
 `self.env.globals['camelcase'] = camelcase `

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









