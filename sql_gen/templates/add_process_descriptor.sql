INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) 
VALUES (
	 @PD.{{ process_descriptor_id }}, --id
	 @ENV.Dflt, --env_id,
	 '{{ process_descriptor_id }}', --process_descriptor_name
	 '{{ repository_path | codepath() | replace(".xml","") }}', --repository_path 
	 {{ config_id | default('NULL') }}, --config_id
	 'N', --is_deleted
	 {{ process_descriptor_type |
	    description('type_id (0=regular process, 2=action, 3=sla)')|
	    default ('0') }} --type
       );


INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'{{process_descriptor_id}}__{{repository_path | replace(".","/")}}', -- OBJECT_INSTANCE
@PD.{{process_descriptor_id}}, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'{{_locale}}', -- LOCALE
'default', -- LOOKUP_LOCALE
'{{process_descriptor_id}}', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'{{process_descriptor_id}}__{{repository_path | replace(".","/")}}', -- OBJECT_INSTANCE
@PD.{{process_descriptor_id}}, -- OBJECT_VERSION
'description', -- FIELD_NAME
'{{_locale}}', -- LOCALE
'default', -- LOOKUP_LOCALE
'{{process_descriptor_id}}', -- TEXT
'N'
);
