{# Compute variables for add_process_descriptor#}
 {# Compute current pd #}
	{% set entity_ids = _keynames.ED %}
	{% set verb_names =_ed.with_keyname(entity_def_id | suggest(entity_ids)).verb_names%}
	{% set verb_name_tmp = verb_name | suggest(verb_names) %}
	{% set old_pd = _pd.load(entity_def_id,verb_name_tmp)%}

 {{config_id 		  |description("config_id, default fetched from current value")
 			  |default(old_pd['CONFIG_ID']) }}
 {{process_descriptor_type| description('type_id (0=regular process, 2=action, 3=sla)')
 			  | default(old_pd['TYPE'])}}
 {%set process_descriptor_id = prj_prefix()+ entity_def_id.capitalize() + verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}

{# Compute variables for process_descriptor_ref#}
 {% set process_descriptor_ref_id = process_descriptor_id %}

{% include 'add_process_descriptor_ref.sql' %}

{# Rewire verb to point to new process descriptor#}
UPDATE EVA_VERB 
SET (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_ref_id}})
WHERE ENTITY_DEF_ID = @ED.{{entity_def_id}} AND NAME ='{{verb_name}}';
