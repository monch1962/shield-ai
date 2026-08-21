package shield_ai.ds.agent_originated_artifact_publ

import rego.v1

# SHIELD-AI(TM) DS-07: Agent-Originated Artifact Publication Control
# Pillar: DS -- Data Security
#
# Prevent agents from unintentionally or maliciously publishing execution-bearing artifacts into the software supply chain.
#
# Maturity indicators:
#   L1: Agents can reach publication endpoints with standing credentials; no approval gate.
#   L2: Publication requires human approval; publication credentials reviewed for least privilege.
#   L3: Signed, scanned, provenance-tracked publication pipeline; short-lived scoped credentials; agent cannot self-approve.
#   L4: Continuous monitoring and provenance verification of agent-authored artifacts; automated blocking of unapproved publication paths.
#
# Regulatory mappings:
#   NIST: SSDF
#   ISM: Software Integrity, Change Management
#   OWASP: LLM09 (Misuse of System Access)
#   EU AI Act: Art. 15(b)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Anthropic PyPI
# publication INC-19, Kiro MCP-registry self-write INC-20).
# Input model: input.action.kind == "publication"; input.action.target = the
# distribution channel; input.approval = {"present": bool, "channel": string}.
# Out-of-band approval is one the agent cannot invoke: channel must be a human
# console, never "agent".

deny contains msg if {
    input.action.kind == "publication"
    not input.approval.present
    msg := sprintf("DS-07 deny: agent publication to %q lacks the required out-of-band approval", [input.action.target])
}

deny contains msg if {
    input.action.kind == "publication"
    input.approval.present == true
    input.approval.channel == "agent"
    msg := sprintf("DS-07 deny: publication to %q was approved on the agent channel; out-of-band human approval required", [input.action.target])
}

deny contains msg if {
    input.action.kind == "publication"
    input.action.target == "execution_bearing_config"
    input.approval.present == true
    input.approval.channel != "human_console"
    msg := "DS-07 deny: execution-bearing configuration write requires human-console approval (Kiro class)"
}

allow if {
    count(deny) == 0
}
