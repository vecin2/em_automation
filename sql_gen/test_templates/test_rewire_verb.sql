-- {"entity_def_id":"Customer","verb_name":"identifyCustomer","config_id":"NULL","type_id":"0","repository_path":"GSC1CoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper"}
INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE)
VALUES (
	 @PD.GSC1CustomerIdentifycustomer, --id
	 @ENV.Dflt, --env_id,
	 'GSC1CustomerIdentifycustomer', --process_descriptor_name
	 'GSC1CoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper', --repository_path
	 NULL, --config_id
	 'N', --is_deleted
	 0 --type
);

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED)
VALUES (
	@PDR.GSC1CustomerIdentifycustomer, --id
	@PD.GSC1CustomerIdentifycustomer, --process_descriptor_id
	@ENV.Dflt, --process_descriptor_env_id
	NULL, --config_id
	'N' --is_shared
);

UPDATE EVA_VERB
SET (PROCESS_DESC_REF_ID) = (@PDR.GSC1CustomerIdentifycustomer)
WHERE ENTITY_DEF_ID = @ED.Customer AND NAME ='identifyCustomer';


