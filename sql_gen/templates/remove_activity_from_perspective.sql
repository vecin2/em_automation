{% set tmp1 =perspective_id | suggest(_keynames.CC)%}
{% set verbs =_db.fetch.v_by_pers_id(perspective_id)%}
{% set display_names =verbs.column("DISPLAY_NAME")%}
{% set verb_ids =verbs.column("VERB")%}
{% set v_to_remove_desc = "Verbs on perspective:\n"+verbs.to_str()+"\nVerb"%}
{% set tmp2 = verb_name | description(v_to_remove_desc) |suggest(verb_ids) %}
{% set verb_to_remove = verbs.find(VERB=verb_name)%}
DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.{{perspective_id}}
and VERB = '{{verb_to_remove["VERB"]}}'
and ENTITY_DEF_TYPE_ID= @ET.{{verb_to_remove["ET_KEYNAME"]}};

