--["createInfo2","Info","Create Info 2","DynamicContentCaseCreateInfo2","en-US","@ED.KnowledgeArticle"]

INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED,TYPE) VALUES (
@PD.DynamicContentCaseCreateInfo2, -- ID
@ENV.Dflt, -- ENV_ID
'DynamicContentCaseCreateInfo2', -- NAME
'AddKnowContentCase.Implementation.DynamicContentCase.Verbs.Create', -- REPOSITORY_PATH
NULL, --CONFIG_PROCESS_ID
'N', --IS_DELETED
@PDT.Verb --TYPE
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'DynamicContentCaseCreateInfo2__AddKnowContentCase/Implementation/DynamicContentCase/Verbs/Create', -- OBJECT_INSTANCE
@PD.DynamicContentCaseCreateInfo2, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'DynamicContentCaseCreateInfo2', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'DynamicContentCaseCreateInfo2__AddKnowContentCase/Implementation/DynamicContentCase/Verbs/Create', -- OBJECT_INSTANCE
@PD.DynamicContentCaseCreateInfo2, -- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'DynamicContentCaseCreateInfo2', -- TEXT
'N'
);

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) VALUES (
@PDR.DynamicContentCaseCreateInfo2, --ID
@PD.DynamicContentCaseCreateInfo2, --PROCESS_DESCRIPTOR_ID
@ENV.Dflt, --PROCESS_DESCRIPTOR_ENV_ID
@ED.KnowledgeArticle, --CONFIG_ID
'N' -- IS_SHARED
);

INSERT INTO EVA_VERB (ID, NAME, PROCESS_DESC_REF_ID, ENTITY_DEF_ID, ENTITY_DEF_ENV_ID, IS_INSTANCE, IS_DEFAULT, IS_INSTANCE_DEFAULT, IS_USER_VISIBLE) VALUES (
@V.DynamicContentCaseCreateInfo2, --ID
'createInfo2', -- NAME
@PDR.DynamicContentCaseCreateInfo2, --PROCESS_DESC_REF_ID
@ED.DynamicContentCase, -- ENTITY_DEF_ID
@ENV.Dflt, -- ENTITY_DEF_ENV_ID
'N', --IS_INSTANCE
'N', -- IS_DEFAULT
'N', -- IS_INSTANCE_DEFAULT
'Y' -- IS_USER_VISIBLE
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'VerbED',-- OBJECT_TYPE
'DynamicContentCaseED__createInfo2',-- OBJECT_INSTANCE
@V.DynamicContentCaseCreateInfo2,-- OBJECT_VERSION
'displayName',-- FIELD_NAME
'en-US',-- LOCALE
'default', -- LOOKUP_LOCALE
'Info', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'VerbED',-- OBJECT_TYPE
'DynamicContentCaseED__createInfo2',-- OBJECT_INSTANCE
@V.DynamicContentCaseCreateInfo2,-- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US',-- LOCALE
'default', -- LOOKUP_LOCALE
'Create Info 2', -- TEXT
'N'
);

UPDATE EVA_CONTEXT_VERB_ENTRY
SET (SEQUENCE_NUMBER) = (1)
where CONFIG_ID = @CC.KMAuthoringHome;

INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (
	 @CC.KMAuthoringHome,--config_id
  	 @ENV.Dflt, --config_env_id
  	 'createInfo2', --verbname
  	 @ET.DynamicContentCase, --entity_type
  	 @ENV.Dflt, --entity_def_type_env_id
  	 1, --sequence_number
  	 @RELEASE.ID --release_id
       );
