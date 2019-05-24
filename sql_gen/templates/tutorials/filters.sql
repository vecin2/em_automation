*** FILTERS ***
Filters allow both, changing the way the value is prompted to the user and changing how the values is rendered.
Jinja takes care of rendering the value while the prompting part is what sqltask does.
Jinja provides a long list of builtin filters, here we are only describing the filters created specifically for sqltask.
For more information about other jinja filters check the Jinja Design Documentation.

By default only variables which are not set will be prompt using the variable name.

**Default Filter**
This prompts 'surname (default is Smith)'
{{surname | default('Smith') }}

**Description Filter**
This prompts 'Please enter the address'
{{address | description('Please enter the address') }}

**Print Filter**
Print filter is similar to description but is used to print longer text. For example tables or information for the user. Description filter shouldn't be used with long strings as it doesnt support well long lines.
This prompts 'Please enter the address'
{{current_address | print('The customer address where he has lived during the last year. Leave blank if he has not remain in the same address for that long') }}

**Default Filter | Description Filter**
Filters can be piped. Examples:
This prompts 'Please enter the country' and default to "US"
{{country | description('Please enter the country') | default("US") }}

**Codepath Filter**
Codepath filter suggest repository paths. Examples:
{{ package_name | codepath() }}

**Suggest Filter**
Suggest filter prompt to enter the value showing a list of options. To select an option user start typing and it does a fuzzy find.
{{ customer_type | suggest(['Regular', 'Premium'])}}

{% set residence_type_list = ['House (small)','House (big)','Apartment','Condo'] %}
{{ residence_type | suggest(residence_type_list)}}

**split_uppercase(string)**
It useful to turn and id or name into a diplayed name and then suggest it as default
{% set default_display_name =verb_name |  description ("Please enter a verbname, e.g inlineSearch") | split_uppercase()%}
{{  display_name |  default(default_display_name)}}

**objectname(path)**
It extract the object name from a logical object path
{% set logical_object_path = 'Customer.Implementation.Customer' %}
Object name is  {{ logical_object_path | objectname() }} == 'Customer'

**objectdir(path)**
It extract the object dir from a logical object path
{% set logical_object_path_2 = 'Customer.Implementation.Customer' %}
Object dir is  {{ logical_object_path_2 | objectdir() }} == 'Customer.Imlementation'

** Variables within Filters **
Variables can be used within filters and they are resolved
{% set office_no_desc = 'Please enter the Office Number'%}
The office {{ office_no | description(office_no_desc)}} is located at the end of the street.

** Keynames **
Keynames are supported within filters. The following will suggest the list of ED keynames:
{{ verb | suggest(_keynames.ED) }}

** Function within Filters **
Functions are currently NOT supported within filters!!!! 
Only variables and keynames are supported
The following will NOT work:
{% raw %}
The office {{ office_name | description(camelcase("my office"))}} is located at the end of the street.
{% endraw %}
You will have to assign that to a variable first:
{% set desc_office_name = camelcase("my office") %}
The office '{{ office_name | description(desc_office_name)}}' is located at the end of the street.
