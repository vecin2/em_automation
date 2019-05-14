--creates an agent with the same password as 'admin' user
INSERT INTO FU_USER (ID, USERNAME, LOCALE_ID, LOCALE_ENV_ID, IS_DELETED, VIRTUAL_ENVIRONMENT_ID, VIRTUAL_ENVIRONMENT_ENV_ID, TENANT_ID, CONTENT_LOCALE) VALUES (@USER.{{username}}, '{{username}}', @LOC.en_US, 666, 'N', 1, 666, 'default', '{{_locale}}');

INSERT INTO FD_USER_PROFILE_TYPE (TENANT_ID, USER_ID, PROFILE_TYPE_ID, PROFILE_TYPE_ENV_ID, IS_DELETED) VALUES ('default', @USER.{{username}}, @PROFILE.{{profile_id | suggest(_keynames.PROFILE)}}, 666, 'N');

INSERT INTO CE_PERSON (ID, FIRST_NAME, FIRST_NAME_UPPER, LAST_NAME, LAST_NAME_UPPER, GENDER_ID, GENDER_ENV_ID, TITLE_ID, TITLE_ENV_ID, IS_DELETED, TENANT_ID, DO_NOT_DELETE) VALUES (@USER.{{username}}, '{{name}}', '{{name | upper()}}', '{{surname}}', '{{surname | upper()}}', 0, 666, 0, 666, 'N', 'default', 'N');

INSERT INTO CE_AGENT (ID, USER_ID, TENANT_ID, ORG_REALM_ID) VALUES (@USER.{{username}}, @USER.{{username}}, 'default', 'organisat');

INSERT INTO AGENT (USERNAME,PASSWORD,FULLNAME,EXPIRES,PERSON_ID,CONNECTON,DISABLED,GRACE,CREATED,ALLOWCONCURRENT,CONSISTENTIPONLY,LOGINFAILURES,LASTLOGGEDIN,SALT,ENCRYPTION_CLASSNAME,EXTERNALLY_AUTHENTICATED,TENANT_ID) 
VALUES ('{{username}}','0ef489f','{{name}} {{surname}}',TO_DATE('12/15/2075','MM/DD/YYYY'),@USER.{{username}},1,'no',0,TO_DATE('12/15/2015','MM/DD/YYYY'),1,'no',0,CURRENT_DATE,'wkhvmgQLLhY=','com.gtnet.common.security.algorithms.SHA256','no','default');

{% set username_to_copy_from = "admin" %}
{% include 'update_agent_password.sql' %}

--INSERT INTO DIM_AGENT (TENANT_ID, ID, USERNAME, FIRST_NAME, LAST_NAME, PARENT_AGENT_ID) VALUES ('default', 2, 'ccdev', 'Mark', 'Johson', 1000000).
