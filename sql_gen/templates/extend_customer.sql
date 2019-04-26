--No need to create a new entity definition, because  pre-extended 
--customer object is provided OTB to facilate customer extensions
UPDATE EVA_ENTITY_DEFINITION 
SET (LOGICAL_OBJ_PATH) = ('{{logical_object_path}}') 
WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;

UPDATE EVA_ENTITY_DEFINITION 
SET (INTERFACE_PATH) = ('{{interface_path}}') 
WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;
