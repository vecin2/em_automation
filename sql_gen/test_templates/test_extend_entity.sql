--{"base_entity_id":"VirtualEnvironment","child_object_path":"","child_inteface_path":"","locale":"en-US"}
INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, IS_DELETED, IS_BASIC, SUPPORTS_READONLY,IS_EXPANDABLE,ICON_PATH, INSTANCE_ICON_PATH) VALUES (
@ED.BaseVirtualEnvironment, -- ID
@ENV.Dflt, -- ENV_ID
'BaseVirtualEnvironmentED', -- NAME
'BaseVirtualEnvironmentED', -- UUID
'BaseVirtualEnvironmentED', -- TYPE_UUID
@ET.BaseVirtualEnvironment, -- TYPE_ID
@ENV.Dflt, -- TYPE_ENV_ID
'FrameworkEVA.Implementation.VirtualEnvironment.Objects.VirtualEnvironment', -- LOGICAL_OBJECT_PATH
'FrameworkEVA.API.Interfaces.EIVirtualEnvironment', -- INTERFACE_PATH
NULL, -- SUPER_ENTITY_DEFINITION
@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID
'N', -- IS_DELETED
'Y', -- IS_BASIC
'Y', -- SUPPORTS_READ_ONLY
'N', --IS_EXPANDABLE
NULL, -- ICON_PATH
NULL -- INSTANCE_ICON_PATH
);
INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (
  @EC.SystemGeneral, -- CATEGORY_ID
  @ENV.Dflt, -- CATEGORY_ENV_ID
  @ED.BaseVirtualEnvironment, -- ENTITY_ID
  @ENV.Dflt -- ENTITY_ENV_ID
  );

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'EntityDefinitionED', -- OBJECT_TYPE
'BaseVirtualEnvironmentED', -- OBJECT_INSTANCE
@ED.BaseVirtualEnvironment, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'Virtual Environment Base Class', --TEXT
'N' --IS_DELETED
);
INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'EntityDefinitionED', -- OBJECT_TYPE
'BaseVirtualEnvironmentED', -- OBJECT_INSTANCE
@ED.BaseVirtualEnvironment, -- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'System can contain a number of virtual environments. Base Class', --TEXT
'N' --IS_DELETED
);
UPDATE EVA_ENTITY_DEFINITION
SET (LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID) = ('PRJFrameworkEVA.Implementation.VirtualEnvironment.Objects.PRJVirtualEnvironment', 'PRJFrameworkEVA.API.Interfaces.EIPRJVirtualEnvironment', @ED.BaseVirtualEnvironment, @ENV.Dflt) WHERE ID = @ED.VirtualEnvironment AND ENV_ID = @ENV.Dflt AND RELEASE_ID = @RELEASE.ID;
