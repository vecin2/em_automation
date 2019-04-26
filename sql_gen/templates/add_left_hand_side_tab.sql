
{% set pptive_ids = _keynames.PPTIVE %}
{% set temp_pptive_id = perspective_id | suggest(pptive_ids)%}
{% set verb_ids = _keynames.V %}
{% set last_sequence_num = _addb.list.av_topseq_by_entity_id(perspective_id) %}
{% set sequence_desc ="Sequence_no (Last in sequece was "+last_sequence_num[0].__str__()+")"  %}

INSERT INTO FD_ENTITY__AUX_VERBS (ENTITY_ID,ENTITY_ENV_ID,ENTITY_TYPE_ID,ENTITY_TYPE_ENV_ID,AUXILIARY_VERB_ID,SEQUENCE_NUM,RELEASE_ID,TENANT_ID)
VALUES (
	@PPTIVE.{{perspective_id}}, -- entity_id 
	@ENV.Dflt, --entity_env_id
	@ET.Perspective,--entity_type_id
	@ENV.Dflt, --entity_type_env_id
	@V.{{verb_id | suggest(verb_ids)}}, --auxiliary_verb_id
	{{sequence_num | description(sequence_desc)}},--sequence_num
	@RELEASE.ID,--relase_id
	'default' --tenant_id
);

