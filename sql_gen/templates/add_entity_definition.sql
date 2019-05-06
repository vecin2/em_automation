{% set tmp = entity_id | description("Please enter the entity_id, e.g Policy,PRJCustomer - do not add 'ED' at the end")%}
{% set default_display_name = entity_id | split_uppercase() %}
{% set display_name = tmp1 | description("display_name") 
			   | default(default_display_name)%}
INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, IS_DELETED, IS_BASIC, ICON_PATH, INSTANCE_ICON_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, SUPPORTS_READONLY) VALUES (
@ED.{{entity_id}}, -- ID
@ENV.Dflt, -- ENV_ID
'{{entity_id}}ED', -- NAME
'{{entity_id}}', -- UUID
'{{entity_id}}', -- TYPE_UUID
@ET.{{entity_id}}, -- TYPE_ID
@ENV.Dflt, -- TYPE_ENV_ID
'{{logical_object_path  | codepath() | replace(".xml","")}}', -- LOGICAL_OBJECT_PATH
'{{interface_path | codepath() | replace(".xml","")}}', -- INTERFACE_PATH
'N', -- IS_DELETED
'{{is_basic | description("is_basic(Y/N)") | default("Y")}}', -- IS_BASIC
NULL, -- ICON_PATH
NULL, -- INSTANCE_ICON_PATH
{{super_entity_definition | suggest(_keynames.FULL_ED) | default ("PersistableEntity")}}, -- SUPER_ENTITY_DEFINITION
@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID
'{{supports_readonly | description("supports_readonly(Y/N)") | default("Y")}}' -- SUPPORTS_READ_ONLY
);
INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (
@EC.{{category_id | suggest(_keynames.EC) | default(_entity_category)}}, -- CATEGORY_ID
@ENV.Dflt, -- CATEGORY_ENV_ID
@ED.{{entity_id}}, -- ENTITY_ID
@ENV.Dflt -- ENTITY_ENV_ID
);

{% set object_type ="EntityDefinitionED" %}
{% set object_instance = entity_id %}
{% set keyset="ED"%}
{% include 'add_localised_field.sql' %}
