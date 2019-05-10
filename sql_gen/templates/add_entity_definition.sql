{% set tmp = entity_id | description("Please enter the entity_id, e.g Policy,PRJCustomer - do not add 'ED' at the end")%}
{% set entity_name=entity_id+"ED" %}
{% set default_display_name = entity_id | split_uppercase() %}
{% set display_name = tmp1 | description("display_name") 
			   | default(default_display_name)%}
{% set description = tmp5 | description("description") 
			   | default(default_display_name)%}
INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, IS_DELETED, IS_BASIC, SUPPORTS_READONLY,IS_EXPANDABLE,ICON_PATH, INSTANCE_ICON_PATH) VALUES (
@ED.{{entity_id}}, -- ID
@ENV.Dflt, -- ENV_ID
'{{entity_name}}', -- NAME
'{{entity_name}}', -- UUID
'{{entity_name}}', -- TYPE_UUID
@ET.{{entity_id}}, -- TYPE_ID
@ENV.Dflt, -- TYPE_ENV_ID
'{{logical_object_path  | codepath() | replace(".xml","")}}', -- LOGICAL_OBJECT_PATH
'{{interface_path | codepath() | replace(".xml","")}}', -- INTERFACE_PATH
{{super_entity_definition | suggest(_keynames.FULL_ED) | default ("PersistableEntity")}}, -- SUPER_ENTITY_DEFINITION
@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID
'N', -- IS_DELETED
'{{is_basic | description("is_basic(Y/N)") | default("Y")}}', -- IS_BASIC
'{{supports_readonly | description("supports_readonly(Y/N)") | default("Y")}}', -- SUPPORTS_READ_ONLY
'{{is_expandable | description("is_expandable(Y/N)") | default("N")}}', --IS_EXPANDABLE
NULL, -- ICON_PATH
NULL -- INSTANCE_ICON_PATH
);
{% set tmp6 = category_id | suggest(_keynames.EC) | default(_entity_category) %}
{% set category = _db.fetch.category_by_id %}
{% if category_id not in _keynames.EC %}
{% include 'add_category.sql' %}
{% endif %}
INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (
@EC.{{category_id}}, -- CATEGORY_ID
@ENV.Dflt, -- CATEGORY_ENV_ID
@ED.{{entity_id}}, -- ENTITY_ID
@ENV.Dflt -- ENTITY_ENV_ID
);

{% set object_type ="EntityDefinitionED" %}
{% set object_instance = entity_name %}
{% set object_version = "@ED." +entity_id %}
{% set field_name = "displayName" %}
{% set text = display_name %}
{% include 'add_localised_field.sql' %}

{% set field_name = "description" %}
{% set text = description %}
{% include 'add_localised_field.sql' %}
