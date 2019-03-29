Main elements within a template  are:
{% raw %}

{% ... %} for Statements
{{ ... }} for Expressions to print to the template output
{% endraw %}

*Simple variable prompt*

Variables are placed within statements or expressions and when the application runs they are prompted if they dont have a value.

Example 1:
	Hi {{ name }}; #prompts 'name'

*Variable used in multiple places*

When the variable is used in more than one placed, the variable is only prompt once, which corresponds to the first ocurrence within the template. If you want to apply a filter, make sure it is apply to the first occurence.

Example 1:
	Hi {{ surname | default("Smith") }} and welcome back Mrs {{ surname}}

*Variable assignment*
We can assign values to variables and them use them in a filter without having to print the variable

Example 1 - Simple Assignment:
	{% set default_address = "212 78st St" %}
	We send a letter to {{ address | default(default_address) }}

Example 2 - Assignment with filter:
We need to use an extra variable so we can apply the filter to that variable. The variable to the right hand side of the '=' will be displayed.
	{% set display_name_ = display_name | default("unknown") %}
	{{display_name_}} can now be used in multiple places in this scriptwhich show {{ display_name_ }} or in included templates.

Example 3 - Assignment with filter:
Other option when applying a filter is to use a 'tmp_variable' piped with a description filter so the prompt is user friendly:
	{% set displayed_name  = tmp_dsp_name |
					description ("displayed_name") |
					default("unknown") %}
	{{displayed_name}} can now be used in multiple places in this scriptwhich show {{ displayed_name }} or in included templates.
