**Include**
Include allows wrapping other templates so they can be reused and avoid SQL code duplication.

{%raw %}
# Assuming that full_name_greeting.sql template is  'Hello {{full_name}}'
# It will replace the variable 'full_name' within the included template
{% set full_name = first_name.capitalize() + last_name.capitalize() -%}
{% include 'full_name_greeting.sql' %}

SET VARIABLES BEFORE CALL A TEMPLATE
When including a template is important to understand what variables need to be populated.
For example we have a template like this:
       {% set __house_no = house_no | description("house_number") %}
	The house number is {{house_no}}
When this template runs will prompt "house_number", but that is NOT the variable name. The variable no is "house_no".
So if we want to call that template with specific house number we will do the following:
{% set house_no ='123' %}
{% include 'house_no.sql' %}
Otherwise it will still prompts use for 'house_no' when the template is included
{% endraw %}
