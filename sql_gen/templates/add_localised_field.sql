INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (
'{{object_type}}', -- OBJECT_TYPE
'{{object_instance}}', -- OBJECT_INSTANCE
{{object_version}}, -- OBJECT_VERSION
'{{field_name}}', -- FIELD_NAME
'{{locale | default(_locale)}}', -- LOCALE
'default', -- LOOKUP_LOCALE
'{{display_name}}', --TEXT
'N' --IS_DELETED
);
