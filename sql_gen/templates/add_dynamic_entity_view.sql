{% set __entity_keyname = entity_keyname | suggest(_keynames.ED) %}
{% set __view_name = view_name | description("view_name (e.g. View,Create,Edit)")%}
{% set __view_keyname = __entity_keyname + __view_name %}
{% set view_types = _db.fetch.all_dynamic_view_types() %}
{% set view_type_keynames =view_types.column("KEYNAME") %}
INSERT INTO EVA_DYNAMIC_ENTITY_VIEW (ID,ENTITY_DEF_ID,ENTITY_DEF_ENV_ID,NAME,RELEASE_ID,VIEW_TYPE_ID,VIEW_TYPE_ENV_ID,USE_TABS,TENANT_ID) 
VALUES (
	@DEV.{{__view_keyname}}, --ID
	@ED.{{__entity_keyname}}, --ENTITY_DEF_ID
	@ENV.Dflt, --ENTITY_DEF_ENV_ID
	'{{__view_name}}', --NAME
	@RELEASE.ID, --RELEASE_ID
	@ET.{{view_type_keyname | suggest(view_type_keynames)}}, --VIEW_TYPE_ID
	@ENV.Dflt, --VIEW_TYPE__ENV_ID
	'{{use_tabs | description("use_tabs (Y/N)")}}', --USE_TABS
	'default');

INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_LAYOUT (ID,RELEASE_ID,LAYOUT_TYPE_ID,TENANT_ID) 
VALUES (
	@DEV.{{__view_keyname}},
	@RELEASE.ID, --RELEASE_ID
	@ELT.{{layout_type_keyname | suggest(_keynames.ELT)}},
	'default');

{% set __entity = _db.find.ed_by_keyname(__entity_keyname) %}
{% set object_type ="DynamicEntityDefinitionED" %}
{% set object_instance = __entity["NAME"] %}
{% set object_version = "@ED."+__entity_keyname %}
{% set field_name = "views."+__view_name +".displayName" %}
{% set default_display_view_name = __entity_keyname+__view_name %}
{% set text = display_view_name | default(default_display_view_name)  %}
{% include 'add_localised_field.sql' %}
