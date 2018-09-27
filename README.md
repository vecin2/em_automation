
# sqltask - an sql generator for EM projects

sqktask is command line application which allows users to easily generate SQL scripts commonly needed within EM developement. 

It uses a set of SQL script templates and it prompts the user for the template values. Then it renders the template and creates the corresponding SQSL task under the current project -defined by `EM_CORE_HOME` path. A SQL task contains a `tableData.sql` and `update.sequence` files.
 
 SQL templates are meant to evolve overtime and to provide and to server as a model when creating sql tasks.

# Table Of Contents

- [Basic Usage](#basic-usage)
    + [Exiting the application](#exiting-the-application)
    + [Redirect output to SQLTask](#redirect-output-to-sqltask)
    + [Show help](#show-help)
    + [Inserting New SQL Templates](#inserting-new-sql-templates)
      - [Adding hidden templates](#adding-hidden-templates)
 - [User installation](#user-installation)
    + [Environment variables](#environment-variables)
    + [Windows Console](#windows-console)
- [Template Design](#template-design)
    + [Filters](#filters)
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
    + [Implementing new Filters Filters](#implementing-new-filters-filters)



      
# Basic Usage
This section gives you a run through creating a sql template and running it:
- Create a simple SQL template `change_verb_context.sql` under your `SQL_TEMPLATES_PATH`:
```sql
UPDATE EVA_CONTEXT_VERB_ENTRY
SET (CONFIG_ID)= (@CC.{{new_config_id | description("new_config_id (e.g. Home, CustomerPostIdentify, ...)")}})
where CONFIG_ID = @CC.{{old_config_id} | default(}
and VERB = '{{verb_name}} ';
```
- Create a shorcut with the same name under `SQL_TEMPLATES_PATH/menu/`:
- Run the application by simply typing `sqltask` in the comand line. Your template should be display as one of the options.
-  Select you template and the system will prompt to enter:
```bash
	new_config_id (e.g. Home, CustomerPostIdentify, ...): Customer
	old_config_id: Home
	verb_name: identifyCustomer
```
- The system will print in the screen the following SQL:
```sql
	UPDATE EVA_CONTEXT_VERB_ENTRY
	SET (CONFIG_ID)= (@CC.Customer)
	where CONFIG_ID = @CC.Home
	and VERB = 'identifyCustomer';
```

### Exiting the application
At any point press `Ctrl+c` or `Ctrl+d` to exit - if you are using Gitbash you might have to press `Enter` as well.

### Redirect output to SQLTask
Running sqltask with the parameter directory pass will generate and SQL task under the current `EM_CORE_HOME`:

`sql task -d modules/ABCustomer/sqlScripts/oracle/updates/Project_R1_0_0/add_policy_to_Customer_table`

### Show help
Running `sqltask -h`  produces help text on how run the command
```
optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Its the directory where the sql task will be written to.
                     Its a relative path from $EM_CORE_HOME to, e.g.
                     modules/GSCCoreEntites...
```
### Inserting New SQL Templates 
New templates can be added by creating a template file under `$SQL_TEMPLATES_PATH` and create a shortcut with the same name pointing to that file under `$SQL_TEMPLATES_PATH/menu`
Its important that the shorcut name matches the template name otherwise it will not show up in the menu when running sqltask. 

#### Adding hidden templates
Some templates shouldn't be listed as option for the user. For example some scenarios will create a template which include other templates and the included template do not want to be shown. This can be achieve by simply not creating the shorcut. 

# User installation

Install [python3](https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe). 

Add Python installation folder to you system path and make sure the env variable `PYTHON_HOME` is set to the  installation folder.

If you have multiple versions of python installed make sure you are using verion 3. 

Install [sqltask](https://test.pypi.org/project/sqltask/) by typing the command line:
```python3 -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask```

The command above intalls all the require packages including [jinja2 templates](http://jinja.pocoo.org/).  If you get issues when running sqltask where it can find this package you can install manually by running 
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
This is based in jinja templates so please refer to the jinja [Template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/).

What is additional to our project is that templates are parsed to build a set of questions for the user which will capture all the template values building in this way the context which will them be used to render the template.

The application will use the variable if it has been defined otherwise will prompt the user to enter the value.

In this section is detailed how the different template elements affect the question that are prompt to the user. 

### Filters
Jinja Template can contain [filters](http://jinja.pocoo.org/docs/2.10/templates/#filters),  which can modify variables when rendering the template. For example `{{ name|default('NULL') }}`  will use `NULL` when rendering this template  if the user doesnt enter any value.

The issue is that users should be notified that a filter or a set of filters will apply to the value they are entered. For this reason we created our own Filters which can wrap the jinja Filters but also modify the text that is prompt to the user.

In this scenario will prompt `name (default is NULL):` 

### Concatenate multiple filters
Filters can be concatenated:
```sql
#template
{{ my_variable| description('Enter any value' 
              | default('my_variable is not defined')}} 

#prompts
Enter any value (default  is  'my variable is not defined'):

## Notice that description filter will override any other filter
## so if the order of the pipe changes description will override ## everything that was apply before.
```

The list of [builtin filters](#List_of_Builtin_filters) describes all the builtin filters.

### List of Builtin filters
In this section we only detail how the filters will affect the text that is prompt to the user and not how the modify the variable when rendering the template. For details on this check the [list of builtin jinja filters](http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters).

**default**(_value_,  _default_value=u''_,  _boolean=False_)
It appends the `default_value` to the variable name when prompting:
```sql
#template
{{ my_variable| default('my_variable is not defined') }}
#prompts
my_variable (default is 'my variable is not defined'):

```
**description**(_value_,  _description_)
It shows the `description` when prompting the user. 

This is not a jinja filter and it does not modify the variable enter by the user. It only provides additional information when prompting the user:

```sql
{{ my_variable| description('This can be anything, it is just a example') }}
#prompts
This can be anything, it is just a example:
```

## Globals Functions
There is a set of builtin global functions which can be use when writting templates.  Function can only be invoke within blocks `{% %}` or within statements `{{ }}`.

## List of Global Functions
To list of [jinja builtin global functions](http://jinja.pocoo.org/docs/2.10/templates/#builtin-globals) we have added the following:
**camelcase**(_value_)
It  returns the _value_ passed in camelcase:
` camelcase("Change the address") # returns changeTheAddress `
```sql
#Template
{% set display_name = "Change the address" %}
{% set name = camelcase(display_name) # returns changeTheAddress %}
Name is  {{name}}
Name is {{ camelcase(display_name }}

#Renders to
Name is changeTheAddress
Name is changeTheAddress

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

#A Template
 {% set process_desc_id = prj_prefix()+ entity_def_name %}
Process descriptor id is {{process_desc_id }}

#It renders to
Process descriptor id is ABC
Name is changeTheAddress
```
## String Python Builtin Functions
Python string functions can be used as well within templates:

**capitalize**()
It returns the current string capitalize. 
```sql
#A Template
{% entirty_def_id = customer %}
{% set process_desc_id = entity_def_id.capitalize %}
Process descriptor id is {{process_desc_id }}

#Renders to 
Process descriptor id is Customer
```

##  Fomatting and Naming Convention 
All SQL scripts are written in uppercase with the variables in lower case and snake case. 

#### Inserts
For easy reading the values inserted are indented within the brackets and a comment with fiel naem is added next to each value.
```sql
INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) 
VALUES (
        @PDR.{{process_descriptor_ref_id}} --process_descriptor_ref_name,
        @PD.{{process_descriptor_id}}, --process_descriptor_id
		@ENV.Dflt, --env_id
		NULL, --config_id
       	'N' --is_shared
       );
```

# Build Extensions
### Developer Setup
Create a branch for the [master branch](https://bfs-eng-can05.kana-test.com/dgarcia/em_automation)

Consider create a virtual pyhon  envioronment for this project.   As well, it is recomended to user [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to  manage your virtual environment. 

Make user the sql_gen folder is added to you `PYTHONPATH`:
`export PYTHONPATH=${PYTHONPATH}:/home/dgarcia/dev/python/em_automation/sql_gen`

If you are using virtual environment you can set the `PYTHONPATH` within the `$vitualevns/bin/postactivate` so it only runs when you activate this environment.

The application can be executing by running: `python .` from project top folder.

#### Running tests
Test can run with pytest: py.test from the project top folder



Permalink to this definition
DescriptionFilter


### Imlementing new Global functions
Globals functions can easily implemented by adding the function to the `globals.py` module and then adding the function to the environment when the environment is created:
 `self.env.globals['camelcase'] = camelcase `

 ### Implementing new Filters Filters
 Filters are picked up by the environment by name and convention. It looks for classes under the `/filters` whith the class name matching the capitalize name of the filter +"Filter". For example:
 ```sql
 #With a template
 {{ var_name | default("Test default") }}

#Searches for class named "DefaultFilter" under the folder /filters
 ```
### Imlementing new Filters
There are two main two of filters:
- Filters that wrap existing builtin jinja filters
- Completely new filters

In the first case filters do not need to be added to the environment so implementing `apply` should be enough:
_class_ sql_gen.filters.**DefaultFilter**()
		string :: **apply**(prompt_text)
It takes the prompt text and it changes accordingly to what it should be display to the user. Multiple filters can be concatenated.

When creating new filter we need to implement  not only `apply` but  `get_template_filter` which is invoke by the application to add the filter to the environment.

_class_ sql_gen.filters.**DescriptionFilter**()
		func :: **get_template_filter**()
It return the function which implements the filter that will be use to modify the variable when rendering the template.








