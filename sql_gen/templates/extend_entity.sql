{#
To extend entity we create a new "Base" entity pointing to the OTB  object and interface.
Then we update the OTB entity to point to our extended object and to inherit from the new "Base" entity
#}
{% set tmp = extended_entity_id | description("Entity name you would like to extend(e.g Contact)") | suggest(_keynames.ED) %}
{% set int_child_object_path = child_object_path %}
{% set int_child_interface_path = child_interface_path %}

{# We create a new "base" entity using the values from the extended entity#}
{% set extended_entity = _db.find.ed_by_id_n_locale(extended_entity_id) %}
{% set entity_id = "Base"+extended_entity_id %}
{% set tmp_display_name = "Base "+extended_entity['DISPLAY_NAME'] %}
{% set tmp_description = "Base "+extended_entity['DESCRIPTION'] %}
{% set logical_object_path = extended_entity['LOGICAL_OBJ_PATH'] %}
{% set interface_path = extended_entity['INTERFACE_PATH'] %}
{% set super_entity_definition =extended_entity['SUPER_ENTITY_DEFINITION'] %}
{% set is_basic = extended_entity['IS_BASIC'] %}
{% set supports_readonly = extended_entity['SUPPORTS_READONLY'] %}
{% set is_expandable = extended_entity['IS_EXPANDABLE'] %}
{% set category_id = "SystemContact" %}
{%include 'add_entity_definition.sql' %}


UPDATE EVA_ENTITY_DEFINITION
SET (LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID) = ('{{int_child_object_path}}', '{{int_child_interface_path}}', @ED.{{entity_id}}, @ENV.Dflt) WHERE ID = @ED.{{extended_entity_id}} AND ENV_ID = @ENV.Dflt AND RELEASE_ID = @RELEASE.ID;
