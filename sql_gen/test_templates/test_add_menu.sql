--{"menu_name":"manageTools","image_path":"","parent_menu_id":"","verb_display_name":"Manage Tools","verb_description":"Manage Tools Description","verb_id":"menuManageTools","process_desc_ref_id":"","is_instance":"N","is_user_visible":"Y","locale":"en-US"}
INSERT INTO FD_MENU (ID, ENV_ID, NAME, IMAGE_PATH, PARENT_ID, PARENT_ENV_ID, IS_DELETED)
VALUES(
	@MN.manageToolsMenu, --ID
	@ENV.Dflt,--ENV_ID
	'manageTools',--NAME
	'/CorePageSetEditor/Implementation/ScriptingMenu/UI/Images/sciboodleManageScriptingPageSetsUp64x64',--IMAGE_PATH
       	@MN.RootMenu,--PARENT_ID
       	@ENV.Dflt,--PARENT_ENV_ID
       	'N'--IS_DELETED
);

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) VALUES (
@PDR.menuManageTools, --ID
@PD.DefaultRunPanel, --PROCESS_DESCRIPTOR_ID
@ENV.Dflt, --PROCESS_DESCRIPTOR_ENV_ID
@MN.manageToolsMenu, --CONFIG_ID
'N' -- IS_SHARED
);
INSERT INTO EVA_VERB (ID, NAME, PROCESS_DESC_REF_ID, ENTITY_DEF_ID, ENTITY_DEF_ENV_ID, IS_INSTANCE, IS_DEFAULT, IS_INSTANCE_DEFAULT, IS_USER_VISIBLE) VALUES (
@V.menuManageTools, --ID
'manageTools', -- NAME
@PDR.menuManageTools, --PROCESS_DESC_REF_ID
@ED.Menu, -- ENTITY_DEF_ID
@ENV.Dflt, -- ENTITY_DEF_ENV_ID
'N', --IS_INSTANCE
'N', -- IS_DEFAULT
'N', -- IS_INSTANCE_DEFAULT
'Y' -- IS_USER_VISIBLE
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'VerbED',-- OBJECT_TYPE
'MenuED__manageTools',-- OBJECT_INSTANCE
@V.menuManageTools,-- OBJECT_VERSION
'displayName',-- FIELD_NAME
'en-US',-- LOCALE
'default', -- LOOKUP_LOCALE
'Manage Tools', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'VerbED',-- OBJECT_TYPE
'MenuED__manageTools',-- OBJECT_INSTANCE
@V.menuManageTools,-- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US',-- LOCALE
'default', -- LOOKUP_LOCALE
'Manage Tools Description', -- TEXT
'N'
);
