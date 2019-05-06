INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED,TYPE) VALUES (
@PD.{{process_descriptor_id | description('Enter the new relative verb id e.g PCCustomerInlineSearch')}}, -- ID
@ENV.Dflt, -- ENV_ID
'{{process_descriptor_id}}', -- NAME
'{{repository_path | codepath() | replace(".xml","")}}', -- REPOSITORY_PATH
NULL, --CONFIG_PROCESS_ID
'N', --IS_DELETED
0 --TYPE
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'{{process_descriptor_id}}__{{repository_path}}', -- OBJECT_INSTANCE
$PD.{{process_descriptor_id}}, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'{{process_descriptor_id}}', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'{{process_descriptor_id}}__{{repository_path}}', -- OBJECT_INSTANCE
$PD.{{process_descriptor_id}}, -- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'{{process_descriptor_id}}', -- TEXT
'N'
);

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) VALUES (
@PDR.{{process_descriptor_id}}, --ID
@PD.{{process_descriptor_id}}, --PROCESS_DESCRIPTOR_ID
@ENV.Dflt, --PROCESS_DESCRIPTOR_ENV_ID
NULL, --CONFIG_ID
'N' -- IS_SHARED
);

{% set entity_ids = _keynames.ED %}
INSERT INTO EVA_VERB (ID, NAME, PROCESS_DESC_REF_ID, ENTITY_DEF_ID, ENTITY_DEF_ENV_ID, IS_INSTANCE, IS_DEFAULT, IS_INSTANCE_DEFAULT, IS_USER_VISIBLE) VALUES (
@V.{{process_descriptor_id}}, --ID
'{{process_descriptor_id}}', -- NAME
@PDR.{{process_descriptor_id}}, --PROCESS_DESC_REF_ID
@ED.{{entity_def_id | suggest(entity_ids)}}, -- ENTITY_DEF_ID
@ENV.Dflt, -- ENTITY_DEF_ENV_ID
'{{is_instance | description("is_instance (Y/N)")}}', --IS_INSTANCE
'N', -- IS_DEFAULT
'{{is_instance_default | description("is_instance_default (Y/N)")}}', -- IS_INSTANCE_DEFAULT
'{{is_user_visible | description("is_user_visible (Y/N)")}}' -- IS_USER_VISIBLE
);

{% set entity = _db.find.ed_by_id(entity_def_id) %}
INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'VerbED',-- OBJECT_TYPE
'{{entity["NAME"]}}__{{process_descriptor_id}}',-- OBJECT_INSTANCE
$V.{{process_descriptor_id}},-- OBJECT_VERSION
'displayName',-- FIELD_NAME
'en-US',-- LOCALE
'default', -- LOOKUP_LOCALE
'{{verb_display_name}}', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'VerbED',-- OBJECT_TYPE
'{{entity["NAME"]}}__{{process_descriptor_id}}',-- OBJECT_INSTANCE
$V.{{process_descriptor_id}},-- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US',-- LOCALE
'default', -- LOOKUP_LOCALE
'{{verb_display_name}}', -- TEXT
'N'
);
