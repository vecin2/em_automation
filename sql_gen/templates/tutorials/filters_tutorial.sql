*** FILTERS ***
Filters allow to change the way the value is prompt to the user. 

By default only variables which are not set will be prompt using the variable name.

**Simple prompt**
This prompts for 'name'
{{name}}

**Default Filter**
This prompts 'surname (default is Smith)'
{{surname | default('Smith') }}

**Default Description**
This prompts 'Please enter the address'
{{address | description('Please enter the address') }}

**Default Filer piped with Description **
This prompts 'Please enter the address'
{{address | description('Please enter the address') }}
