--["KnowledgeArticle","KnowledgeArticleCreate","KnowledgeArticlePublic","Y","3","Public Information 2","en-US","KnowledgeArticleCreatePublic2","process","FieldEditorRichText","Y"]
INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_GROUP (ID,VIEW_ID,GROUP_NAME,RELEASE_ID)
VALUES (@EDEVG.KnowledgeArticleCreateGroupPublicInformation2,@DEV.KnowledgeArticleCreate,'Public Information 2',@RELEASE.ID);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE,OBJECT_INSTANCE,OBJECT_VERSION,FIELD_NAME,LOCALE,LOOKUP_LOCALE,TEXT,LONG_TEXT,LAST_MODIFIED,IS_DELETED) VALUES (
	'DynamicEntityDefinitionED',
	'KnowledgeArticleED',
	@ED.KnowledgeArticle,
	'views.Create.groups.PublicInformation2.displayGroupName',
	'en-US',
	'default',
	'Public Information 2',
	null,
	null,
	'N');

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED)
VALUES (@PDR.FieldEditorRichTextCreateKnowledgeArticlePublic, @PD.FieldEditorRichText, @ENV.Dflt, NULL, 'N');
INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_FIELD (ID, DYN_ENTITY_VIEW_ID, DYN_ENTITY_FIELD_ID, COMPONENT_TYPE_ID, PROCESS_DESC_REF_ID, SHOW_LABEL, IS_MANDATORY, VIEW_FIELD_SEQUENCE, GROUP_ID)
VALUES (
	@EDEVF.KnowledgeArticleCreatePublic2, --ID
	@DEV.KnowledgeArticleCreate, --DYN_ENTITY_VIEW_ID
       	@EDEF.KnowledgeArticlePublic, --DYN_ENTITY_FIELD_ID
       	NULL, --COMPONENT_TYPE_ID
       	@PDR.FieldEditorRichTextCreateKnowledgeArticlePublic, --PROCESS_DESC_REF_ID
       	'Y', --SHOW_LABEL
	'Y', --IS_MANDATORY
       	3, --VIEW_FIELD_SEQUENCE
       	@EDEVG.KnowledgeArticleCreateGroupPublicInformation2 --GROUP_ID
);
