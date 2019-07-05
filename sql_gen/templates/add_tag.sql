INSERT INTO eva_tag (ID,ENV_ID,RELEASE_ID,TAGSET_ID,TAGSET_ENV_ID,TAGSET_RELEASE_ID,PARENT_TAG,PARENT_TAG_ENV_ID,PARENT_TAG_RELEASE_ID,PREVIOUS_TAG,PREVIOUS_TAG_ENV_ID,PREVIOUS_TAG_RELEASE_ID,NAME,IS_SYSTEM,IS_DELETED,IS_RETIRED,EXPAND_DIRECTION,CREATED_DATE,LAST_MODIFIED_DATE,LEFT_VAL,RIGHT_VAL,DEPTH_VAL,DISPLAY_ORDER,SYSTEM_CODE) 
VALUES (@TAG.{{tag_name | print("Enter only the name, e.g article, faq")}}, --ID
	@ENV.Dflt, --ENV_ID
	@RELEASE.ID, --RELEASE_ID
	@TAG.{{tagset_keyname | suggest(_keynames.TAG)}}, -- TAGSET_ID
	@ENV.Dflt,-- TAGSET_ENV_ID
	@RELEASE.ID,-- TAGSET_RELEASE_ID
	@TAG.{{parent_tag_keyname | suggest(_keynames.TAG)}},--PARENT_TAG_ID
	@ENV.Dflt,--PARENT_TAG_ENV_ID
	@RELEASE.ID,--PARENT_TAG_RELEASE_ID
	{{previous_tag | suggest(_keynames.FULL_TAG)}},--PREVIOUS_TAG
	@ENV.Dflt,--PREVIOUS_TAG_ENV_ID
	@RELEASE.ID,--PREVIOUS_TAG_RELEASE_ID
	'content_{{tag_name}}', --NAME
	'N', --IS_SYSTEM
	'N',--IS_DELETED
	'N',--IS_RETIRED
	null,--EXPAND_DIRECTION
	sysdate, -- created
	sysdate, --LAST_MODIFIED
	{% set previous_tags = _db.fetch.tags_by_parent_keyname(parent_tag_keyname) %}
	{% set default_left_val = previous_tags | length *2 + 1%}
	{% set __left_val = left_val |default(default_left_val)%} 
	{{__left_val}}, --LEFT_VAL
	{% set default_right_val = __left_val |int +1 %}
	{% set __right_val =right_val | default(default_right_val)%}
	{{__right_val}}, --RIGHT_VAL
	{{depth_val | print("depth_val is 1 if it is direct child of the tagset. 2 if it is a child of top level child, and so on.")}}, --DEPTH_VAL
	null, -- DISPLAY_ORDER
	'content_{{tag_name}}' --SYSTEM_CODE
);
update eva_tag
{%set default_parent_right_val =__right_val| int +1 %}
set (RIGHT_VAL)=({{parent_right_val | default(default_parent_right_val)}})
where id =@TAG.{{parent_tag_keyname}};

INSERT INTO eva_tag_loc (ID,ENV_ID,RELEASE_ID,LOCALE,DESCRIPTION,ICON_URI,REPORTING_LABEL) 
VALUES (@TAG.{{tag_name}},--id
	   @ENV.Dflt,--env_id
	   @RELEASE.ID,--release_id
	   '{{_locale}}',--locale
	   '{{tag_description | default(tag_name)}}',--description
	   null,--icon_uri
	   '{{tag_name}}' --reporting_label
);
INSERT INTO EVA_TAG_DISPLAY_NAME (ID,ENV_ID,RELEASE_ID,DISPLAY_NAME_TYPE_ID,DISPLAY_NAME_TYPE_ENV_ID,DISPLAY_NAME_TYPE_RELEASE_ID)
VALUES (@TAG.{{tag_name}},--id
	   @ENV.Dflt,--env_id
	   @RELEASE.ID,--release_id
	   {% set __display_name_type_id =display_name_type_id | default(1) %}
	   {{__display_name_type_id}},--display_name_type_id
	   @ENV.Dflt, --display_name_type_env_id
	   @RELEASE.ID--display_name_type_release_id
);

INSERT INTO EVA_TAG_DISPLAY_NAME_LOC (ID,ENV_ID,RELEASE_ID,LOCALE,DISPLAY_NAME,DISPLAY_NAME_TYPE_ID,DISPLAY_NAME_TYPE_ENV_ID,DISPLAY_NAME_TYPE_RELEASE_ID)
VALUES (@TAG.{{tag_name}},--id
	   @ENV.Dflt,--env_id
	   @RELEASE.ID,--release_id
	   '{{_locale}}',--locale
	   '{{tag_name}}',--display_name
	   {{__display_name_type_id}}, --display_name_type_id
	   @ENV.Dflt,--display_name_type_env_id
	   @RELEASE.ID--display_name_type_release_id
);
