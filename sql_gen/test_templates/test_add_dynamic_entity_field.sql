--["KnowledgeArticle","title2","","StringField","1"]
INSERT INTO EVA_DYNAMIC_ENTITY_FIELD (ID, ENTITY_DEF_ID, NAME, INITIAL_VALUE, FIELD_TYPE_ID, FIELD_SEQUENCE, ENTITY_DEF_ENV_ID)
VALUES (@EDEF.KnowledgeArticleTitle2, @ED.KnowledgeArticle, 'title2', '', @EFT.StringField, 1, @ENV.Dflt);

INSERT INTO LOCALISED_FIELD (OBJECT_TYPE,OBJECT_INSTANCE,OBJECT_VERSION,FIELD_NAME,LOCALE,LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES ('DynamicEntityDefinitionED','KnowledgeArticleED',@ED.KnowledgeArticle,'fields.title2.displayName','en-US','default','Title2','N');


