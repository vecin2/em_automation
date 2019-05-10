{% set tmp =perspective_id | suggest(_keynames.CC)%}
{% set verbs =_db.fetch.v_by_pers_id(perspective_id)%}
{% set verb_display_names =verbs.column("VERB")%}
{% set v_to_remove_desc = "Verbs on perspective:\n"+verbs | string()+"\nEnter the verb name you want to remove"%}
{% set tmp = verb_name_to_remove | description(v_to_remove_desc) |suggest(verb_display_names) %}
{% set verbs_to_remove = verbs.where(VERB=verb_name_to_remove)%}

{% if verbs_to_remove | length ==1 %}
	{% set verb_to_remove = verbs_to_remove | first%}

{% else %}
	{% set entity_names = verbs_to_remove.column("ET_KEYNAME")%}
	{% set tmp = entity_name | suggest(entity_names)%}
	{% set verb_to_remove = verbs_to_remove | first%}
{% endif %}

--remove activity from perspecive
DELETE FROM EVA_CONTEXT_VERB_ENTRY
where CONFIG_ID = @CC.{{perspective_id}}
and VERB = '{{verb_to_remove["VERB"]}}'
and ENTITY_DEF_TYPE_ID= @ET.{{verb_to_remove["ET_KEYNAME"]}};

{% set to_update = verbs.where("SEQUENCE_NUMBER >"+
			        verb_to_remove["SEQUENCE_NUMBER"] | string)%}


--updating sequence numbers
{% for item in to_update %}
UPDATE EVA_CONTEXT_VERB_ENTRY
SET SEQUENCE_NUMBER = {{ item.SEQUENCE_NUMBER - 1 }}
where CONFIG_ID = @CC.{{perspective_id}}
and ENTITY_DEF_TYPE_ID = @ET.{{item.ET_KEYNAME}}
and VERB = '{{item.VERB}}'

{% endfor %}
