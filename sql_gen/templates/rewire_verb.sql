{#
SELECT V.* FROM EVA_PROCESS_DESCRIPTOR PD, 
EVA_VERB V,
EVA_PROCESS_DESC_REFERENCE PDR
WHERE 
V.PROCESS_DESC_REF_ID = PDR.ID
AND PDR.PROCESS_DESCRIPTOR_ID = PD.ID
AND V.ENTITY_DEF_ID = 850
AND V.NAME = 'inlineSearch'
#}
{# We set compute descriptor id #}
{% set process_descriptor_id = "GSC"+ entity_def_id  + verb_name%}
{% include 'add_process_descriptor.sql' %}
{% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'add_process_descriptor_ref.sql' %}


UPDATE EVA_VERB 
SET (process_desc_ref_id) = (@PDR.{{PROCESS_DESCRIPTOR_ID}})
WHERE ENTITY_DEF_ID = @ED.{{entity_def_id}} AND NAME ='{{verb_name}}';
