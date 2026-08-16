#!/usr/bin/env python3
# v1.6 sweep (HISTORICAL, superseded by the v1.7 cycle): README count/version updates
# The v1.7 cycle applied its changes directly; patterns below are inert (old strings no longer present).
path = 'README.md'
with open(path) as f:
    data = f.read()

v15_line = '**v1.5** -- August 3, 2026 (monthly deep review: added perception-fidelity enforcement MS-09, agent-originated artifact publication control DS-07, agent platform inbound control-plane protection TP-10, and evaluation-harness isolation and integrity EE-08; extended MS-04/MS-08/IAM-03/EE-07/MIR-02/GRM-02/GRM-04; addressed the Anthropic evaluation-breach cluster, AWS Kiro, OpenClaw, Azure DevOps MCP, Unit 42 autonomous-attacker campaign, Metasploit/Wiz MCP research, and Android on-device agent incidents; 55 controls)'
v16_line = v15_line + '\n\n**v1.6** -- August 10, 2026 (weekly monitoring cycle: added agent memory-store integrity MS-10 and agent browser and content-rendering isolation TP-11; extended EE-08/EE-01/MS-04/MS-09/IAM-03/MIR-02/GRM-04; addressed the Meta/Irregular third-party evaluation containment failure, UK AISI incident report, Kimi K3 benchmark-cheat escape, ChatMate Remote Prompt Execution against Microsoft 365 Copilot, Zenity Intent Collision agentic-browser takeover, Ruflo/RufRoot MCP-bridge RCE with persistent memory poisoning, and the first documented Australian autonomous agent attack; Langflow CVE-2026-9198 CISA KEV escalation; 57 controls)'

repls = [
    ('#   Full framework (v1.5)', '#   Full framework (v1.6)'),
    ('#   Sandbox escape gap analysis (v1.5)', '#   Sandbox escape gap analysis (v1.6)'),
    ('#   Full guide, all 7 pillars x 55 controls', '#   Full guide, all 7 pillars x 57 controls'),
    ('#   55 machine-readable control stubs', '#   57 machine-readable control stubs'),
    ('# Machine-readable control definitions (v1.5)', '# Machine-readable control definitions (v1.6)'),
    ('- **55 Controls** across all pillars', '- **57 Controls** across all pillars'),
    ('incident research driving framework evolution (v1.5, 25 incidents, 19 gaps)',
     'incident research driving framework evolution (v1.6, 32 incidents, 21 gaps)'),
    ('tools and processes addressing all 55 controls', 'tools and processes addressing all 57 controls'),
    (v15_line, v16_line),
]

count = 0
for old, new in repls:
    n = data.count(old)
    if n == 0:
        print(f'MISSING: {old[:70]}')
        continue
    data = data.replace(old, new)
    count += n
    print(f'ok ({n}x): {old[:70]}')

with open(path, 'w') as f:
    f.write(data)
print('total:', count)
