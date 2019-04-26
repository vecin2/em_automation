from sql_gen.database.sqlparser import SQLParser
from sql_gen.app_project import AppProject
from sql_gen.database.sqlparser import SQLParser, RelativeIdLoader
import sqlparse


def test_rendering_select_verb_matches_expected_sql():
    expected=("SELECT NAME FROM EVA_VERB;")
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    actual=("SELECT NAME FROM EVA_VERB;")
    actual =sqlparser.parse_assertable_statements(actual)
    assert expected == actual

def test_select_verb_runs_succesfully():
    query=("SELECT NAME FROM EVA_VERB;")
    emprj_path=("/opt/em/projects/Pacificorp/trunk")
    app_project = AppProject(emprj_path=emprj_path)
    sqlparser =SQLParser(RelativeIdLoader())
    app_project.addb.execute(query,sqlparser=sqlparser)

def test_rendering_extend_customer_matches_expected_sql():
    expected=("UPDATE EVA_ENTITY_DEFINITION\n"
	"SET (LOGICAL_OBJ_PATH) = ('GSCCoreEntities.Implementation.Customer.GSCCustomer')\n"
	"WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;\n"
	"\n"
	"UPDATE EVA_ENTITY_DEFINITION\n"
	"SET (INTERFACE_PATH) = ('GSCCoreEntities.API.EIGSCCustomer')\n"
	"WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;")
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    actual=("--No need to create a new entity definition, because  pre-extended \n"
	"--customer object is provided OTB to facilate customer extensions\n"
	"UPDATE EVA_ENTITY_DEFINITION \n"
	"SET (LOGICAL_OBJ_PATH) = ('GSCCoreEntities.Implementation.Customer.GSCCustomer') \n"
	"WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;\n"
	"\n"
	"UPDATE EVA_ENTITY_DEFINITION \n"
	"SET (INTERFACE_PATH) = ('GSCCoreEntities.API.EIGSCCustomer') \n"
	"WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;")
    actual =sqlparser.parse_assertable_statements(actual)
    assert expected == actual

def test_extend_customer_runs_succesfully():
    query=("UPDATE EVA_ENTITY_DEFINITION\n"
	"SET (LOGICAL_OBJ_PATH) = ('GSCCoreEntities.Implementation.Customer.GSCCustomer')\n"
	"WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;\n"
	"\n"
	"UPDATE EVA_ENTITY_DEFINITION\n"
	"SET (INTERFACE_PATH) = ('GSCCoreEntities.API.EIGSCCustomer')\n"
	"WHERE ID = @ED.Customer AND ENV_ID = @ENV.Dflt;")
    emprj_path=("/opt/em/projects/Pacificorp/trunk")
    app_project = AppProject(emprj_path=emprj_path)
    sqlparser =SQLParser(RelativeIdLoader())
    app_project.addb.execute(query,sqlparser=sqlparser)

def test_rendering_rewire_verb_matches_expected_sql():
    expected=("INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE)\n"
	"VALUES (\n"
	"	 @PD.GSC1CustomerIdentifycustomer, @ENV.Dflt, 'GSC1CustomerIdentifycustomer', 'GSC1CoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper', NULL, 'N', 0 );\n"
	"\n"
	"INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED)\n"
	"VALUES (\n"
	"	@PDR.GSC1CustomerIdentifycustomer, @PD.GSC1CustomerIdentifycustomer, @ENV.Dflt, NULL, 'N' );\n"
	"\n"
	"UPDATE EVA_VERB\n"
	"SET (PROCESS_DESC_REF_ID) = (@PDR.GSC1CustomerIdentifycustomer)\n"
	"WHERE ENTITY_DEF_ID = @ED.Customer AND NAME ='identifyCustomer';")
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    actual=("\n"
	"\n"
	"\n"
	"\n"
	"INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) \n"
	"VALUES (\n"
	"	 @PD.GSC1CustomerIdentifycustomer, --id\n"
	"	 @ENV.Dflt, --env_id,\n"
	"	 'GSC1CustomerIdentifycustomer', --process_descriptor_name\n"
	"	 'GSC1CoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper', --repository_path \n"
	"	 NULL, --config_id\n"
	"	 'N', --is_deleted\n"
	"	 0 --type\n"
	"       );\n"
	"\n"
	"INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED) \n"
	"VALUES (\n"
	"        @PDR.GSC1CustomerIdentifycustomer, --id\n"
	"        @PD.GSC1CustomerIdentifycustomer, --process_descriptor_id\n"
	"	@ENV.Dflt, --process_descriptor_env_id\n"
	"	NULL, --config_id\n"
	"       	'N' --is_shared\n"
	"       );\n"
	"\n"
	"UPDATE EVA_VERB \n"
	"SET (PROCESS_DESC_REF_ID) = (@PDR.GSC1CustomerIdentifycustomer)\n"
	"WHERE ENTITY_DEF_ID = @ED.Customer AND NAME ='identifyCustomer';\n"
	"\n"
	"\n"
	"\n"
	"")
    actual =sqlparser.parse_assertable_statements(actual)
    assert expected == actual

