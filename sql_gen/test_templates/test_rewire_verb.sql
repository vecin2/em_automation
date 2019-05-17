-- {"entity_def_id":"Customer","verb_name":"identifyCustomer","config_id":"NULL","type_id":"Verb","repository_path":"PCCoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper","_locale":"en-US"}
INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE)
VALUES (
	 @PD.PCCustomerIdentifycustomer, --id
	 @ENV.Dflt, --env_id,
	 'PCCustomerIdentifycustomer', --process_descriptor_name
	 'PCCoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper', --repository_path
	 NULL, --config_id
	 'N', --is_deleted
	 @PDT.Verb --type
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'PCCustomerIdentifycustomer__PCCoreEntities/Implementation/Customer/Verbs/IdentifyCustomerWrapper', -- OBJECT_INSTANCE
@PD.PCCustomerIdentifycustomer, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'PCCustomerIdentifycustomer', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'PCCustomerIdentifycustomer__PCCoreEntities/Implementation/Customer/Verbs/IdentifyCustomerWrapper', -- OBJECT_INSTANCE
@PD.PCCustomerIdentifycustomer, -- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'PCCustomerIdentifycustomer', -- TEXT
'N'
);

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED)
VALUES (
	@PDR.PCCustomerIdentifycustomer, --id
	@PD.PCCustomerIdentifycustomer, --process_descriptor_id
	@ENV.Dflt, --process_descriptor_env_id
	NULL, --config_id
	'N' --is_shared
);


UPDATE EVA_VERB
SET (PROCESS_DESC_REF_ID) = (@PDR.PCCustomerIdentifycustomer)
WHERE ENTITY_DEF_ID = @ED.Customer AND NAME ='identifyCustomer';


