INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, TYPE_ID, TYPE_ENV_ID,  LOGICAL_OBJ_PATH, INTERFACE_PATH, IS_DELETED, ICON_PATH, INSTANCE_ICON_PATH , SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, RELEASE_ID, SUPPORTS_READONLY, IS_EXPANDABLE, IS_BASIC)  
VALUES (
	@ED.{{entity_id}}, --id
       	@ENV.Dflt, --env_id
       	'{{entity_name}}',--name
       	@ET.{{entity_id}},--type_id
       	@ENV.Dflt, --type_env_id
       	'{{object_path}}',--object_path
       	'{{interface_path}}',--interface_path
       	'N',--is_delted
       	'',--icon_path
       	'',--instance_icon_path
       	NULL,--super_entity_definition
       	NULL,--super_entity_definition_env_id
       	@RELEASE.ID, --release_id
       	'Y', --supports_readonly
       	'N',--is_expandable
       	'Y' --is_basic
      );

INSERT INTO EVA_ENTITY_DEFINITION_LOC(ID, ENV_ID, LOCALE, DISPLAY_NAME, DESCRIPTION, RELEASE_ID) VALUES
(@ED.$ENTITY_ID, @ENV.Dflt, 'en-GB', '$ENTITY_ID', '$ENTITY_ID',@RELEASE.ID);

INSERT INTO EVA_CATEGORY_ENTRY (CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (@EC.SystemGeneral, @ENV.Dflt, @ED.${ENTITY_ID}, @ENV.Dflt);
