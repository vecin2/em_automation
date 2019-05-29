{# Compute variables for add_process_descriptor#}
 {# Compute current pd #}
	{% set verb_names= _db.fetch.v_names_by_ed(entity_def_id | suggest(_keynames.ED)).column("NAME") %}
	{% set __verb_name = verb_name | suggest(verb_names) %}
	{% set old_pd = _db.find.pd_by_ed_n_vname(entity_def_id,__verb_name) %}

 {# Request add_process_desc_variables using old pd #}
 {% set default_config_process_id = _keynames.full_keyname("PD",old_pd['CONFIG_PROCESS_ID']) %}
 {% set old_process_desc ="Verb is currently point to this process descriptor:\n"+old_pd  | string %}
 {% set config_process_id =__config_process_id     | print(old_process_desc)
						   | description("config_process_id, default fetched from current value")
			  	  	           | default(default_config_process_id)
						   | suggest(_keynames.FULL_PD) %}

 {% set default_type = _keynames.keyname("PDT",old_pd['PD_TYPE']) %}
 {% set process_descriptor_type = __process_descriptor_type | description("process_descriptor_type")
							    | default(default_type)
							    | suggest(_keynames.PDT) %}

 {% set default_repo_path =      _prjprefix+old_pd['REPOSITORY_PATH'] %}
 {% set repository_path=          __repository_path | description("repository_path")
					            | codepath()
					            | default (default_repo_path) %}

 {% set process_descriptor_id = _prjprefix+ entity_def_id.capitalize() + __verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}

{# Compute variables for process_descriptor_ref#}
 {% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'hidden_templates/add_process_descriptor_ref.sql' %}


{# Rewire verb to point to new process descriptor#}
UPDATE EVA_VERB 
SET (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_ref_id}})
WHERE ENTITY_DEF_ID = @ED.{{entity_def_id}} AND NAME ='{{__verb_name}}';





