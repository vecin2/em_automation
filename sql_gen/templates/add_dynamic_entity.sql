{% set __entity_name = entity_name | description("Please enter the entity_name, e.g 'PRJCustomerED' (by convention finishes in ED)")%}
{% if __entity_name.endswith('ED') %}
  {% set entity_id = __entity_name[:-2] %}
{% else %}
  {% set entity_id = __entity_name %}
{%endif%}
{% set default_display_name = entity_id | split_uppercase() %}
{% set __entity_display_name = entity_display_name | description("display_name")
			   | default(default_display_name)%}
{% set __entity_description = entity_description | description("description")
			   | default(default_display_name)%}
--ADD DYNAMIC ENTITY
INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, IS_DELETED, IS_BASIC, SUPPORTS_READONLY,IS_EXPANDABLE,ICON_PATH, INSTANCE_ICON_PATH) VALUES (
@ED.{{entity_id}}, -- ID
@ENV.Dflt, -- ENV_ID
'{{__entity_name}}', -- NAME
'{{__entity_name}}', -- UUID
'{{__entity_name}}', -- TYPE_UUID
@ET.{{entity_id}}, -- TYPE_ID
@ENV.Dflt, -- TYPE_ENV_ID
'FrameworkDynamicEntities.Implementation.DynamicEntity.Objects.DynamicEntity', -- LOGICAL_OBJECT_PATH
'FrameworkDynamicEntities.API.EntityInterfaces.EIDynamicEntity', -- INTERFACE_PATH
@ED.BaseDynamicEntity, -- SUPER_ENTITY_DEFINITION
@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID
'N', -- IS_DELETED
'N', -- IS_BASIC
'Y', -- SUPPORTS_READ_ONLY
'N', --IS_EXPANDABLE
NULL, -- ICON_PATH
NULL -- INSTANCE_ICON_PATH
);

{% set __category_id = "DynamicEntity"%}
{# Category can be null is this template is included, e.g extended_entity.
In that case we dont want to insert in EVA_CATEGORY_ENTRY#}
{% if __category_id != "NULL" %}
  {% set category = _db.fetch.category_by_keyname(__category_id) %}
  {% if category | length ==  0%}
{% include 'add_category.sql' %}
  {% endif %}
  INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (
  @EC.{{__category_id}}, -- CATEGORY_ID
  @ENV.Dflt, -- CATEGORY_ENV_ID
  @ED.{{entity_id}}, -- ENTITY_ID
  @ENV.Dflt -- ENTITY_ENV_ID
  );
{% endif %}

{% set object_type ="DynamicEntityDefinitionED" %}
{% set object_instance = __entity_name %}
{% set object_version = "@ED." +entity_id %}
{% set field_name = "displayName" %}
{% set text = __entity_display_name %}
{% include 'add_localised_field.sql' %}

{% set field_name = "description" %}
{% set text = __entity_description %}
{% include 'add_localised_field.sql' %}

{% set field_name = "summaryExpression" %}
{% set text = summary_expression | description("summary_expression (e.g Article [title])") %}
{% include 'add_localised_field.sql' %}

{% set entity_keyname = entity_id %}
{% include 'add_dynamic_entity_def.sql' %}
