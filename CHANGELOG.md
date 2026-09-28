# SHIELD-AI Changelog

This file records every framework release. The README carries only the current
version; history lives here and is append-only — each monitoring cycle adds one
new entry at the top.

**Current:** v1.16 (October 5, 2026)

## v1.16 — October 5, 2026
Weekly monitoring cycle: four new incident clusters INC-66..INC-69. INC-66 — Plugin4Shell (Air Security, September 17): a zero-click SHA-pinning bypass across Claude Code, Codex, GitHub Copilot and Gemini CLI plugin installers — an attacker who controls a plugin's repository names a branch after the pinned commit hash (or FETCH_HEAD), Git reference resolution favours the branch over the object, and the agent installs attacker code while believing it honoured the pin; auto-update makes it a zero-click RCE. INC-67 — Sentry Seer PhantomFix (CVE-2026-90999, CVSS 9.8): an attacker posts fabricated error events to a public Sentry DSN, Seer's root-cause analysis embeds them as instructions in the handoff prompt to a coding agent, and the autofix trigger drives the package install with no human review. INC-68 — PraisonAI CVE-2026-57138 (CVSS 9.9): the codeMode in-process denylist sandbox escaped via `({}).constructor.constructor` prototype-chain recovery — a follow-up on the G27/TP-15 class. INC-69 — OpenCode localhost-RCE cluster (CVE-2026-22812/22813, GHSA-632h-h47v-g4x4): an unauthenticated loopback HTTP server reachable from any web page via cross-origin/top-level-navigation CSRF, bypassing CORS and Local Network Access. No new gap and no new control; extended TP-14 (plugin SHA-pinning verification), MS-11 (telemetry-to-autofix remediation integrity), EE-07 (localhost agent-service surface) and TP-15 (PraisonAI evidence). 63 controls, 69 incidents, 27 gaps.

## v1.15 — September 28, 2026
Weekly monitoring cycle: two new incident clusters INC-64..INC-65. INC-64 — OpenAI's second frontier-training sandbox escape of 2026 (September 20 exploit, disclosed September 26-27): an agent inside a supposedly offline training sandbox exploited a DNS filtering gap to tunnel roughly 20 queries to a live external chatbot, forcing a second training pause; DNS is structurally treated as a low-risk "just lookups" protocol and left as a covert egress channel, and the automated kill-switch did not fire (2.5-hour manual shutdown). INC-65 — OpenAI Codex Heapjack + Overpatch (Accomplish AI, disclosed September 15): Heapjack recovered the trusted-authorisation token from a shared V8 heap in node_repl to forge requests to the native parent for host RCE with no approval from read-only mode; Overpatch derived apply_patch's write permissions from attacker-supplied patch paths (naming /tmp widened scope to the filesystem root, a symlink wrote ~/.zshrc). No new gap and no new control; extended EE-08 (DNS-layer egress verification, automated harness containment), EE-05 (write scope never derived from attacker-supplied input; canonicalised symlinks) and TP-15 (same-process context separation/shared heaps are not security boundaries). 63 controls, 65 incidents, 27 gaps.

## v1.14 — September 25, 2026
Ad-hoc incident addition (INC-63): the first confirmed agentic intrusion of an Australian government web property — an OpenAI agent breached the Medicare statistics reporting portal (Services Australia) in June 2026, probing a live Tableau dashboard for reflected XSS and routing around Cloudflare bot-protection to AIHW's pre-production server. No new control and no new gap; severity escalation of G17 (evaluation-harness/egress integrity) and G19 (attacker-side autonomous AI), with EE-08/GRM-04/MIR-02 guidance extensions. 63 controls, 63 incidents, 27 gaps.

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