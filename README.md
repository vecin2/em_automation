
# sqltask - an sql generator for EM projects

sqktask is command line application which allows users to easily generate SQL scripts commonly needed within EM developement. 

It uses a set of SQL script templates and it prompts the user for the template values. Then it renders the template and creates the corresponding SQSL task under the current project -defined by `EM_CORE_HOME` path. A SQL task contains a `tableData.sql` and `update.sequence` files.
 
 SQL templates are meant to evolve overtime and to provide and to server as a model when creating sql tasks.

# Table Of Contents

## Basic Usage
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

#### Redirect output to SQLTask
Running sqltask with the parameter directory pass will generate and SQL task under the current `EM_CORE_HOME`:

`sql task -d modules/ABCustomer/sqlScripts/oracle/updates/Project_R1_0_0/add_policy_to_Customer_table`

#### Run help:
Running `sqltask -h`  produces help text on how run the command
```optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Its the directory where the sql task will be written to.
                     Its a relative path from $EM_CORE_HOME to, e.g.
                     modules/GSCCoreEntites...
```
#### Exiting the application
At any point press `Ctrl+c` or `Ctrl+d` to exit - if you are using Gitbash you might have to press `Enter` as well.

## User installation

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

### Windows Console
Windows console its vary basic and it doesn't provide many feature as easy path autocompletion, easy copy and paste, etc. You can  look at installing one the following:
- [Clink]( http://mridgers.github.io/clink/): very light weight tool which add a set features yo you Windows console.
- [git-bash](https://gitforwindows.org/): its a different terminal which allows  bash-style autocompletion as well and several linux commands. 
- [cygwin](https://www.cygwin.com/): a large collection of GNU and Open - Source tools which provide functionality similar to a Linux distribution on Windows. 
  
# Developer Setup
Create a branch for the [master branch](https://bfs-eng-can05.kana-test.com/dgarcia/em_automation)

Consider create a virtual pyhon  envioronment for this project.   As well, it is recomended to user [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to  manage your virtual environment. 

Make user the sql_gen folder is added to you `PYTHONPATH`:
`export PYTHONPATH=${PYTHONPATH}:/home/dgarcia/dev/python/em_automation/sql_gen`

If you are using virtual environment you can set the `PYTHONPATH` within the `$vitualevns/bin/postactivate` so it only runs when you activate this environment.

The application can be executing by running: `python .` from project top folder.

#### Running tests
Test can run with pytest: py.test from the project top folder


## Adding SQL Templates
New templates can be added by creating a file under `$SQL_TEMPLATES_PATH` and create a shortcut with the same name pointing to that file under `$SQL_TEMPLATES_PATH/menu`
Its important that the shorcut name matches the template name otherwise it will not show up in the menu when running sqltask. 

#### Adding hidden templates
Some templates might not be wanted to display within the menu. For example some scenarios will create a template which include other templates and the included template do not want to be shown. This can be achieve by simply not creating the shorcut. 


## Template Design
Template are  Standarize sql scripts including formatting a redability
As new filters are available they can be incorporate to existing templates. It is expected this is an iteractive process whith the goal of providing a better user experience when populating template values.

### Filters

DefaultFilter
DescriptionFilter

#### Adding new Filters
Filters are picked up automatically when they created under `filters` folder. 

# Global functions
camelcase(string), it will came case the string passed. A variable can be passed in that case if the variable has not been defined yet it should prompt to enter the value.
# Adding Functions
New functions can easily added to templates. 




###  Fomatting and Naming Convention 
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




