INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) 
VALUES (
	 @PD.{{ process_descriptor_id }}, --id
	 @ENV.Dflt, --env_id,
	 '{{ process_descriptor_id }}', --process_descriptor_name
	 '{{ repository_path | codepath() | replace(".xml","") }}', --repository_path 
	 {{ config_id | default('NULL') }}, --config_id
	 'N', --is_deleted
	 @PDT.{{ process_descriptor_type |
	         suggest(_keynames.PDT) |
	         default ('Verb') }} --type
       );

{% set object_type ="ProcessDescriptorED" %}
{% set slash_repo_path =repository_path | replace(".","/") %} 
{% set object_instance = process_descriptor_id+"__"+ slash_repo_path %}
{% set object_version = '@PD.' +process_descriptor_id %}
{% set text = process_descriptor_id %}
{% set field_name = "displayName" %}
{% include 'add_localised_field.sql' %}
{% set field_name = "description" %}
{% include 'add_localised_field.sql' %}
