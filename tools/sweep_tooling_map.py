#!/usr/bin/env python3
# v1.6 sweep (HISTORICAL, superseded by the v1.7 cycle): tooling-map count/version updates
# The v1.7 cycle applied its changes directly; patterns below are inert (old strings no longer present).
path = 'framework/shield-ai-tooling-map.md'
with open(path) as f:
    data = f.read()

repls = [
    ('Tools and Processes to Address All 55 Controls, Assessed with Six Thinking Hats',
     'Tools and Processes to Address All 57 Controls, Assessed with Six Thinking Hats'),
    ('(v1.5, 55 controls across 7 pillars)', '(v1.6, 57 controls across 7 pillars)'),
    ('maps every one of the 55 SHIELD-AI controls', 'maps every one of the 57 SHIELD-AI controls'),
    ('- **Seven controls have no mature commercial tool** and require custom or emerging implementation: MS-07 (deployment-context obfuscation), MS-09 (perception-fidelity enforcement), DS-07 (artifact publication control), TP-07 (cross-tool dependency analysis), TP-10 (inbound control-plane protection), EE-07 (control-plane configuration integrity), and EE-08 (evaluation-harness isolation). The SHIELD-AI reference implementation exists precisely to cover these.',
     '- **Nine controls have no mature commercial tool** and require custom or emerging implementation: MS-07 (deployment-context obfuscation), MS-09 (perception-fidelity enforcement), MS-10 (agent memory-store integrity), DS-07 (artifact publication control), TP-07 (cross-tool dependency analysis), TP-10 (inbound control-plane protection), TP-11 (agent browser and content-rendering isolation), EE-07 (control-plane configuration integrity), and EE-08 (evaluation-harness isolation). The SHIELD-AI reference implementation exists precisely to cover these.'),
    ('covering all 55 controls is in Part A', 'covering all 57 controls is in Part A'),
    ('# Part A: Control-to-Tool Mapping (All 55 Controls)', '# Part A: Control-to-Tool Mapping (All 57 Controls)'),
    ('## A1. Model Security (MS-01 .. MS-09)', '## A1. Model Security (MS-01 .. MS-10)'),
    ('| MS-09 Perception-fidelity enforcement | P12 (custom workflow) + T7 (partial) | Snapshot-binding of approvals; emerging; custom |',
     '| MS-09 Perception-fidelity enforcement | P12 (custom workflow) + T7 (partial) | Snapshot-binding of approvals; emerging; custom |\n| MS-10 Agent memory-store integrity | T15 vector DB access control + T18 observability + T20 audit | Memory-write audit, tamper-evident stores, retrieval filtering; mature via composition |'),
    ('## A4. Tool and Pipeline Security (TP-01 .. TP-10)', '## A4. Tool and Pipeline Security (TP-01 .. TP-11)'),
    ('| TP-10 Inbound control-plane protection | T26 IaC security + T11 + custom binding policy | Emerging; network-binding deny defaults |',
     '| TP-10 Inbound control-plane protection | T26 IaC security + T11 + custom binding policy | Emerging; network-binding deny defaults |\n| TP-11 Browser/content-rendering isolation | T7 (partial) + custom rendering-layer controls | No mature tool; hidden-content scanning + origin-isolation policy, custom |'),
    ('| Mature mainstream tooling | 44 of 55 |', '| Mature mainstream tooling | 45 of 57 |'),
    ('| Custom / process-only | 7 | MS-07, MS-09, DS-07 (workflow), TP-07, TP-10, EE-07, EE-08 |',
     '| Custom / process-only | 8 | MS-07, MS-09, DS-07 (workflow), TP-07, TP-10, TP-11, EE-07, EE-08 |'),
    ('- **EE-08 Evaluation-harness isolation**: attestation + active egress verification, fail-closed (P10 + T25)\n\nThese seven are exactly the controls',
     '- **EE-08 Evaluation-harness isolation**: attestation + active egress verification, fail-closed (P10 + T25)\n- **TP-11 Agent browser/content-rendering isolation**: hidden-content scanning on rendered pages and documents (T7 partial) plus custom origin-isolation policy; no mature tool\n\nThese eight are exactly the controls'),
    ('the SHIELD-AI reference implementation already uses it for its 55 controls',
     'the SHIELD-AI reference implementation already uses it for its 57 controls'),
]

count = 0
for old, new in repls:
    n = data.count(old)
    if n == 0:
        print(f'MISSING: {old[:75]}')
        continue
    data = data.replace(old, new)
    count += n
    print(f'ok ({n}x): {old[:75]}')

with open(path, 'w') as f:
    f.write(data)
print('total:', count)
