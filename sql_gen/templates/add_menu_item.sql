--[]
{% set menu_item_explanation = "A menu item is points to a verb within an entity definition. We need to define as well the menu where this item will be displayed " %}
{% set __entity_def_id = entity_def_id | suggest(_keynames.ED) | print(menu_item_explanation)%}
{% set verb_names = _db.fetch.verbs_by_ed(__entity_def_id).column('NAME') %}
{% set __verb_name = verb_name | suggest(verb_names)%}
{% set __menu = menu | suggest(_keynames.MN) %}
{% set default_menu_item_name = __verb_name +"MenuItem"%}
{% set __menu_item_name = menu_item_name | default(default_menu_item_name)%}
{% set default_menu_item_display_name = __menu_item_name | split_uppercase() %}
{% set __menu_item_display_name = menu_item_display_name | default(default_menu_item_display_name) %}
{% set __menu_item_description = menu_item_description | default(default_menu_item_display_name)%}
{% set __menu_item_id = menu_item_name %}
INSERT INTO FD_MENU_ITEM (ID, ENV_ID, MENU_ID, MENU_ENV_ID, NAME, IMAGE_PATH, IMAGE_PATH_ROLLOVER, VERB_NAME, VERB_ENTITY_DEF_TYPE_ID, VERB_ENTITY_DEF_TYPE_ENV_ID, IS_DELETED) 
VALUES (
	@MNI.{{__menu_item_name}}, --ID
       	@ENV.Dflt, --ENV_ID
       	@MN.{{__menu}}, --MENU_ID
       	@ENV.Dflt, --MENU_ENV_ID
       	'{{__menu_item_name}}', --NAME
       	'{{image_path | default("/FrameworkDesktop/Skin/ControlPanelImages/sciboodleControlPanelFieldEditorsUp64x64")}}', --IMAGE_PATH
	'{{image_path_rollover | default("/FrameworkDesktop/Skin/ControlPanelImages/sciboodleControlPanelFieldEditorsUp64x64")}}',--IMAGE_PATH_ROLLOVER
       	'{{__verb_name}}', --VERB_NAME
       	@ET.{{__entity_def_id}}, --ENTITY_DEF_ID
       	@ENV.Dflt, --ENTITY_DEF_ENV_ID
       	'N' --IS_DELETED
);
{% set object_type = "MenuItemED" %}
{% set object_instance = __menu_item_name %}
{% set object_version = "@MNI."+__menu_item_name%}
{% set field_name = "displayName" %}
{% set text = __menu_item_display_name %}
{% include 'add_localised_field.sql' %}

{% set field_name = "description" %}
{% set text = __menu_item_description %}
{% include 'add_localised_field.sql' %}
