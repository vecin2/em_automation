{% set entity_type_tmp = entity_type | suggest(_keynames.ET) %}
{% set verb_names = _db.list.v_names_by_et(entity_type) %}
INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (
	 @CC.{{perspective_id | suggest(_keynames.CC) }},--config_id
  	 @ENV.Dflt, --config_env_id
  	 '{{verb_name | suggest(verb_names) }}', --verbname
  	 @ET.{{entity_type}}, --entity_type
  	 @ENV.Dflt, --entity_def_type_env_id
  	 1, --sequence_number
  	 @RELEASE.ID --release_id
       );
