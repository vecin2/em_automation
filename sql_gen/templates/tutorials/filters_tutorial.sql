*** FILTERS ***
Filters allow to change the way the value is prompt to the user. 

By default only variables which are not set will be prompt using the variable name.

**Simple prompt**
This prompts for 'name'
{{name}}

**Default Filter**
This prompts 'surname (default is Smith)'
{{surname | default('Smith') }}

**Description Filter**
This prompts 'Please enter the address'
{{address | description('Please enter the address') }}

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

** Variables within Filters **
Variables can be used within filters and they are resolved
{% set office_no_desc = 'Please enter the Office Number'%}
The office {{ office_no | description(office_no_desc)}} is located at the end of the street.

** Function within Filters **
Functions are NOT supported within filters!!!! 

The following will NOT work:
{% raw %}
The office {{ office_number | description(camelcase(number_desc))}} is located at the end of the street.
{% endraw %}
