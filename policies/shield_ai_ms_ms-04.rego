package shield_ai.ms.adversarial_robustness

import rego.v1

# SHIELD-AI(TM) MS-04: Adversarial Robustness
# Pillar: MS -- Model Security
#
# Test and verify that models resist prompt injection, jailbreaking, and other adversarial inputs through automated testing, red-teaming, and proxy-layer guardrails.
#
# Maturity indicators:
#   L1: No adversarial testing. Models deployed based on functional tests only.
#   L2: Basic prompt injection test suite run manually before major deployments.
#   L3: Automated adversarial test suite in CI/CD. Quarterly red-teaming. Output guardrails at proxy layer.
#   L4: Continuous automated red-teaming. Real-time adversarial input detection and blocking. Coverage against MITRE ATLAS.
#
# Regulatory mappings:
#   OWASP LLM Top 10 v2: LLM01 (Prompt Injection), LLM05 (Jailbreak)
#   NIST AI RMF: MEASURE (ME.AD)
#   EU AI Act: Art. 15 -- Accuracy
#   MITRE ATLAS: AML.T0051, AML.T0059
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.context.content[] = agent-visible content the action is
# driven by. Deny-override semantics: allow == (count(deny) == 0), fail closed.

# Deployment-defined marker set. Extend per organisation; covers the documented
# prompt-injection primitives (INC-03/09/13/29) and the imperceptible-content
# primitives that defeat human-in-the-loop perception (INC-20/25/30).
injection_markers := {
    "ignore previous instructions",
    "ignore all prior instructions",
    "disregard your instructions",
    "you are now",
    "system prompt:",
    "new system prompt",
    "color:#fff;font-size:1px",
    "font-size:0px",
    "opacity:0",
}

deny contains msg if {
    some item in input.context.content
    some marker in injection_markers
    contains(item, marker)
    msg := sprintf("MS-04 deny: prompt-injection or imperceptible-content marker %q found in agent-visible content", [marker])
}

allow if {
    count(deny) == 0
}
