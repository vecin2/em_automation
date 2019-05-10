{% set tmp = entity_id | suggest(_keynames.ED) %}
{% set entity_verbs = _db.fetch.verbs_by_ed(entity_id) %}
{% set verb_ids = entity_verbs.column('KEYNAME') %}

DELETE
FROM EVA_VERB
WHERE ID = @V.{{verb_id | suggest(verb_ids)}}
and ENTITY_DEF_ID=@ED.{{entity_id}};


{% set keyset ="V" %}
{% set keyname =verb_id %}
{% include 'hidden_templates/remove_idmap.sql' %}
