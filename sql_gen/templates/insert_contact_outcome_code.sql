{% set name = camelcase(display_name)%}
INSERT INTO CCH_OUTCOME_CODE (ID,NAME,RELEASE_ID,IS_USER_VISIBLE,IS_DELETED,IS_SYSTEM_CODE) 
VALUES (@OC.{{name}},'{{name}}',1,'Y','N','N');
INSERT INTO CCH_OUTCOME_CODE_LOC (ID,LOCALE,DISPLAY_NAME,DESCRIPTION,RELEASE_ID) 
VALUES (@OC.{{name}},'{{language | default('en-US')}}','{{display_name}}','{{description}}',1);
