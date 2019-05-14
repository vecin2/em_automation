{% set __perspective_id =perspective_id | suggest(_keynames.CC)%}
{% set verbs =_db.fetch.v_by_pers_keyname(__perspective_id)%}
{% set verb_display_names =verbs.column("VERB")%}
{% set v_to_remove_desc = "Verbs on perspective:\n"+verbs | string()+"\nEnter the verb name you want to remove"%}
{% set __verb_name_to_remove = verb_name_to_remove | description(v_to_remove_desc) |suggest(verb_display_names) %}
{% set verbs_to_remove = verbs.where(VERB=__verb_name_to_remove)%}

{% if verbs_to_remove | length ==1 %}
	{% set verb_to_remove = verbs_to_remove | first%}

{% else %}
	{% set entity_names = verbs_to_remove.column("ET_KEYNAME")%}
	{% set __entity_name = entity_name | suggest(entity_names)%}
	{% set verb_to_remove = verbs_to_remove.find(ET_KEYNAME=__entity_name) %}
{% endif %}

--remove activity from perspecive
DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.{{__perspective_id}}
and VERB = '{{verb_to_remove["VERB"]}}'
and ENTITY_DEF_TYPE_ID= @ET.{{verb_to_remove["ET_KEYNAME"]}};

{% set to_update = verbs.where("SEQUENCE_NUMBER >"+
			        verb_to_remove["SEQUENCE_NUMBER"] | string)%}

{% if to_update | length >0 %}
--updating sequence numbers
{% for item in to_update %}
UPDATE EVA_CONTEXT_VERB_ENTRY
SET SEQUENCE_NUMBER = {{ item.SEQUENCE_NUMBER - 1 }}
where CONFIG_ID = @CC.{{__perspective_id}}
and ENTITY_DEF_TYPE_ID = @ET.{{item.ET_KEYNAME}}
and VERB = '{{item.VERB}}'
{% endfor %}
{% endif %}
