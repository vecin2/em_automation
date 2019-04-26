--['GSCCoreEntities.Implementation.Customer.GSCCustomer','GSCCoreEntities.API.EIGSCCustomer']
UPDATE EVA_ENTITY_DEFINITION
SET (LOGICAL_OBJ_PATH) = ('GSCCoreEntities.Implementation.Customer.GSCCustomer')
WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;

UPDATE EVA_ENTITY_DEFINITION
SET (INTERFACE_PATH) = ('GSCCoreEntities.API.EIGSCCustomer')
WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;
