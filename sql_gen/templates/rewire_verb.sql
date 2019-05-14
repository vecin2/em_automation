{# Compute variables for add_process_descriptor#}
 {# Compute current pd #}
	{% set verb_names= _db.list.v_names_by_ed(entity_def_id | suggest(_keynames.ED)) %}
	{% set __verb_name = verb_name | suggest(verb_names) %}
	{% set old_pd = _db.find.pd_by_ed_n_vname(entity_def_id,__verb_name) %}

 {# Request add_process_desc_variables using old pd #}
 {% set config_id = 	  __config_id        	   | description("config_id, default fetched from current value",old_pd)
			  	  	           | default(old_pd['CONFIG_ID']) %}

 {% set process_descriptor_type = __process_descriptor_type      | description('type_id (0=regular process, 2=action, 3=sla)')
					           | default(old_pd['TYPE']) %}

 {% set suggested_ext_path =      _emprj.prefix()+old_pd['REPOSITORY_PATH'] %}
 {% set repository_path=          __repository_path | description("repository_path")
					        | codepath()
					        | default (suggested_ext_path) %}

 {% set process_descriptor_id = _emprj.prefix()+ entity_def_id.capitalize() + __verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}

{# Compute variables for process_descriptor_ref#}
 {% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'hidden_templates/add_process_descriptor_ref.sql' %}


{# Rewire verb to point to new process descriptor#}
UPDATE EVA_VERB 
SET (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_ref_id}})
WHERE ENTITY_DEF_ID = @ED.{{entity_def_id}} AND NAME ='{{__verb_name}}';





