--{"entity_id":"Agreement","entity_display_name":"Agreement","entity_description":"Agreement Description","logical_object_path":"PacificorpAccount.Implementation.Objects.Agreement","interface_path":"PacificorpAccount.API.EIAgreement","super_entity_definition":"@ED.PersistableEntity","is_basic":"Y","supports_readonly":"Y","category_id":"Pacificorp","_locale":"en-US"}
INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, IS_DELETED, IS_BASIC, SUPPORTS_READONLY, ICON_PATH, INSTANCE_ICON_PATH) VALUES (
@ED.Agreement, -- ID
@ENV.Dflt, -- ENV_ID
'AgreementED', -- NAME
'AgreementED', -- UUID
'AgreementED', -- TYPE_UUID
@ET.Agreement, -- TYPE_ID
@ENV.Dflt, -- TYPE_ENV_ID
'PacificorpAccount.Implementation.Objects.Agreement', -- LOGICAL_OBJECT_PATH
'PacificorpAccount.API.EIAgreement', -- INTERFACE_PATH
@ED.PersistableEntity, -- SUPER_ENTITY_DEFINITION
@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID
'N', -- IS_DELETED
'Y', -- IS_BASIC
'Y', --SUPPORTS_READONLY
NULL, -- ICON_PATH
NULL -- INSTANCE_ICON_PATH
);
INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (
@EC.Pacificorp, -- CATEGORY_ID
@ENV.Dflt, -- CATEGORY_ENV_ID
@ED.Agreement, -- ENTITY_ID
@ENV.Dflt -- ENTITY_ENV_ID
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'EntityDefinitionED', -- OBJECT_TYPE
'AgreementED', -- OBJECT_INSTANCE
@ED.Agreement, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'Agreement', --TEXT
'N' --IS_DELETED
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'EntityDefinitionED', -- OBJECT_TYPE
'AgreementED', -- OBJECT_INSTANCE
@ED.Agreement, -- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'Agreement Description', --TEXT
'N' --IS_DELETED
);
