--["VerbAudit"]
DELETE FROM EVA_ENTITY_DEFINITION 
WHERE ID = @ED.VerbAudit;

DELETE FROM LOCALISED_FIELD 
WHERE OBJECT_VERSION = @ED.VerbAudit
AND OBJECT_TYPE = 'EntityDefinitionED';