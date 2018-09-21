
INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) 
VALUES (
        @PDR.{{ process_descriptor_ref_id }} --process_descriptor_ref_name,
        @PD.{{ process_descriptor_id }}, --process_descriptor_id
	@ENV.Dflt, --env_id
	NULL, --config_id
       	'N' --is_shared
       );
