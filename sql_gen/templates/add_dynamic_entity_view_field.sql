{% set __entity_keyname = entity_keyname | suggest(_keynames.ED) %}
{% set views = _db.fetch.views_by_ed(__entity_keyname).column("KEYNAME") %}
{% set __entity_view_keyname = entity_view_keyname | suggest(views)%}
{% set fields = _db.fetch.fields_by_ed(__entity_keyname).column("KEYNAME") %}
{% set __entity_field_keyname = entity_field_keyname | suggest(fields) %}
{% set __component_type_keyname = component_type_keyname | suggest(_keynames.FULL_ECT) | default("NULL")%}
{% set __show_label = show_label  | description("show_label(Y/N)")%}
{% set view_fields = _db.fetch.view_fields_by_view(__entity_view_keyname) %}
{% if view_fields | length > 0 %}
  {% set default_seq_no = view_fields[0]['VIEW_FIELD_SEQUENCE'] %}
{% else %}
  {% set default_seq_no = "1" %}
{% endif %}
{% set __view_field_sequence = view_field_sequence | default(default_seq_no) %}

{% set view_groups = _db.fetch.view_groups(__entity_view_keyname) %}
{% set view_group_names = view_groups.column("GROUP_NAME") %}
{% set __group_name = group_name | suggest(view_group_names)
 				 | print ("The group name is the tab tile and determines in which tab the field will be displayed (e.g Public Information, tags...)")%}
{% set __group_row =view_groups.find(GROUP_NAME=__group_name) %}

{% if __group_row is none %}
{% set __group_keyname = __entity_view_keyname+"Group"+__group_name | replace(" ","") %}
INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_GROUP (ID,VIEW_ID,GROUP_NAME,RELEASE_ID,TENANT_ID) 
VALUES (@EDEVG.{{__group_keyname}},@DEV.{{__entity_view_keyname}},'Public Information',1,'default');
{% else %}
{% set __group_keyname = __group_row["KEYNAME"] %}
{% endif %}


{# Compute keyname #}
{% set __field_name = __entity_field_keyname | replace(entity_keyname,"") %}
{% set __entity_view_field_keyname = __entity_view_keyname + __field_name | replace(" ","")%}
{# End Compute keyame #}
{% set field_pds =_db.fetch.all_field_pds().column("KEYNAME") %}
{% set __show_as_pd = show_as_pd | suggest(field_pds)%}
{% set process_desc_ref_keyname =__show_as_pd+__entity_field_keyname%}
INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) 
VALUES (@PDR.{{process_desc_ref_keyname}}, @PD.{{__show_as_pd}}, @ENV.Dflt, NULL, 'N');

INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_FIELD (ID, DYN_ENTITY_VIEW_ID, DYN_ENTITY_FIELD_ID, COMPONENT_TYPE_ID, PROCESS_DESC_REF_ID, SHOW_LABEL, VIEW_FIELD_SEQUENCE, GROUP_ID) 
VALUES (
	@EDEVF.{{__entity_view_field_keyname}}, --ID
	@DEV.{{__entity_view_keyname}}, --DYN_ENTITY_VIEW_ID
       	@EDEF.{{__entity_field_keyname}}, --DYN_ENTITY_FIELD_ID
       	{{__component_type_keyname}}, --COMPONENT_TYPE_ID
       	@PDR.{{process_desc_ref_keyname}}, --PROCESS_DESC_REF_ID
       	'{{__show_label}}', --SHOW_LABEL
       	{{__view_field_sequence}}, --VIEW_FIELD_SEQUENCE
       	@EDEVG.{{__group_keyname}} --GROUP_ID
);
