#!/usr/bin/env python3
import re

path = 'assessment-guide/shield-ai-assessment-guide.md'
with open(path) as f:
    lines = f.readlines()

start = None
for i, l in enumerate(lines):
    if l.startswith('| # | Control |'):
        start = i
        break
assert start is not None, 'header not found'

# Collect data rows: stop at first non-table line after the separator
rows = []
j = start + 1
while j < len(lines) and lines[j].startswith('|--'):
    j += 1
while j < len(lines) and lines[j].startswith('| '):
    rows.append(j)
    j += 1
table_end = j

# Extract control id per row (e.g. MS-10 from "| 10 | MS-10: Agent memory-store integrity | ? |")
def ctrl_id(l):
    m = re.search(r'\|\s*\d+\s*\|\s*((?:MS|IAM|DS|TP|MIR|GRM|EE)-\d+)', l)
    return m.group(1) if m else None

ids = [ctrl_id(lines[r]) for r in rows]
print('before:', len(rows), 'ids:', ids[:5], '...', ids[-3:])

# Dedupe keeping first occurrence, preserving order
seen = set()
clean = []
for r, cid in zip(rows, ids):
    if cid is None:
        continue
    if cid in seen:
        print('  dropping duplicate row:', lines[r].strip())
        continue
    seen.add(cid)
    clean.append((r, cid))

print('after dedupe:', len(clean))
# Verify exactly 57
assert len(clean) == 57, f'expected 57 controls, got {len(clean)}'
expected = [f'{p}-{i:02d}' for p, n in [('MS',10),('IAM',9),('DS',7),('TP',11),('MIR',6),('GRM',6),('EE',8)]
            for i in range(1, n+1)]
actual = [c for _, c in clean]
assert actual == expected, f'order mismatch: {actual}'

# Renumber
for num, (r, cid) in enumerate(clean, start=1):
    lines[r] = re.sub(r'^\|\s*\d+\s*\|', f'| {num} |', lines[r], count=1)

# Drop any leftover duplicate rows (rows in `rows` not in clean)
keep_rows = {r for r, _ in clean}
new_lines = []
for idx, l in enumerate(lines):
    if idx in rows and idx not in keep_rows:
        continue  # drop duplicate
    new_lines.append(l)

with open(path, 'w') as f:
    f.writelines(new_lines)

print('final rows:', len(clean))
