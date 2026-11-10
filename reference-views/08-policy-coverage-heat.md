# 08 · Policy Coverage Heatmap

How deep is each control's executable verification? A glanceable grid of implementation status, deny-rule depth, and incident evidence per control, derived from the committed policies and incident catalogue so it stays current with the sources.

![Policy coverage heatmap](../assets/diagrams/policy-coverage-heat.svg)

## Verification depth by pillar

| Pillar | Controls | Implemented | Deny rules | Incident refs |
|---|---|---|---|---|
| **EE** | 8 | 8 | 18 | 173 |
| **MS** | 15 | 15 | 48 | 236 |
| **IAM** | 10 | 10 | 24 | 68 |
| **DS** | 8 | 8 | 24 | 32 |
| **TP** | 16 | 16 | 57 | 289 |
| **MIR** | 6 | 6 | 10 | 75 |
| **GRM** | 6 | 6 | 14 | 39 |

## Reading the heat

- **Implementation status** - `IMPL` is an executable policy; `stub` is declared but not yet enforced.
- **Deny rules** - how many fail-closed conditions the policy enforces.
- **Incidents** - how many catalogue events evidence the control class; intensity shades cool (low) to hot (high).
