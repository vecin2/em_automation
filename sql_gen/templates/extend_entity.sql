{#
To extend entity we create a new "Base" entity pointing to the OTB  object and interface.
Then we update the OTB entity to point to our extended object
and to inherit from the new created entity
#}

{{ base_entity_id | description("Entity name you would like to extend(e.g CustomerED)") | suggest(_keynames.ED)}}
{% set base_entity = _db.find.ed_by_id(base_entity_id) %}
{% set entity_name = "Base"+base_entity_name %}
{{ interface_path | description("Interface path you would like to override (e.g. CoreEntities.API.Interfaces.EICustomer)")}}
{{ object_path | description("Logical object path you would like to override(e.g CoreEntities.Implementation.Customer.Customer):")}}
{{ entity_id | description("Child entity_id, (e.g. SPENCustomer):")}}

{%include 'add_entity_definition.sql' %}

{{ child_interface_path | description("Child interface path, (e.g.e.g. SPENCustomer.API.EISPENCustomer):")}}
{{ child_object_path | description("Child logical object path, (e.g.e.g. SPENCustomer.Implementation.Customer.Objects.SpenCustomer):")}}


UPDATE EVA_ENTITY_DEFINITION 
SET (LOGICAL_OBJ_PATH, INTERFACE_PATH, SUPER_ENTITY_DEFINITION, SUPER_ENTITY_DEFINITION_ENV_ID) = ('{{child_object_path}}', '{{child_interface_path}}', @ED.{{entity_id}}, @ENV.Dflt) WHERE NAME = '{{base_entity_name}}' AND ENV_ID = @ENV.Dflt and RELEASE_ID = @RELEASE.ID;

