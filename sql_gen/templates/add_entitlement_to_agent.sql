{% set entitlements = _db.fetch.all_entitlements() %}
{% set entitlement_names = entitlements.column('SYSTEM_NAME') %}
{% set tmp = entitlement_name | suggest(entitlement_names) %}
{% set entitlement = entitlements.find(SYSTEM_NAME=entitlement_name) %}

{% set users = _db.fetch.all_users() %}
{% set usernames = users.column('USERNAME') %}
{% set tmp = username | suggest(usernames) %}
{% set user = users.find(USERNAME=username) %}

INSERT INTO EVA_ENTITY__ENTITLEMENT (ENTITLEMENT_ID, ENTITLEMENT_ENV_ID, ENTITY_ID, ENTITY_ENV_ID, ENTITY_TYPE_ID, ENTITY_TYPE_ENV_ID, IS_DELETED, RELEASEID, TENANT_ID) 
VALUES (
	@ENTLMNT.{{entitlement['KEYNAME']}}, --ENTITLEMENT_ID
	@ENV.Dflt,--ENTITY_ENV_ID
       	{{user['ID']}},
	@ENV.Dflt,--ENTITY_ENV_ID
       	@ET.Agent,
       	@ENV.Dflt,
       	'N',
       	@RELEASE.ID,
       	'default');
