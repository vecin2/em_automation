# Developer Installation and Execution
Remember to source pipenv to source all the python libs: . bin/activate
Source as well the local file "set_env_vars.sh" which is a work around to fix an issue importing modules.

The application be executing by running: python sql_gen.py
Test can run with pytest: pytest sql_gent/test

# User installation
https://test.pypi.org/project/sql-gen/

Download [git-bash](https://git-scm.com/download/win)
Downlaod [python3.7](https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe)
When running the installer make sure you check the box to add python to the system path.

Make sure the system variable "PATH" contains the folder where you install Python.
PYTHON_HOME should be set to the folder when python has been intalled.

Open the command line and run:
python3 -m pip install --index-url https://test.pypi.org/simple/ sql_gen 
Or use extra index url to look for the dependencies within the pypi real repository as well. Thas would allow download jinja2 as well.
python3 -m pip install --extra-index-url https://test.pypi.org/simple/ sql_gen 

Install Jinja2
We rely on a package Jinja2. If you are installing from the test repository that package will not be found there and youll have to install it with a different command:
python3 -m pip install Jinja2

If you have multiple versions of python install make sure you install the python3 Jinja2 version.
 

Environment variables
The following env variables need to be setup:
EM_CORE_HOME=/opt/em/projects/gsc #it should point to your project home
SQL_TEMPLATES_PATH=/opt/em/projects/gsc/sql_templates # it should point to the folder containing the sql templates

# em-dev-tools
 The main pacakge is sql_gen
 
 ## sql_gen
  Its a command line application that reads from a folder of sql_templates, and let the user select which one he like to fill. Then it prompts the user to enter the values and finally renders the template and write it to the given place in the fylesystem.
  Some of the values can be computed based on what the use enters, so to create a set of "filters" which will allow writting templates using in a way that minimizes the user action and it provides good feedback on how to fill the values.
 
For example a template like the following:


```sql
INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) 
VALUES 
(
 @PD.{{ process_descriptor_name }}, --ID
 @ENV.Dflt, --ENV_ID,
 '{{ process_descriptor_name }}', --process_descriptor_name
 '{{ repository_path }}', --repository_path 
 {{ config_id | default('NULL') }} , --config_id
 'N',
 {{ process_descriptor_type |
    description('type id (0=regular process, 2=action, 3=sla)') |
    default ('0')}} --type
);
```


It should prompt the user the following:
 repository_path:
 
 process_descriptor_name:
 
 config_id (default is NULL):
 
 type id (0=regular protype id (0=regular process, 2=action, 3=sla) (default is 0):
  
# Running application  

`em_sql # no parameters`

will print the output in the console

`em_sql -d modules/GSCCoreEntities/sqlScripts/oracle/updates/Project_R1_0_0/test_rewire_verb # will create that sql task including "update.sequence"`

-d indicates the directory where the sql task will be written to. The EM_CORE_HOME will be prefixed to this path

To specify the path in windows is a bit harder if there is no folder autocomplate. You c

# Template Design
By convention the all the SQL should be written in uppercase. 
Variables and lower case and in snake case (variable_names)


# Other Windows tools
When runnig it in windows to get autocomplete features and easier command line navigation it is recommenced to install one the following:
[Clink]( http://mridgers.github.io/clink/): gives you Bash-style autocompletion in Windows Cmd
[git-bash](https://gitforwindows.org/): its a different terminal which allows  bash-style autocompletion as well. 
[cygwin](https://www.cygwin.com/): a large collection of GNU and Open Source tools which provide functionality similar to a Linux distribution on Windows. 
  
