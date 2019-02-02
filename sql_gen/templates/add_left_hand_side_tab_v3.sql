
{% set pptive_ids = _keynames.PPTIVE %}
{% set verb_ids = _keynames.V %}
INSERT INTO FD_ENTITY__AUX_VERBS (ENTITY_ID,ENTITY_ENV_ID,ENTITY_TYPE_ID,ENTITY_TYPE_ENV_ID,AUXILIARY_VERB_ID,SEQUENCE_NUM,RELEASE_ID,TENANT_ID)
VALUES (
	@PPTIVE.{{perspective_id | suggest(pptive_ids)}}, -- entity_id 
	@ENV.Dflt, --entity_env_id
	@ET.Perspective,--entity_type_id
	@ENV.Dflt, --entity_type_env_id
	@V.{{verb_id | suggest(verb_ids)}}, --auxiliary_verb_id
	{{sequence_num}},--sequence_num
	@RELEASE.ID,--relase_id
	'default' --tenant_id
);

