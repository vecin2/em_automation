# Installation and Execution
Remember to source pipenv to source all the python libs: . bin/activate
Source as well the local file "set_env_vars.sh" which is a work around to fix an issue importing modules.

The application be executing by running: python sql_gen.py
Test can run with pytest: pytest sql_gent/test



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
  
  
 
  
