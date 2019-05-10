DELETE
FROM EVA_ENTITY_DEFINITION
WHERE ID = @ED.{{entity_id | suggest(_keynames.ED)}};

DELETE
FROM LOCALISED_FIELD
WHERE OBJECT_VERSION = @ED.{{entity_id}}
AND OBJECT_TYPE = 'EntityDefinitionED';

{% set keyset ="ED" %}
{% set keyname =entity_id %}
{% include 'hidden_templates/remove_idmap.sql' %}
