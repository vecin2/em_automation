{% set ed_object_type ="DynamicEntityDefinitionED" %}
{% set logical_object_path ='FrameworkDynamicEntities.Implementation.DynamicEntity.Objects.DynamicEntity' %}
{% set interface_path ='FrameworkDynamicEntities.API.EntityInterfaces.EIDynamicEntity' %}
{% set super_entity_definition ='@ED.BaseDynamicEntity' %}
{% set category_id = "DynamicEntity"%}
{% set is_basic = 'N' %}
{% set supports_readonly = 'Y' %}
{% set is_expandable = 'N' %}

{% include 'hidden_templates/base_add_entity_def.sql' %}

{% set field_name = "summaryExpression" %}
{% set text = summary_expression | description("summary_expression (e.g Article [title])") %}
{% include 'add_localised_field.sql' %}

{% set entity_keyname = entity_id %}
{% include 'add_dynamic_entity_def.sql' %}
