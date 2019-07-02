{%set system_name = __system_name | description("system_name (by conventionfinishes in 'ED', e.g KnowledgeArticleED)")%}
{% set content_type_keyname = system_name | replace("Knowledge","") | replace("ED","") %}
INSERT INTO AKCB_CONTENT_TYPE (ID,ENV_ID,RELEASE_ID,SYSTEM_NAME,DEFAULT_CATEGORY_NAME,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,RELATIVE_URL,IS_DELETED,PREFIX,TENANT_ID) 
VALUES (@AKCBCT.{{content_type_keyname}}, --ID
	@ENV.Dflt, --ENV_ID
	@RELEASE.ID, --RELEASE_ID
	'{{system_name | description("system_name (by conventionfinishes in 'ED', e.g KnowledgeArticleED)")}}',--SYSTEM_NAME
	'{{default_category_name | description("default_category_name (e.g content_article)")}}', --DEFAULT_CATEGORY_NAME
	@ED.Content,--ENTITY_DEF_TYPE_ID
	@ENV.Dflt, --ENTITY_DEF_TYPE_ENV_ID
	'live.kana.com?:ws/', --RELATIVE_URL
	'N',--IS_DELETED
	'{{prefix | description("Prefix to be used for the Content Type") | default("KM")}}',--PREFIX
	'default'--TENANT_ID
);
INSERT INTO AKCB_CONTENT_TYPE_LOC (ID,ENV_ID,RELEASE_ID,LOCALE,DISPLAY_NAME,DESCRIPTION,TENANT_ID)
VALUES (@AKCBCT.{{content_type_keyname}}, --ID
	@ENV.Dflt, --ENV_ID
	@RELEASE.ID, --RELEASE_ID
	'{{locale | default(_locale)}}',
	'{{display_name | default(content_type_keyname)}}',
	'{{description | default(content_type_keyname)}}',
	'default');

INSERT INTO AKCB_CONTENT_CATEGORY (ID,ENV_ID,RELEASE_ID,SYSTEM_NAME,SMALL_ICON_CLASS,LARGE_ICON_CLASS,ICON_CLASS,TENANT_ID)
VALUES (@AKCBCC.{{content_type_keyname}}, --ID
	@ENV.Dflt, --ENV_ID
	@RELEASE.ID, --RELEASE_ID
	'{{default_category_name}}', --SYSTEM_NAME
	{% set __category_css_class = category_css_class | default(content_type_keyname) %}
	'knowledgeCategoryIcon iconSmall icon{{__category_css_class}}', --SMALL_ICON_CLASS
	'knowledgeCategoryIcon iconLarge icon{{__category_css_class}}', --LARGE_ICON_CLASS
	'tabIcon{{__category_css_class}}',--ICON_CLASS
	'default');

INSERT INTO AKI_INDEX_CONTENT_TYPE (ID,ENV_ID,TYPE_NAME,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,RELEASE_ID,TENANT_ID) 
VALUES (@AKIT.{{system_name}},
	@ENV.Dflt, --ENV_ID
	'{{system_name}}',--TYPE_NAME
	@ED.ContentAuthoringWorkItem,
	@ENV.Dflt, --ENTITY_DEF_TYPE_ENV_ID
	@RELEASE.ID, --RELEASE_ID
	'default');


