{# We set compute descriptor id #}
{% set process_descriptor_id = "GSC"+ entity_def_id  + verb_name%}
{% set query = "SELECT CONFIG_ID FROM EVA_PROCESS_DESCRIPTOR WHERE ENTITY_DEF_ID =" + entity_def_id %}
this is the query  {{query}}
{{ config_id | default (query)}}
{% include 'add_process_descriptor.sql' %}
{% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'add_process_descriptor_ref.sql' %}

update eva_verb 
set (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_id}})
where ENTITY_DEF_ID = @ED.{{entity_def_id}} and name ='{{verb_name}}';
