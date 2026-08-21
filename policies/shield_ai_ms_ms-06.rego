package shield_ai.ms.model_inventory_and_lineage_tr

import rego.v1

# SHIELD-AI(TM) MS-06: Model Inventory and Lineage Tracking
# Pillar: MS -- Model Security
#
# Maintain a complete, versioned inventory of all models with traceable lineage from training through deployment to retirement.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.model.inventory = {"registered": bool, "lineage_tracked": bool,
# "versioned": bool}. Fail closed: an unregistered model is not deployable.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "model_deploy"
    not input.model.inventory.registered
    msg := sprintf("MS-06 deny: model %q not registered in the model inventory", [input.model.id])
}

deny contains msg if {
    input.action.kind == "model_deploy"
    not input.model.inventory.lineage_tracked
    msg := sprintf("MS-06 deny: model %q has no traceable lineage", [input.model.id])
}

deny contains msg if {
    input.action.kind == "model_deploy"
    not input.model.inventory.versioned
    msg := sprintf("MS-06 deny: model %q has no version record", [input.model.id])
}

allow if {
    count(deny) == 0
}
