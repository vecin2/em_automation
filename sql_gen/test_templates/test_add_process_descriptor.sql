--["PRJsearchBasicCustomer","Customer.Process.SearchBasicCustomer","NULL","0","en-US"]
INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE)
VALUES (
         @PD.PRJsearchBasicCustomer, --id
         @ENV.Dflt, --env_id,
         'PRJsearchBasicCustomer', --process_descriptor_name
         'Customer.Process.SearchBasicCustomer', --repository_path
         NULL, --config_id
         'N', --is_deleted
         0 --type
       );


INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'PRJsearchBasicCustomer__Customer/Process/SearchBasicCustomer', -- OBJECT_INSTANCE
@PD.PRJsearchBasicCustomer, -- OBJECT_VERSION
'displayName', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'PRJsearchBasicCustomer', -- TEXT
'N'
);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'ProcessDescriptorED', -- OBJECT_TYPE
'PRJsearchBasicCustomer__Customer/Process/SearchBasicCustomer', -- OBJECT_INSTANCE
@PD.PRJsearchBasicCustomer, -- OBJECT_VERSION
'description', -- FIELD_NAME
'en-US', -- LOCALE
'default', -- LOOKUP_LOCALE
'PRJsearchBasicCustomer', -- TEXT
'N'
);
