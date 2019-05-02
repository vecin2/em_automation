{% set tmp1 =perspective_id | suggest(_keynames.CC)%}
{% set verb_displaynames =_db.list.v_displaynames_by_pers_id(perspective_id)%}

{% set tmp2 = display_name_to_remove | suggest(verb_displaynames) %}
{% set verb_to_remove = _db.find.verb_by_pers_id_and_display_name(perspective_id,display_name_to_remove) %}
DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.{{perspective_id}}
and VERB = '{{verb_to_remove["NAME"]}}'
and ENTITY_DEF_TYPE_ID= {{verb_to_remove["TYPE_ID"]}};

