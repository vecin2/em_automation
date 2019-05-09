{% set tmp = entity_id | suggest(_keynames.ED) %}
{% set entity_verbs = _db.fetch.verbs_by_ed(entity_id) %}
{% set verb_names = entity_verbs.column('NAME') %}
{% set tmp = verb_name | suggest(verb_names) %}
{% set verb =  entity_verbs.find(NAME=verb_name) %}
DELETE
FROM EVA_VERB
WHERE NAME='{{verb_name}}'
and ENTITY_DEF_ID=@ED.{{entity_id}};


DELETE
FROM CCADMIN_IDMAP
WHERE KEYSET = 'V'
AND ID =@V.{{verb["KEYNAME"]}};
