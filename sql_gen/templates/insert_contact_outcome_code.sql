{% set name = camelcase(display_name)%}
INSERT INTO CCH_OUTCOME_CODE (ID,NAME,RELEASE_ID,IS_USER_VISIBLE,IS_DELETED,IS_SYSTEM_CODE) 
VALUES (
	@OC.{{name}}, --id
	'{{name}}', --name
	 1, --release_id
	'Y',-- is_user_visible
	'N',-- is_deleted
	'N' -- is_system_code
       );

INSERT INTO CCH_OUTCOME_CODE_LOC (ID,LOCALE,DISPLAY_NAME,DESCRIPTION,RELEASE_ID) 
VALUES (@OC.{{name}},--id
	'{{locale | default('en-US')}}', --locale
	'{{display_name}}', --display_name
	'{{description}}', --description
	 1 --release_id
       );
