Analyze the Quantum Safe Mode description from @reference/reference_mode.yaml and compare it with the currently configured qse and qse_remediator modes in the codebase. Identify and document all differences between the reference implementation and the current modes, including any missing features, parameters, descriptions, or configurations. For each identified difference, provide explicit advice on whether it should be added to the current modes and explain the reasoning behind each recommendation. Present findings in a clear, structured format showing: (1) the specific differences found, (2) what is missing from the current modes compared to the reference, and (3) detailed recommendations with justifications for each gap. Do not modify any files or configurations; provide analysis and recommendations only.
Mon Nov 23 20:30:28 CET 2026

# Comparative Analysis: Reference Quantum Safe Mode vs. Current QSE Implementation

## Executive Summary
This document provides a comprehensive architectural and functional comparison between the reference implementation in `reference/reference_mode.yaml` and the current Quantum Safe Explorer (`qse`) configuration in the codebase (`.bob/custom_modes.yaml`, `.bob/skills/qse/`, and `.bob/skills/qse-remediation/`).

The reference implementation follows a **monolithic, fully autonomous model** designed around a single large prompt block that performs mandatory web searches, forces batch fixes across all files without user approval, and relies on automated GitHub PR generation while prohibiting local documentation files.

In contrast, the current codebase implements a **modular, enterprise-grade, skill-driven architecture** combining a lightweight custom mode (`qse`) with two specialized skills (`qse` for scanning/QCM upload and `qse-remediation` with a Python state helper `remediation_tool.py`). The current design prioritizes cryptographic safety, human-in-the-loop approval, state persistence across sessions, behavior-change detection, validation checks, offline air-gapped readiness, and full auditability.

---

## 1. Specific Differences Found

| Dimension | Reference Implementation (`reference_mode.yaml`) | Current Codebase Implementation (`.bob/`) |
| :--- | :--- | :--- |
| **Mode Architecture** | Monolithic: ~450 lines of instructions embedded entirely within `customInstructions` of `custom_modes.yaml`. | Modular: Lightweight mode definition in `custom_modes.yaml` backed by distinct Skills (`qse` and `qse-remediation`). |
| **Mode Identifier (`slug`)** | `slug: quantum-safe` | `slug: qse` |
| **Mode Display Name** | `name: 🔐 Quantum Safe` | `name: 🔐 Quantum Safe Explorer` |
| **Mode Description** | `description: Crypto vulnerability scanner and fixer` | `description: ""` (Currently empty string in `.bob/custom_modes.yaml`). |
| **Tool Groups** | `read`, `edit`, `command`, `mcp` (`command` is non-standard in Bob mode schema). | `read`, `execute`, `mcp`, `edit`, `skill`, `subtask`, `subagent`, `mode` (`execute` is Bob-compliant). |
| **Role Scope** | Broad: Cryptographic security expert covering scanning, web research, automated fixes, post-quantum algorithms, and PR creation. | Scanning-focused in mode `roleDefinition`, while remediation expertise is partitioned into `.bob/skills/qse-remediation/SKILL.md`. |
| **Execution Philosophy** | Fully autonomous ("Assume Full Remediation", do NOT ask user confirmation, fix all files in a single batch PR). | Governed / Human-in-the-loop (Propose fixes with diffs, mandate `ask_followup_question` approval per file, isolate behavior-changing risks). |
| **Remediation Tracking & State** | Stateless within conversation; no on-disk progress tracking. | Stateful & Resume-safe: Dedicated `remediation_tool.py` maintaining `state.json`, `changelog.md`, and `originals/` backups. |
| **Documentation & Summary Files** | Explicitly prohibits markdown summaries (`NO FIXES_SUMMARY.md`, `NO REMEDIATION_SUMMARY.md`). | Generates persistent audit reports (`remediation_report.md`, `changelog.md`, and `task-outcomes/`). |
| **Vulnerability Research** | Mandatory live web search for every finding using MCP search tools (Tavily/web search). | Curated, offline-ready reference knowledge base (`remediation_patterns.md`) covering NIST SP 800-175B, FIPS 203/204/205, OWASP, and CWE mappings. |
| **Supported Languages** | Python, Java, C++, C#, Go. | Java, Go, Python, Dart, C++ (including Java bytecode Cryptographic Analytics vs API Discovery distinction). |
| **Scanner & Cloud Integration** | Assumes user provides findings from VS Code extension panel or JSON. | Direct QSE CLI execution via `cli.sh` with automated exclusion flags (`-ef`), git URL stamping, and IBM Guardium QCM upload via `gcm_api`. |
| **PR & Issue Creation** | References specific tools `submit_review_findings` and `create_pull_request` with a mandatory PR description template. | Local code modifications via `apply_diff` + test validation; git commits and PRs are governed by explicit user requests. |

---

## 2. What is Missing from Current Modes Compared to Reference

1. **Mode-Level Description Parameter**:
   - `reference_mode.yaml` provides a clear single-line description (`Crypto vulnerability scanner and fixer`).
   - `.bob/custom_modes.yaml` currently leaves `description: ""` empty.

