{#
Autosuggest entityName
List entity_names
#}
{entity_name}
#{%set result = adquery("SELECT * FROM EVA_ENTITY_DEFINITION WHERE NAME = '"+entity_name+"'")%}

{% if result | length == 1%}
name is: {{result[0]["NAME"]}}
{%else%}
cant compute name
{%endif%}
