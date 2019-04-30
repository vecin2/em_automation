--["Home","ContactHistoryEntitiyDefinition","searchContactHistory"]
DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.Home
and VERB = 'searchContactHistory'
and ENTITY_DEF_TYPE_ID= @ET.ContactHistoryEntitiyDefinition;

