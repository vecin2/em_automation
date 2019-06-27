{% set __entity_keyname= entity_keyname | suggest(_keynames.ED) %}
{% set __field_name = field_name  %}
{% set keyname =__entity_keyname+__field_name[0].upper()+__field_name[1:]%}
{% set query ="SELECT FIELD_SEQUENCE FROM EVA_DYNAMIC_ENTITY_FIELD WHERE ENTITY_DEF_ID = @ED.{} ORDER BY FIELD_SEQUENCE DESC".format(__entity_keyname) %}
{% set entity_fields =_database.fetch(query) %}
{% if entity_fields | length > 0 %}
 {% set default_seq =entity_fields[0]["FIELD_SEQUENCE"] %}
 {% else %}
 {% set default_seq =1 %}
{%endif%}

INSERT INTO EVA_DYNAMIC_ENTITY_FIELD (ID, ENTITY_DEF_ID, NAME, INITIAL_VALUE, FIELD_TYPE_ID, FIELD_SEQUENCE, ENTITY_DEF_ENV_ID)
VALUES (@EDEF.{{keyname}}, @ED.{{__entity_keyname}}, '{{field_name}}', '', @EFT.{{field_type | suggest(_keynames.EFT)}}, {{sequence | default(default_seq)}}, @ENV.Dflt);

