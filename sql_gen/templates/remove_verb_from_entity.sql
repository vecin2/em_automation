{% set tmp = entity_id | suggest(_keynames.ED) %}
{% set entity_verbs = _db.fetch.verbs_by_ed(entity_id) %}
{% set verb_ids = entity_verbs.column('KEYNAME') %}

DELETE
FROM EVA_VERB
WHERE ID = @V.{{verb_id | suggest(verb_ids)}}
and ENTITY_DEF_ID=@ED.{{entity_id}};


DELETE
FROM CCADMIN_IDMAP
WHERE KEYSET = 'V'
AND ID =@V.{{verb_id}};
