--["Home","Customer","inlineCreate","50"]
INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (
	 @CC.Home,--config_id
  	 @ENV.Dflt, --config_env_id
  	 'inlineCreate', --verbname
  	 @ET.Customer, --entity_type
  	 @ENV.Dflt, --entity_def_type_env_id
  	 50, --sequence_number
  	 @RELEASE.ID --release_id
       );
