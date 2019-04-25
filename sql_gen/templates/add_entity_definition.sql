@EC.{{category_id | suggest(_keynames.EC)}}, -- CATEGORY_ID
{% set entity_def_ids = _keynames.ED %}
{% set category_ids = _keynames.EC %}
{% set entity_display_name = tmp | description("entity_display_name") %}
INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, IS_DELETED, IS_BASIC, ICON_PATH, INSTANCE_ICON_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, SUPPORTS_READONLY) VALUES (
@ED.{{entity_id}}, -- ID
@ENV.Dflt, -- ENV_ID
'{{entity_id}}', -- NAME 
'{{entity_id}}', -- UUID 
'{{entity_id}}', -- TYPE_UUID 
@ET.{{entity_id}}, -- TYPE_ID
@ENV.Dflt, -- TYPE_ENV_ID
'{{logical_object_path  | codepath()}}', -- LOGICAL_OBJECT_PATH
'{{interface_path | codepath()}}', -- INTERFACE_PATH
'N', -- IS_DELETED
'Y', -- IS_BASIC
NULL, -- ICON_PATH
NULL, -- INSTANCE_ICON_PATH
@ED.{{super_entity_definition | suggest(entity_def_ids) | default ("PersistableEntity")}}, -- SUPER_ENTITY_DEFINITION
@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID
'Y' --SUPPORTS_READONLY
);
INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (
@EC.{{category_id | suggest(_keynames.EC)}}, -- CATEGORY_ID
@ENV.Dflt, -- CATEGORY_ENV_ID
@ED.{{entity_id}}, -- ENTITY_ID
@ENV.Dflt -- ENTITY_ENV_ID
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'EntityDefinitionED', -- OBJECT_TYPE
'{{entity_id}}', -- OBJECT_INSTANCE
@ED.{{entity_id}}, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'{{entity_display_name}}', --TEXT
'N' --IS_DELETED
);
