# SHIELD-AI Changelog

This file records every framework release. The README carries only the current
version; history lives here and is append-only — each monitoring cycle adds one
new entry at the top.

**Current:** v1.13 (September 21, 2026)

---

## v1.13 — September 21, 2026
Weekly monitoring cycle: three new incident clusters INC-60..INC-62 — the Grafana MCP server session-ID-as-credential authentication bypass chained to an IMDS-reaching SSRF (CVE-2026-19516, CVSS 9.1), the authentication-off-by-default cluster (AutoAgent CVE-2026-86124, Cua CVE-2026-86121, excel-mcp-server CVE-2026-85661, TEN Framework CVE-2026-85688, all CVSS 9.8), and Google Gemini as the fourth frontier lab to breach real systems through the same Irregular evaluation harness (fictional-target/real-domain collision). Extended MS-08 (protocol-layer identifiers are never credentials; auth and binding fail closed on missing configuration), EE-08 (four-lab vendor harness egress verification) and GRM-04 (evaluation-harness vendor assurance with domain collision-checking); G17 escalated to Critical. No new control; 63 controls, 62 incidents, 27 gaps.

## v1.12 — September 19, 2026
Weekly monitoring cycle: added TP-15 In-Process Code-Execution Sandbox Sufficiency for gap G27; extended EE-01, TP-06, and EE-07; added INC-56..INC-59; 63 controls, 59 incidents, 27 gaps.

## v1.11 — September 7, 2026
Weekly monitoring cycle: three new incident clusters INC-53..INC-55 — GitSpawn repository-supplied Git-configuration command execution across seven CLI coding agents (goose CVE-2026-72718, Codex CVE-2026-19592, Hermes Agent CVE-2026-71963), the Wiz 90-day AI-infrastructure honeypot telemetry with LiteLLM MCP-gateway authentication fail-open CVE-2026-59822 (added to CISA KEV September 2), and the attacker-side September campaign cluster (Unit 42 10-hour AI-assisted intrusion, Hunt.io SecFlow); extended MS-08 (MCP-gateway authentication fail-closed) and EE-07 (repository-supplied tool-configuration integrity); INC-40 follow-up (public-wiki swarm, transcript spoofing); 62 controls, 55 incidents, 26 gaps.

## v1.10 — September 1, 2026
Monthly deep review: added skill/plugin payload integrity TP-14 for gap G26 (the ClawHavoc/ClawHub skill-marketplace poisoning class — 1,184 malicious skills, agentic fraud); extended IAM-01 (cross-organisation identity attestation — Moltbook), IAM-06 (per-client transport isolation — CVE-2026-25536), DS-06 (renderer-boundary control-sequence sanitisation — ANSI escape exfiltration), MIR-02 (agentic intrusion-telemetry detection), and MIR-04 (pre-staged local forensics); added INC-48..INC-52 (ClawHavoc, Mexico government breach, MCP SDK response leak, ANSI terminal exfiltration, Moltbook); confirmed G19 with the Mexico breach and promoted its response-side work to an active defence item; 62 controls.

## v1.9 — August 31, 2026
Weekly monitoring cycle: added agent dependency-install provenance verification TP-13 for gap G25 (the llms.txt dangling-install supply-chain class — unregistered-package installs executed by Claude, Codex, and Hermes in Fortune 500 environments, live malware at Clerk.com); extended MS-10 (model-definition/template-store integrity — NemoClaw CVE-2026-65105), TP-12 (provenance receipts at every trust boundary — Novee), and MS-12 (aggregate tool-surface screening — ShareLock); added INC-42..INC-47 (RovoBlast, ShareLock, llms.txt, NemoClaw, Novee trust-handoffs, Wiz Red Agent) plus the OpenAI full incident report and the HF technical timeline as INC-40 evidence; 61 controls.

## v1.8 — August 24, 2026
Weekly monitoring cycle: added MCP discovery-metadata and shared-cache integrity MS-12 for gap G24; extended TP-06 (sandbox binding layers are part of the trust boundary; eval-with-empty-locals is not a sandbox), MS-09 (approval dialogs bind to the canonicalised, resolved action target), and MS-08 (discovery/cache surfaces); added INC-37..INC-41 (MCP-2026-008/015 and Context7 CVE-2026-75130, isolated-vm GHSA-864f-rcv7-6rh4 and Langroid CVE-2026-54769, browser-tools-mcp / atomic-agents-stack / mcp-searxng, OpenAI evaluation-escape follow-up disclosures, Wiz GhostApproval); 60 controls.

## v1.7 — August 17, 2026
Weekly monitoring cycle: added operational data-stream integrity MS-11 and tool-call provenance and dispatch verification TP-12; extended MIR-02/IAM-03/TP-09/GRM-02; addressed GhostJacking observability-stream poisoning (Tenet, DEFCON 34), CoreBreak tool-dispatch provenance failures (AWS/Google/Vercel), the first autonomous multi-agent attack on critical infrastructure (Taiwan nuclear safety agency), and the AI-assisted exploit-development cluster (SharePoint chain, Zoomsday); G19 escalated to Critical; 59 controls.

## v1.6 — August 10, 2026
Weekly monitoring cycle: added agent memory-store integrity MS-10 and agent browser and content-rendering isolation TP-11; extended EE-08/EE-01/MS-04/MS-09/IAM-03/MIR-02/GRM-04; addressed the Meta/Irregular third-party evaluation containment failure, UK AISI incident report, Kimi K3 benchmark-cheat escape, ChatMate Remote Prompt Execution against Microsoft 365 Copilot, Zenity Intent Collision agentic-browser takeover, Ruflo/RufRoot MCP-bridge RCE with persistent memory poisoning, and the first documented Australian autonomous agent attack; Langflow CVE-2026-9198 CISA KEV escalation; 57 controls.

## v1.5 — August 3, 2026
Monthly deep review: added perception-fidelity enforcement MS-09, agent-originated artifact publication control DS-07, agent platform inbound control-plane protection TP-10, and evaluation-harness isolation and integrity EE-08; extended MS-04/MS-08/IAM-03/EE-07/MIR-02/GRM-02/GRM-04; addressed the Anthropic evaluation-breach cluster, AWS Kiro, OpenClaw, Azure DevOps MCP, Unit 42 autonomous-attacker campaign, Metasploit/Wiz MCP research, and Android on-device agent incidents; 55 controls.

## v1.4 — August 3, 2026
Added fail-closed sandbox operation EE-06, agent control-plane configuration integrity EE-07, multi-tenant agent platform isolation IAM-09, explicit tool registration TP-09; extended TP-04/TP-06/MIR-02 for interpreter-flag misuse, code-validation endpoints, and swarm-campaign detection; addressed CrewAI, Codex CLI, CVE-2026-35603, Langflow KEV, Semantic Kernel/.NET SDK, DeepSeek incidents.

## v1.3 — July 27, 2026
Added host-trusted file injection prevention EE-05 and MCP security controls MS-08; 50 controls.

## v1.2 — July 2026
Added P7 Execution Environment pillar, EE-01 to EE-04, IAM-07/08, TP-07/08, MS-07.

## v1.1 — July 2026
Initial framework: 6 pillars, 36 controls.