def test_rewire_verb_runs_succesfully():
    query=("INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE)\n"
	"VALUES (\n"
	"	 @PD.GSC1CustomerIdentifycustomer, @ENV.Dflt, 'GSC1CustomerIdentifycustomer', 'GSC1CoreEntities.Implementation.Customer.Verbs.IdentifyCustomerWrapper', NULL, 'N', 0 );\n"
	"\n"
	"INSERT INTO EVA_PROCESS_DESC_REFERENCE (ID, PROCESS_DESCRIPTOR_ID, PROCESS_DESCRIPTOR_ENV_ID, CONFIG_ID, IS_SHARED)\n"
	"VALUES (\n"
	"	@PDR.GSC1CustomerIdentifycustomer, @PD.GSC1CustomerIdentifycustomer, @ENV.Dflt, NULL, 'N' );\n"
	"\n"
	"UPDATE EVA_VERB\n"
	"SET (PROCESS_DESC_REF_ID) = (@PDR.GSC1CustomerIdentifycustomer)\n"
	"WHERE ENTITY_DEF_ID = @ED.Customer AND NAME ='identifyCustomer';")
    emprj_path=("/opt/em/projects/Pacificorp/trunk")
    app_project = AppProject(emprj_path=emprj_path)
    sqlparser =SQLParser(RelativeIdLoader())
    app_project.addb.execute(query,sqlparser=sqlparser)

def test_rendering_add_entity_definition_matches_expected_sql():
    expected=("INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, IS_DELETED, IS_BASIC, ICON_PATH, INSTANCE_ICON_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, SUPPORTS_READONLY) VALUES (\n"
	"@ED.Agreement, @ENV.Dflt, 'Agreement', 'Agreement', 'Agreement', @ET.Agreement, @ENV.Dflt, 'PacificorpAccount.Implementation.Objects.Agreement', 'PacificorpAccount.API.EIAgreement', 'N', 'Y', NULL, NULL, @ED.PersistableEntity, @ENV.Dflt, 'Y' );\n"
	"\n"
	"INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (\n"
	"@EC.Pacificorp, @ENV.Dflt, @ED.Agreement, @ENV.Dflt  );\n"
	"\n"
	"INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (\n"
	"'EntityDefinitionED', 'Agreement', @ED.Agreement, 'displayName', 'en-US', 'default', 'Agreement', 'N' );")
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    actual=("INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, IS_DELETED, IS_BASIC, ICON_PATH, INSTANCE_ICON_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, SUPPORTS_READONLY) VALUES (\n"
	"@ED.Agreement, -- ID\n"
	"@ENV.Dflt, -- ENV_ID\n"
	"'Agreement', -- NAME \n"
	"'Agreement', -- UUID \n"
	"'Agreement', -- TYPE_UUID \n"
	"@ET.Agreement, -- TYPE_ID\n"
	"@ENV.Dflt, -- TYPE_ENV_ID\n"
	"'PacificorpAccount.Implementation.Objects.Agreement', -- LOGICAL_OBJECT_PATH\n"
	"'PacificorpAccount.API.EIAgreement', -- INTERFACE_PATH\n"
	"'N', -- IS_DELETED\n"
	"'Y', -- IS_BASIC\n"
	"NULL, -- ICON_PATH\n"
	"NULL, -- INSTANCE_ICON_PATH\n"
	"@ED.PersistableEntity, -- SUPER_ENTITY_DEFINITION\n"
	"@ENV.Dflt, -- SUPER_ENTITY_DEFINITION_ENV_ID\n"
	"'Y' --SUPPORTS_READONLY\n"
	");\n"
	"INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (\n"
	"@EC.Pacificorp, -- CATEGORY_ID\n"
	"@ENV.Dflt, -- CATEGORY_ENV_ID\n"
	"@ED.Agreement, -- ENTITY_ID\n"
	"@ENV.Dflt -- ENTITY_ENV_ID\n"
	");\n"
	"\n"
	"INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (\n"
	"'EntityDefinitionED', -- OBJECT_TYPE\n"
	"'Agreement', -- OBJECT_INSTANCE\n"
	"@ED.Agreement, -- OBJECT_VERSION\n"
	"'displayName', -- FIELD_NAME\n"
	"'en-US', -- LOCALE\n"
	"'default', -- LOOKUP_LOCALE\n"
	"'Agreement', --TEXT\n"
	"'N' --IS_DELETED\n"
	");")
    actual =sqlparser.parse_assertable_statements(actual)
    assert expected == actual

