{% set tmp = verb_name %}
{% set default_display_name =  verb_name | split_uppercase() %}
{% set verb_display_name = tmp1 | description("verb_display_name")
			       | default(default_display_name)%}
{% set tmp = entity_def_id | suggest(_keynames.ED) %}
{% set capitalized_verb_name = verb_name | capitalize() %}
{% set default_verb_id = _prjprefix+entity_def_id+capitalized_verb_name %}
{% set verb_id = tmp44 | default(default_verb_id) %}
{% set process_descriptor_id = verb_id %}
{% include 'add_process_descriptor.sql' %}

{% set process_descriptor_ref_id = verb_id %}
{% include 'hidden_templates/add_process_descriptor_ref.sql' %}

{% set entity_ids = _keynames.ED %}
INSERT INTO EVA_VERB (ID, NAME, PROCESS_DESC_REF_ID, ENTITY_DEF_ID, ENTITY_DEF_ENV_ID, IS_INSTANCE, IS_DEFAULT, IS_INSTANCE_DEFAULT, IS_USER_VISIBLE) VALUES (
@V.{{verb_id}}, --ID
'{{verb_name}}', -- NAME
@PDR.{{process_descriptor_ref_id}}, --PROCESS_DESC_REF_ID
@ED.{{entity_def_id | suggest(entity_ids)}}, -- ENTITY_DEF_ID
@ENV.Dflt, -- ENTITY_DEF_ENV_ID
'{{is_instance | description("is_instance (Y/N)")}}', --IS_INSTANCE
'N', -- IS_DEFAULT
{% if is_instance == 'N'%} {% set is_instance_default = 'N' %} {%endif%}
'{{is_instance_default | description("is_instance_default (Y/N)")}}', -- IS_INSTANCE_DEFAULT
'{{is_user_visible | description("is_user_visible (Y/N)")}}' -- IS_USER_VISIBLE
);

{% set entity = _db.find.ed_by_id(entity_def_id) %}
{% set object_type = "VerbED" %}
{% set object_instance =  entity["NAME"]+"__"+verb_name %}
{% set object_version = "@V."+verb_id %}
{% set display_name = verb_display_name %}
{% set field_name= 'displayName'  %}
{% include 'add_localised_field.sql' %}

{% set field_name= 'description'  %}
{% include 'add_localised_field.sql' %}
