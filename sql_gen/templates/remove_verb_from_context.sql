DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.{{config_id | description("config_id (e.g. Home, CustomerPostIdentify, Customer)")}}
and VERB = '{{verb_name}}'
and ENTITY_DEF_TYPE_ID= @ET.{{customer_type}};
