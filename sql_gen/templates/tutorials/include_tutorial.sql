**Include**
Include allows wrapping other templates so they can be reused and avoid SQL code duplication.

{%raw %}
#Compute descriptor id  which is used in 'add_process_descriptor.sql'##
{% set full_name = first_name.capitalize() + last_name.capitalize() -%}

# Assuming that this template is  'Hello {{full_name}}'
# It will replace the variable 'full_name' within the included template
{% include 'full_name_greeting.sql' %}
	

{% endraw %}
