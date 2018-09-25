UPDATE EVA_CONTEXT_VERB_ENTRY
SET (CONFIG_ID)= (@CC.{{new_config_id | description("new_config_id (e.g. Home, CustomerPostIdentify, Customer)")}})
where CONFIG_ID = @CC.{{old_config_id}}
and VERB = '{{verb_name}}';

