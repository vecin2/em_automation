INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (@CC.{{config_id | 
	         description("config_id (e.g. Home, CustomerPostIdentify, Customer)" )}},--config_id
	      @ENV.Dflt, --config_env_id
	      {{verb_name |
	         description('verb name (e.g. launchIdentifyPlanMember)')}}, --verb_name
	      @ET.{{customer_type}}, --customer_type
	      @ENV.Dflt, --entity_def_type_env_id
	      1, --sequence_number
	      @RELEASE.ID);--release_id
