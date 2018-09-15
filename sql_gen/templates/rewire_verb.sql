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
{#{{ config_id | ad_run_query (query)}} #}
{#{{ set old_pd = find_pd_by_verb_name_and_path(verb_name,repository_path)}} #}
{#{{ type_id | default(old_pd=pd['TYPE_ID'}}) #}


{# We set compute descriptor id #}
{% set process_descriptor_id = "GSC"+ entity_def_id  + verb_name%}
{% include 'add_process_descriptor.sql' %}
{% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'add_process_descriptor_ref.sql' %}

update eva_verb 
set (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_id}})
where ENTITY_DEF_ID = @ED.{{entity_def_id}} and name ='{{verb_name}}';
