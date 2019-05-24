{% set __perspective_id = perspective_id | suggest(_keynames.CC) %}
{% set __entity_type = entity_type | suggest(_keynames.ET) %}
{% set verb_names = _db.fetch.v_names_by_et(__entity_type).column('NAME') %}
{% set __verb_name = verb_name | suggest(verb_names)%}
{% set perspective_verbs = _db.fetch.v_by_pers_keyname(__perspective_id) %}
{%set seq_no_desc ="All the activities sequence numbers are 1 by default which will display them in alphabetical order. Please notice that changing the Context within 'Manage Context' admin screen overrides sequence numbers"+
				   " and set them matching the screen order.\n"
				   "\nShould we display the activities in alphabetical order?(Y/N)?"%}
{% set __is_alphabetical_order = is_alphabetical_order | print(seq_no_desc) | default('Y') %}
{% if __is_alphabetical_order == "Y"%}
	{% set __sequence_number = 1 %}
--update all sequence_numbers to 1 so they display in alphabetical order
UPDATE EVA_CONTEXT_VERB_ENTRY
SET (SEQUENCE_NUMBER) = (1)
where CONFIG_ID = @CC.{{__perspective_id}};
{% else %}
	{% set seq_no_desc =perspective_verbs.to_str()+"\n"+"In which sequence number should this activity be displayed? (this will increase the higher sequence numbers)"%}
	{% set __sequence_number =sequence_number | description(seq_no_desc) %}
	{% set to_update = perspective_verbs.where("SEQUENCE_NUMBER>="+__sequence_number)%}
--updating sequence numbers
	{% for item in to_update %}

UPDATE EVA_CONTEXT_VERB_ENTRY
SET (SEQUENCE_NUMBER) = ({{ item.SEQUENCE_NUMBER + 1 }})
where CONFIG_ID = @CC.{{__perspective_id}}
and ENTITY_DEF_TYPE_ID = @ET.{{item.ET_KEYNAME}}
and VERB = '{{item.VERB}}';

	{% endfor %}
{%endif%}

--inserting new activity in specific sequence no
INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (
	 @CC.{{__perspective_id}},--config_id
  	 @ENV.Dflt, --config_env_id
  	 '{{__verb_name}}', --verbname
  	 @ET.{{__entity_type}}, --entity_type
  	 @ENV.Dflt, --entity_def_type_env_id
  	 {{__sequence_number}}, --sequence_number
  	 @RELEASE.ID --release_id
       );
