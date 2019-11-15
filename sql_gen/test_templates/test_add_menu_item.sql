--{"entity_def_id":"Customer","verb_name":"inlineSearch","menu":"OrganisationMenu","menu_item_name":"CustomerInlineSearchMenuItem","menu_item_display_name":"Inline Search","menu_item_description":"Inline Search Desc","image_path":"","image_path_roll_over":"","locale":"en-US"}
INSERT INTO FD_MENU_ITEM (ID, ENV_ID, MENU_ID, MENU_ENV_ID, NAME, IMAGE_PATH, IMAGE_PATH_ROLLOVER, VERB_NAME, VERB_ENTITY_DEF_TYPE_ID, VERB_ENTITY_DEF_TYPE_ENV_ID, IS_DELETED) 
VALUES (
	@MNI.CustomerInlineSearchMenuItem, --ID
       	@ENV.Dflt, --ENV_ID
       	@MN.OrganisationMenu, --MENU_ID
       	@ENV.Dflt, --MENU_ENV_ID
       	'CustomerInlineSearchMenuItem', --NAME
       	'/FrameworkDesktop/Skin/ControlPanelImages/sciboodleControlPanelFieldEditorsUp64x64', --IMAGE_PATH
	'/FrameworkDesktop/Skin/ControlPanelImages/sciboodleControlPanelFieldEditorsUp64x64',--IMAGE_PATH_ROLLOVER
       	'inlineSearch', --VERB_NAME
       	@ET.Customer, --ENTITY_DEF_ID
       	@ENV.Dflt, --ENTITY_DEF_ENV_ID
       	'N' --IS_DELETED
);
INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED)
VALUES (
       	'MenuItemED',
	'CustomerInlineSearchMenuItem',
	@MNI.CustomerInlineSearchMenuItem,
	'displayName',
	'en-US',
	'default',
	'Inline Search',
	'N'
);
INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED)
VALUES (
       	'MenuItemED',
	'CustomerInlineSearchMenuItem',
	@MNI.CustomerInlineSearchMenuItem,
	'description',
	'en-US',
	'default',
	'Inline Search Desc',
	'N'
);

