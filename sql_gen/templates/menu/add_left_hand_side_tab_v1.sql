INSERT INTO FD_ENTITY__AUX_VERBS (ENTITY_ID,ENTITY_ENV_ID,ENTITY_TYPE_ID,ENTITY_TYPE_ENV_ID,AUXILIARY_VERB_ID,SEQUENCE_NUM,RELEASE_ID,TENANT_ID)
VALUES (
	{{entity_id}}, -- entity_id 
	@ENV.Dflt, --entity_env_id
	@ET.Perspective,--entity_type_id
	@ENV.Dflt, --entity_type_env_id
	{{verb_id}}, --auxiliary_verb_id
	{{sequence_num}},--sequence_num
	@RELEASE.ID,--relase_id
	'default' --tenant_id
);

