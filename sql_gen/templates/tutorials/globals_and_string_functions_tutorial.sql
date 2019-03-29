
**Globals**
Globals are functions which can be invoked within the template expressions

*camelcase*
{% set relative_id = camelcase(display_name) %}
The 'camelcase' relative_id is {{relative_id}}


**Python String Functions**
Python string functions can be applied to variables

*capitalize*
{% set full_name = first_name.capitalize() + " " +last_name.capitalize() -%}
Hi {{full_name}}!
