--["KnowledgeArticle","KnowledgeArticleCreate","KnowledgeArticlePublic","NULL","Y","3","Public Information 2","FieldEditorRichText"]
INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_GROUP (ID,VIEW_ID,GROUP_NAME,RELEASE_ID,TENANT_ID) 
VALUES (@EDEVG.KnowledgeArticleCreateGroupPublicInformation2,@DEV.KnowledgeArticleCreate,'Public Information',1,'default');

INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) 
VALUES (@PDR.FieldEditorRichTextKnowledgeArticlePublic, @PD.FieldEditorRichText, @ENV.Dflt, NULL, 'N');
INSERT INTO EVA_DYNAMIC_ENTITY_VIEW_FIELD (ID, DYN_ENTITY_VIEW_ID, DYN_ENTITY_FIELD_ID, COMPONENT_TYPE_ID, PROCESS_DESC_REF_ID, SHOW_LABEL, VIEW_FIELD_SEQUENCE, GROUP_ID) 
VALUES (
	@EDEVF.KnowledgeArticleCreatePublic, --ID
	@DEV.KnowledgeArticleCreate, --DYN_ENTITY_VIEW_ID
       	@EDEF.KnowledgeArticlePublic, --DYN_ENTITY_FIELD_ID
       	NULL, --COMPONENT_TYPE_ID
       	@PDR.FieldEditorRichTextKnowledgeArticlePublic, --PROCESS_DESC_REF_ID
       	'Y', --SHOW_LABEL
       	3, --VIEW_FIELD_SEQUENCE
       	@EDEVG.KnowledgeArticleCreateGroupPublicInformation2 --GROUP_ID
);
