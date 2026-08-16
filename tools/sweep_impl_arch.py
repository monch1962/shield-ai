#!/usr/bin/env python3
# v1.6 sweep (HISTORICAL, superseded by the v1.7 cycle): implementation-architecture count/range updates
# The v1.7 cycle applied its changes directly; patterns below are inert (old strings no longer present).
path = 'framework/shield-ai-implementation-architecture.md'
with open(path) as f:
    data = f.read()

repls = [
    ('realise the 55 controls across 7 pillars', 'realise the 57 controls across 7 pillars'),
    ('seven security pillars and 55 controls', 'seven security pillars and 57 controls'),
    ('mapping matrix for all 55 controls', 'mapping matrix for all 57 controls'),
    ('defined subset of the 55 controls', 'defined subset of the 57 controls'),
    ('MS-01..MS-09', 'MS-01..MS-10'),
    ('TP-01..TP-10', 'TP-01..TP-11'),
    ('continuously tests the 55 controls', 'continuously tests the 57 controls'),
    ('all 55 controls have shipped stubs (v1.5)', 'all 57 controls have shipped stubs (v1.6)'),
    ('| MS-09 Perception-fidelity enforcement | 2, 6 | IAM-09 Multi-tenant isolation | 3 |',
     '| MS-09 Perception-fidelity enforcement | 2, 6 | IAM-09 Multi-tenant isolation | 3 |\n| MS-10 Agent memory-store integrity | 4 | | | |'),
    ('| | | TP-10 Inbound control-plane protection | 1, 5 |',
     '| | | TP-10 Inbound control-plane protection | 1, 5 |\n| | | TP-11 Browser/content-rendering isolation | 1, 5 |'),
    ('| MS | MS-01..MS-10 | Model security controls (incl. perception-fidelity enforcement MS-09) |',
     '| MS | MS-01..MS-10 | Model security controls (incl. perception-fidelity MS-09, memory-store integrity MS-10) |'),
    ('| TP | TP-01..TP-11 | Tool and pipeline controls (incl. inbound control-plane protection TP-10) |',
     '| TP | TP-01..TP-11 | Tool and pipeline controls (incl. inbound control-plane protection TP-10, browser/content-rendering isolation TP-11) |'),
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
print('total replacements:', count)
