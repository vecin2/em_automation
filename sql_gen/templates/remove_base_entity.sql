{% set __extension_entity_id = extension_entity_id | suggest(_keynames.entity_name) %}
{% set extension_entity = _db.find.ed_by_keyname(__extension_entity_id) %}
{% set base_entity = _db.find.ed_by_id(extension_entity['SUPER_ENTITY_DEFINITION']) %}

UPDATE EVA_ENTITY_DEFINITION
SET (LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID) = ('{{base_entity["LOGICAL_OBJ_PATH"]}}', '{{base_entity["INTERFACE_PATH"]}}', @ED.{{_keynames.get("ED",base_entity["SUPER_ENTITY_DEFINITION"]) }}, @ENV.Dflt) 
WHERE ID = @ED.{{extension_entity_id}} AND ENV_ID = @ENV.Dflt AND RELEASE_ID = @RELEASE.ID;

{% set entity_id = base_entity["KEYNAME"] %}
{% include 'remove_entity_definition.sql' %}

