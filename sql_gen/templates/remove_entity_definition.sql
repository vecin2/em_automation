DELETE 
FROM EVA_ENTITY_DEFINITION 
WHERE ID = @ED.{{entity_id}};

DELETE 
FROM LOCALISED_FIELD 
WHERE OBJECT_VERSION = @ED.{{entity_id}} 
AND OBJECT_TYPE = 'EntityDefinitionED';