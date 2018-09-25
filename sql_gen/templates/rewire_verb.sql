{# We compute descriptor id #}
{% set process_descriptor_id = prj_prefix()+ entity_def_id.capitalize() + verb_name.capitalize() -%}

{% include 'add_process_descriptor.sql' %}
{% set process_descriptor_ref_id = process_descriptor_id %}
{% include 'add_process_descriptor_ref.sql' %}


UPDATE EVA_VERB 
SET (PROCESS_DESC_REF_ID) = (@PDR.{{process_descriptor_ref_id}})
WHERE ENTITY_DEF_ID = @ED.{{entity_def_id}} AND NAME ='{{verb_name}}';
