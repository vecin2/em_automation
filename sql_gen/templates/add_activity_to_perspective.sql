{% set tmp = perspective_id | suggest(_keynames.CC) %}
{% set tmp = entity_type | suggest(_keynames.ET) %}
{% set verb_names = _db.list.v_names_by_et(entity_type) %}
{% set tmp = verb_name | suggest(verb_names)%}
{% set perspective_verbs = _db.fetch.v_by_pers_id(perspective_id) %}
{%set seq_no_desc ="All the activities sequence numbers are 1 by default. This shows the activities in alphabetical order.\n"+
		   "Please notice that changing the Context within 'Manage Context' admin screen overrides sequence numbers and set them matching the screen order.\n"
		   "Notice that you local environment configuration might ddiffer from the environment where this script will be released"
		   "Is it ok to display the activities in alphabetical order?(Y/N) (sequence_numbers will be set to 1)?"%}
{% set tmp = is_alphabetical_order | description(seq_no_desc) %}
{% if is_alphabetical_order == "Y"%}
	{% set sequence_number = 1 %}
UPDATE EVA_CONTEXT_VERB_ENTRY
SET SEQUENCE_NUMBER = 1
where CONFIG_ID = @CC.{{perspective_id}};
{% else %}
	{% set seq_no_desc =perspective_verbs.to_str()+"\n"+"In which sequence number should this activity be displayed? (this will increase the higher sequence numbers)"%}
	{% set tmp =sequence_number | description(seq_no_desc) %}
	{% set to_update = perspective_verbs.where("SEQUENCE_NUMBER>="+sequence_number)%}
--updating sequence numbers
	{% for item in to_update %}

UPDATE EVA_CONTEXT_VERB_ENTRY
SET (SEQUENCE_NUMBER) = ({{ item.SEQUENCE_NUMBER + 1 }})
where CONFIG_ID = @CC.{{perspective_id}}
and ENTITY_DEF_TYPE_ID = @ET.{{item.ET_KEYNAME}}
and VERB = '{{item.VERB}}'

	{% endfor %}
{%endif%}

--inserting new activity in specific sequence no
INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) 
VALUES (
	 @CC.{{perspective_id}},--config_id
  	 @ENV.Dflt, --config_env_id
  	 '{{verb_name}}', --verbname
  	 @ET.{{entity_type}}, --entity_type
  	 @ENV.Dflt, --entity_def_type_env_id
  	 {{sequence_number}}, --sequence_number
  	 @RELEASE.ID --release_id
       );
