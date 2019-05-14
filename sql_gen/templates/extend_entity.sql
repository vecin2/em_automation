{#
To extend entity we create a new "Base" entity pointing to the OTB  object and interface.
Then we update the OTB entity to point to our extended object and to inherit from the new "Base" entity
#}
{% set tmp = extended_entity_id | description("Entity keyname you would like to extend(e.g Contact)") | suggest(_keynames.ED) %}

{# We create a new "base" entity using the values from the extended entity#}
{% set extended_entity = _db.find.ed_by_keyname_n_locale(extended_entity_id) %}
{% set entity_name = "Base"+extended_entity["NAME"] %}
{% set entity_display_name = extended_entity['DISPLAY_NAME'] +" Base Class" %}
{% set entity_description = extended_entity['DESCRIPTION'] +" Base Class" %}
{% set logical_object_path = extended_entity['LOGICAL_OBJ_PATH'] %}
{% set interface_path = extended_entity['INTERFACE_PATH'] %}
{% set super_entity_definition =extended_entity['SUPER_ENTITY_DEFINITION'] %}
{% set is_basic = extended_entity['IS_BASIC'] %}
{% set supports_readonly = extended_entity['SUPPORTS_READONLY'] %}
{% set is_expandable = extended_entity['IS_EXPANDABLE'] %}
{% set category_id = "SystemContact" %}

{% set extension_object_path = _prjprefix + logical_object_path | objectpath +"."+_prjprefix +logical_object_path | objectname %}
{% set extension_interface_path = _prjprefix + interface_path | objectpath +"." + interface_path | objectname | replace("EI","EI"+_prjprefix)%}
{% set int_child_object_path = child_object_path | default(extension_object_path) | codepath() | replace(".xml","")%}
{% set int_child_interface_path = child_interface_path | default(extension_interface_path) | codepath()| replace(".xml","") %}
{%include 'add_entity_definition.sql' %}

{% if entity_name.endswith('ED') %}
  {% set entity_id = entity_name[:-2] %}
{% else %}
  {% set entity_id = entity_name %}
{%endif%}
UPDATE EVA_ENTITY_DEFINITION
SET (LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID) = ('{{int_child_object_path}}', '{{int_child_interface_path}}', @ED.{{entity_id}}, @ENV.Dflt) WHERE ID = @ED.{{extended_entity_id}} AND ENV_ID = @ENV.Dflt AND RELEASE_ID = @RELEASE.ID;
