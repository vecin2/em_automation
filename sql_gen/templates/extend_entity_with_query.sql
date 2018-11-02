
{% macro select_from(entity_def_id,list) %}
Hello {{ list }}!
{% endmacro %}
{% set entity_ids = [1,2]%}
{{ select_from("entity_def_id",entity_ids) }}
