{% set tmp = entity_type | suggest(_keynames.ET) %}
{% set verb_names = _db.list.v_names_by_et(entity_type) %}
DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.{{perspective_id | suggest(_keynames.CC)}}
and VERB = '{{verb_name | suggest(verb_names)}}'
and ENTITY_DEF_TYPE_ID= @ET.{{entity_type | suggest(_keynames.ET)}};

