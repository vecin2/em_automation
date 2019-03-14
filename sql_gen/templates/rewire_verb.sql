{# Compute variables for add_process_descriptor#}
 {# Compute current pd #}
	{% set entity_ids = _keynames.ED %}
	{% set verb_names= _db.list.v_names_by_ed(entity_def_id | suggest(entity_ids)) %}
	{% set verb_name_tmp = verb_name | suggest(verb_names) %}
	{% set old_pd = _db.find.pd_by_ed_n_vname(entity_def_id,verb_name) %}

 {# Request add_process_desc_variables using old pd #}
 {% set config_id = 	  tmp_pd_config        	   | description("config_id, default fetched from current value")
			  	  	           | default(old_pd['CONFIG_ID']) %}

 {% set process_descriptor_type = tmp_pd_type      | description('type_id (0=regular process, 2=action, 3=sla)')
					           | default(old_pd['TYPE']) %}

 {% set suggested_ext_path =      _emprj.prefix()+old_pd['REPOSITORY_PATH'] %}
 {% set repository_path=          tmp_repo_path | description("repository_path")
					        | codepath()
					        | default (suggested_ext_path) %}

 {% set process_descriptor_id = _emprj.prefix()+ entity_def_id.capitalize() + verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}

{# Compute variables for process_descriptor_ref#}
 {% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'hidden_templates/add_process_descriptor_ref.sql' %}


{# Rewire verb to point to new process descriptor#}
UPDATE EVA_VERB 
SET (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_ref_id}})
WHERE ENTITY_DEF_ID = @ED.{{entity_def_id}} AND NAME ='{{verb_name}}';





Running find returns a dictionary with column names as keys.
{% set verb= _db.find.v__by_id({{verb_id | default("2129")}}) %}
Returns verb['NAME']={{verb['NAME']}}

{% set verb_fetch= _db.fetch.v__by_id({{fetch_verb_id | default("2129")}}) %}
Returns verbs[0]['NAME'] ={{verb[0]['NAME']}}

{% set verb_list= _db.list.v_names_by_ed("Customer") %}
Returns verb_list[0]={{verb_list[0]}}
