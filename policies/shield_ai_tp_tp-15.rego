package shield_ai.tp.in_process_code_execution_sandbox_sufficiency

import rego.v1

# SHIELD-AI(TM) TP-15: In-Process Code-Execution Sandbox Sufficiency
# Pillar: TP -- Tool and Pipeline Security
#
# Route all LLM-generated or untrusted code execution to an OS/VM-isolated execution environment; never rely on an in-process denylist/blocklist interpreter gate as the boundary.
#
# Maturity indicators:
#   L1: Agent frameworks run LLM-generated code in an in-process denylist/blocklist sandbox as the sole containment; host code-execution primitives reachable.
#   L2: Code-execution tools identified and routed to an OS/VM-level sandbox (EE-01); in-process gates flagged and scheduled for replacement.
#   L3: In-process sandboxes locked in the HIGH-RISK dependency class (TP-06) with automated blocking on critical findings; model-generated code executes only in the EE sandbox.
#   L4: No in-process gate deployed for untrusted code; all model-generated execution is OS/VM-isolated with provenance receipts (TP-12); red-teamed object-graph bypass attempts in CI.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for Software Development, Application Control

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-58 PraisonAI,
# CrewAI denylist escapes; INC-68 PraisonAI CVE-2026-57138 object-graph bypass;
# INC-77 VTCode token-blocklist bypass; INC-91 CPython/Jinja template escape).
# Input model: input.action.kind == "code_execution". LLM-generated or untrusted
# code must execute in an OS/VM-isolated boundary; an in-process denylist gate as
# sole containment, or a same-process context sharing memory, is a deny.

deny contains msg if {
    input.action.kind == "code_execution"
    input.action.code.sandboxed_os_vm == false
    msg := sprintf("TP-15 deny: code execution by agent %q runs LLM-generated/untrusted code outside an OS/VM-isolated boundary", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "code_execution"
    input.action.code.in_process_gate_sole_containment == true
    msg := sprintf("TP-15 deny: code execution by agent %q relies on an in-process denylist/blocklist gate as the sole containment; structurally bypassable", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "code_execution"
    input.action.code.shared_memory_context == true
    msg := sprintf("TP-15 deny: code execution by agent %q separates trust by an in-process context that shares a memory heap; not a security boundary (Codex Heapjack class)", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "code_execution"
    input.action.code.in_process_gate_high_risk_unblocked == true
    msg := sprintf("TP-15 deny: code execution by agent %q uses an in-process sandbox not treated as the HIGH-RISK dependency class with blocking on critical findings", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "code_execution"
    input.action.code.template_engine == true
    input.action.code.template_render_isolated == false
    msg := sprintf("TP-15 deny: code execution by agent %q runs a chat-template/rendering-template engine as a code surface without EE-01-grade render isolation (CPython/Jinja template-escape class)", [input.agent.id])
}

allow if {
    count(deny) == 0
}