def test_add_entity_definition_runs_succesfully():
    query=("INSERT INTO EVA_ENTITY_DEFINITION (ID, ENV_ID, NAME, UUID, TYPE_UUID, TYPE_ID, TYPE_ENV_ID, LOGICAL_OBJ_PATH, INTERFACE_PATH, IS_DELETED, IS_BASIC, ICON_PATH, INSTANCE_ICON_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID, SUPPORTS_READONLY) VALUES (\n"
	"@ED.Agreement, @ENV.Dflt, 'Agreement', 'Agreement', 'Agreement', @ET.Agreement, @ENV.Dflt, 'PacificorpAccount.Implementation.Objects.Agreement', 'PacificorpAccount.API.EIAgreement', 'N', 'Y', NULL, NULL, @ED.PersistableEntity, @ENV.Dflt, 'Y' );\n"
	"\n"
	"INSERT INTO EVA_CATEGORY_ENTRY(CATEGORY_ID, CATEGORY_ENV_ID, ENTITY_ID, ENTITY_ENV_ID) VALUES (\n"
	"@EC.Pacificorp, @ENV.Dflt, @ED.Agreement, @ENV.Dflt  );\n"
	"\n"
	"INSERT INTO LOCALISED_FIELD (OBJECT_TYPE, OBJECT_INSTANCE, OBJECT_VERSION, FIELD_NAME, LOCALE, LOOKUP_LOCALE,TEXT,IS_DELETED) VALUES (\n"
	"'EntityDefinitionED', 'Agreement', @ED.Agreement, 'displayName', 'en-US', 'default', 'Agreement', 'N' );")
    emprj_path=("/opt/em/projects/Pacificorp/trunk")
    app_project = AppProject(emprj_path=emprj_path)
    sqlparser =SQLParser(RelativeIdLoader())
    app_project.addb.execute(query,sqlparser=sqlparser)

def test_rendering_add_verb_to_context_matches_expected_sql():
    expected=("INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID)\n"
	"VALUES (\n"
	"	 @CC.Home, @ENV.Dflt, 'launchIdentifyPlanMember', @ET.Agent, @ENV.Dflt, 1, @RELEASE.ID  );")
    sqlparser =SQLParser()
    expected =sqlparser.parse_assertable_statements(expected)
    actual=("INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID) \n"
	"VALUES (\n"
	"	 @CC.Home,--config_id\n"
	"  	 @ENV.Dflt, --config_env_id\n"
	"  	 'launchIdentifyPlanMember', --verb_name\n"
	"  	 @ET.Agent, --entity_type\n"
	"  	 @ENV.Dflt, --entity_def_type_env_id\n"
	"  	 1, --sequence_number\n"
	"  	 @RELEASE.ID --release_id\n"
	"       );")
    actual =sqlparser.parse_assertable_statements(actual)
    assert expected == actual

def test_add_verb_to_context_runs_succesfully():
    query=("INSERT INTO EVA_CONTEXT_VERB_ENTRY (CONFIG_ID,CONFIG_ENV_ID,VERB,ENTITY_DEF_TYPE_ID,ENTITY_DEF_TYPE_ENV_ID,SEQUENCE_NUMBER,RELEASE_ID)\n"
	"VALUES (\n"
	"	 @CC.Home, @ENV.Dflt, 'launchIdentifyPlanMember', @ET.Agent, @ENV.Dflt, 1, @RELEASE.ID  );")
    emprj_path=("/opt/em/projects/Pacificorp/trunk")
    app_project = AppProject(emprj_path=emprj_path)
    sqlparser =SQLParser(RelativeIdLoader())
    app_project.addb.execute(query,sqlparser=sqlparser)