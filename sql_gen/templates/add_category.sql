INSERT INTO EVA_CATEGORY (ID,ENV_ID,PARENT_CATEGORY_ID,PARENT_CATEGORY_ENV_ID,ENTITY_DEF_ID,ENTITY_DEF_ENV_ID,RELEASE_ID,SYSTEM_NAME)
VALUES (
	@EC.{{category_id}}, --ID
	@ENV.Dflt, --ENV_ID
	@EC.{{parent_category_id | suggest(_keynames.EC)}}, --PARENT_CATEGORY_ID
	@ENV.Dflt, --PARENT_CATEGORY_ENV_ID
	@ED.EntityDefinition, --ENTITY_DEF_ID
	@ENV.Dflt, --ENTITY_DEF_ENV_ID
	@RELEASE.ID,
	{% set parent_category = _db.find.category_by_keyname(parent_category_id) %}
	'{{parent_category["SYSTEM_NAME"]+"->"+category_id}}' --SYSTEM_NAME
       );

