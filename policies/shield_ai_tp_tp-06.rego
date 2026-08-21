package shield_ai.tp.dependency_scanning

import rego.v1

# SHIELD-AI(TM) TP-06: Dependency Scanning
# Pillar: TP -- Tool and Pipeline Security
#
# Continuously scan all ML libraries, model dependencies, tool SDKs, and container images for vulnerabilities with automated blocking of critical-severity findings.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (DeepSeek python_exec
# INC-18, Langflow validate_code INC-16).
# Input model: input.dependencies = {"scanned": bool, "critical_finding": bool,
# "critical_blocked": bool, "sandbox_library": bool, "alternative_approved": bool}.
# Interpreter isolation flags are never security boundaries; code-validation
# endpoints are code-execution surfaces (see EE-06 and TP-04 respectively).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "deployment"
    not input.dependencies.scanned
    msg := "TP-06 deny: deployment with unscanned dependencies"
}

deny contains msg if {
    input.dependencies.critical_finding == true
    not input.dependencies.critical_blocked
    msg := "TP-06 deny: critical-severity dependency finding not blocked"
}

deny contains msg if {
    input.dependencies.sandbox_library == true
    input.dependencies.critical_finding == true
    not input.dependencies.alternative_approved
    msg := "TP-06 deny: HIGH-RISK sandbox library (vm2/n8n/Pyodide/Wasmtime class) with critical finding and no approved alternative"
}

allow if {
    count(deny) == 0
}
