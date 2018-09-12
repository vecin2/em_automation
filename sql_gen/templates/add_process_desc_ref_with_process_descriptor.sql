{% include 'add_process_descriptor.sql' %}

{% set process_descriptor_ref_id = process_descriptor_id %}
INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) 
VALUES (@PDR.{{ process_descriptor_ref_id }}, @PD.{{ process_descriptor_id }}, @ENV.Dflt, NULL, 'N');