2. **Unified Mode Role Definition**:
   - The current mode `roleDefinition` only mentions scanning and CLI construction. It does not mention remediation, PQC migration algorithms (Kyber, Dilithium, etc.), or cryptographic fixing, which are currently only described inside the sub-skills.

3. **Live Web Research Integration**:
   - The reference mandates querying search engines for latest CVEs and standards updates. The current codebase relies on static reference guides (`remediation_patterns.md`) without dynamic web search steps for zero-day/latest CVE intelligence.

4. **GitHub Issue & Pull Request Formatting Templates**:
   - The reference contains detailed markdown templates for batch PR descriptions, categorized research summaries, and issue payloads (`submit_review_findings`). The current codebase does not include PR description templates.

5. **Separate `qse_remediator` Mode**:
   - Neither the reference nor the current codebase defines a separate mode named `qse_remediator`. The current architecture integrates remediation as a skill (`qse-remediation`) accessible under the `qse` mode (which has the `edit` and `skill` permissions).

---

## 3. Detailed Recommendations and Justifications

### Recommendation 1: Populate Mode Description and Update `roleDefinition` in `custom_modes.yaml`
- **Advice**: **ADOPT**
- **Justification**: 
  - Leaving `description: ""` is an omission that degrades UX in the mode selector interface. Setting `description: "Scan codebases for quantum-readiness and remediate cryptographic vulnerabilities with QSE."` provides clarity.
  - Expanding `roleDefinition` to mention remediation, post-quantum cryptography (FIPS 203 ML-KEM, FIPS 204 ML-DSA), and secure coding practices aligns the mode with its full capabilities without bloating the configuration.

### Recommendation 2: Maintain Modular Skill Architecture over Monolithic Mode Instructions
- **Advice**: **RETAIN CURRENT ARCHITECTURE (REJECT MONOLITHIC EMBEDDING)**
- **Justification**:
  - Embedding 450 lines of instructions directly into `custom_modes.yaml` consumes excessive context tokens on every turn regardless of whether the user is scanning, reporting, or remediating.
  - The current skill-based pattern (`.bob/skills/qse/` and `.bob/skills/qse-remediation/`) keeps token consumption minimal and modular, activating instructions only when relevant.

### Recommendation 3: Retain Human-in-the-Loop Approval & Reject "Assume Full Remediation"
- **Advice**: **RETAIN CURRENT APPROVAL GATE (REJECT REFERENCE AUTO-FIX)**
- **Justification**:
  - The reference's instruction ("Do NOT ask for confirmation - Proceed immediately to fix all vulnerabilities") is dangerous for cryptographic code. Cryptographic changes frequently break ciphertext compatibility, change database column lengths, require key rotation, or alter public API signatures.
  - The current approach (propose diffs, flag `BEHAVIOR-CHANGING` impact, require `ask_followup_question` approval, create pristine backups in `originals/`, and run automated test validation) adheres strictly to enterprise security standards and prevents catastrophic production breakage.

### Recommendation 4: Retain On-Disk Persistence and Audit Reporting (`remediation_report.md`)
- **Advice**: **RETAIN CURRENT PERSISTENCE (REJECT REFERENCE NO-MARKDOWN RULE)**
- **Justification**:
  - The reference rule forbidding markdown summaries ("NO FIXES_SUMMARY.md", "NO REMEDIATION_SUMMARY.md") prevents multi-session resumption and eliminates local compliance evidence.
  - The current `remediation_tool.py` maintaining `state.json`, `changelog.md`, and `remediation_report.md` allows security teams to review changes offline, verify before/after unified diffs, and resume interrupted remediation workflows across sessions.

### Recommendation 5: Introduce Optional Web Research as a Secondary Fallback
- **Advice**: **ADAPT / ENHANCE**
- **Justification**:
  - Forcing mandatory web search for *every* finding (as in the reference) fails in air-gapped / enterprise private networks and slows down remediation.
  - However, for novel CVEs or algorithms not covered by `remediation_patterns.md`, allowing dynamic web search using available MCP tools (such as Tavily or Google Search) when online enhances accuracy. The primary guidance should remain the curated offline knowledge base, with web research as a fallback for unknown patterns.

### Recommendation 6: Add PR Description Templates to the Remediation Skill
- **Advice**: **ADAPT / ENHANCE**
- **Justification**:
  - The comprehensive PR description template in `reference_mode.yaml` lines 235–356 is well-structured and beneficial when users request a Git commit/PR.
  - Instead of putting this template into `custom_modes.yaml`, it should be added to `.bob/skills/qse-remediation/` (e.g. as a template helper in `remediation_patterns.md` or a skill step) so that when a user requests "create a PR for these fixes", the assistant formats the PR using this structured template.

### Recommendation 7: Retain Single `qse` Mode with Skills instead of Creating a Separate `qse_remediator` Mode
- **Advice**: **RETAIN SINGLE UNIFIED MODE**
- **Justification**:
  - The current `qse` mode already has `read`, `execute`, `mcp`, `edit`, `skill`, `subtask`, `subagent`, and `mode` tool groups.
  - Maintaining a single unified `qse` mode that switches seamlessly between scanning (`qse` skill) and remediation (`qse-remediation` skill) avoids unnecessary mode switching friction while keeping all capabilities accessible in one workspace environment.
