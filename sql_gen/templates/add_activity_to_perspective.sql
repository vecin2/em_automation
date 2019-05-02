{% set tmp1 = perspective_id | suggest(_keynames.CC) %}
{% set entity_type_tmp = entity_type | suggest(_keynames.ET) %}
{% set verb_names = _db.list.v_names_by_et(entity_type) %}
{% set tmp2 = verb_name | suggest(verb_names)%} 
{% set perspective_verbs = _db.fetch.v_displaynames_by_pers_id(perspective_id) %}
INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (
	 @CC.{{perspective_id}},--config_id
  	 @ENV.Dflt, --config_env_id
  	 '{{verb_name}}', --verbname
  	 @ET.{{entity_type}}, --entity_type
  	 @ENV.Dflt, --entity_def_type_env_id
  	 {{sequence_number | int | description("sequence_number",perspective_verbs)}}, --sequence_number
  	 @RELEASE.ID --release_id
       );
{% set to_update = perspective_verbs.where(SEQUENCE_NUMBER=sequence_number | int )%}
{% for item in to_update %}

	UPDATE EVA_CONTEXT_VERB_ENTRY
	SET SEQUENCE_NUMBER = {{ item.SEQUENCE_NUMBER + 1 }}
	where CONFIG_ID = {{item.CONFIG_ID}}
	and ENTITY_DEF_TYPE_ID = {{item.ENTITY_DEF_TYPE_ID}}
	and VERB = {{item.verb}}

{% endfor %}
