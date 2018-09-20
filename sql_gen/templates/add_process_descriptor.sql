INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) 
VALUES (@PD.{{ process_descriptor_id }}, --ID
 @ENV.Dflt, --ENV_ID,
 '{{ process_descriptor_id }}', --process_descriptor_name
 '{{ repository_path }}', --repository_path 
 {{ config_id | default('NULL') }} , --config_id
 'N',
 {{ process_descriptor_type |
    description('type_id (0=regular process, 2=action, 3=sla)'|
    default ('0') ) }} --type
);
