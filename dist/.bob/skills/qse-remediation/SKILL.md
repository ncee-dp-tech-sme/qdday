---
name: qse-remediation
description: Use when the user wants to remediate, fix, or migrate away from quantum-vulnerable cryptography reported by a Quantum Safe Explorer (QSE) scan — reads qs_explorer_result findings JSON, proposes per-file fixes, applies them only after user approval, keeps a change log, and produces a remediation report with before/after evidence.
---

# QSE Remediation

Turns QSE findings into reviewed, documented code changes. All progress is persisted under
`qs_explorer_result/remediation/` so work can stop and resume across sessions and the final report is complete.

## Ground rules
- **Never edit code without explicit user approval** of that specific proposal (`ask_followup_question`).
- **Preserve behavior.** If a fix inherently changes behavior (output format, key size, ciphertext/digest compatibility, dependency), label it **BEHAVIOR-CHANGING** in the proposal and explain the migration impact. Prefer a compatible alternative when one exists.
- **Evidence only.** Base every claim on the finding JSON and the code you actually read. Do not invent APIs; verify a library/version exists and is maintained before proposing it.
- **Explicit Consent for Web Research (Recommendation 5):** Never make web searches or external API calls silently. Before executing any web research for novel algorithms or standards updates, Bob **MUST** prompt the user via `ask_followup_question`, explicitly display what search query will be executed, which public sources will be accessed, the justification for the research, and a guarantee that no proprietary source code or secrets will be transmitted. Proceed **only** upon affirmative user consent.
- **Tool availability.** The `qse` mode includes `edit` and `execute` groups by default. If running in a mode without edit capabilities, ask the user (`ask_followup_question`) to switch to `qse` or `agent` mode. State is persisted on disk in `qs_explorer_result/remediation/`, so nothing is lost across mode switches.
- Helper: `.bob/skills/qse-remediation/remediation_tool.py` (Python 3 stdlib only). Run it from the workspace root as `python3 .bob/skills/qse-remediation/remediation_tool.py <cmd>`. Abbreviated below as `TOOL`.

## Workflow

1. **Load findings (resume-safe).** Run `TOOL init`. It looks in `qs_explorer_result/` for
   `quantum_safe_cryptography_analysis_findings_<LANG>.json` and/or `quantum_safe_api_discovery_findings.json`
   (language comes from the filename or from the `file_type` field), parses every artifact with
   `crypto_vulnerabilities`, groups them per source file, assigns stable ids (`F-001`…), and writes `state.json`.
   Re-running `init` keeps existing statuses, so use it (or `TOOL status`) to resume. If no file is found, stop and
   suggest running the `qse` scan skill first. Show the user `TOOL status` output (files, findings, severities).
2. **Process one file at a time**, highest severity first. For a file run `TOOL show --file <path>`
   (finding details + numbered source context), then read the whole file with `read_file`.
3. **Analyze in context** for each finding:
   - Confirm the code at the reported line still matches the finding. If it already differs (stale scan or
      already fixed), say so, propose `skipped` with reason, and recommend a rescan.
   - Determine purpose (password hashing? integrity check? data at rest? key exchange? signing?), what depends on
      it (stored data, other modules, tests, external peers), and whether it is test code.
   - Findings with no vulnerability entries are informational; mention them but only propose changes if the
      code is clearly unsafe, and flag that as outside the scan evidence.
   - Several vulnerabilities on one line (e.g. CWE-327 + CWE-328) get **one** combined fix.
4. **Research & guidance (Offline-first, Permission-Gated Web Search fallback):**
   - **Primary (Offline):** Check `.bob/skills/qse-remediation/references/remediation_patterns.md` for standard NIST/OWASP patterns and algorithm replacements.
   - **Secondary (Permission-gated Web Research - Recommendation 5):** If a finding involves an unlisted algorithm, novel CVE, or ambiguous guidance:
     1. Formulate a sanitized query containing only the public algorithm/standard name (e.g., `"FIPS 203 ML-KEM migration guide"`, `"NIST SP 800-175B SHA-1 deprecation"`). **NEVER** include repository paths, codebase logic, or proprietary identifiers in search queries.
     2. Prompt the user for explicit consent via `ask_followup_question`:
        - **Question:** State what needs to be researched, why, and display the exact search query and target domains (e.g., NIST CSRC, OWASP).
        - **Data disclosure:** Explicitly confirm that *no proprietary code or secrets are sent*.
        - **Options:**
          - `[A] Approve web research with specified query: <query>`
          - `[B] Skip web research and use best-effort offline pattern`
          - `[C] Provide custom replacement instructions manually`
     3. **Execution Gate:** Execute web research **only** if Option A is selected. If denied or skipped, proceed with best-effort offline patterns.
5. **Propose, then ask.** For each file present: finding ids, vulnerability (CWE, severity, scanner message), exact proposed diff, why it addresses the vulnerability, what behavior stays the same, what changes (BEHAVIOR-CHANGING items, new dependencies, migration needs), and risks. Then `ask_followup_question` with options: apply all for this file / apply selected / skip / defer / modify proposal. Record decisions that are not "apply" immediately:
   `TOOL record --ids F-002,F-003 --status skipped|rejected|deferred --summary "<reason>"`.
6. **Apply approved changes only.**
   1. `TOOL backup --file <path>` (pristine copy, taken once, before the first edit).
   2. Edit with `apply_diff`. Above every modified block add a comment (in the file's comment syntax, use
      `date` for the timestamp) containing: `QSE remediation <finding ids>`; **Vulnerability** (CWE + message);
      **Change** (what was changed); **Rationale**; **Notes** (security considerations, compatibility,
      migration, follow-ups). Keep it factual and compact.
   3. `TOOL record --ids <ids> --status applied --summary "<one-line description of the change>"`
      (this also appends to `changelog.md` and stores the post-change hash).
7. **Validate functionality** after each file: run what exists — syntax/compile check, linter, unit tests
   (use the project `.venv`/`venv` for Python if present; otherwise ask the user), and a focused check of the
   changed behavior where feasible. Record every run:
   `TOOL record-validation --file <path> --command "<cmd>" --exit-code <n> --summary "<result>"`.
   If validation fails, show the user, propose a fix or revert (restore from `remediation/originals/<path>`), and
   record the outcome. Never claim functionality is intact without a recorded validation or an explicit statement
   that none could be run.
8. **Next file** until `TOOL status` shows no `pending` findings with vulnerabilities (deferred/skipped are
   acceptable if recorded with reasons).
9. **Report & PR Documentation Generation (Recommendation 6):**
   - Run `TOOL report` → `qs_explorer_result/remediation/remediation_report.md` with scope and source
     file hashes, status summary, per-finding evidence (incl. raw finding JSON), change log, unified before/after
     diffs, validation results, and non-remediated findings (marked PARTIAL if findings are still pending). Present
     a short summary to the user with the report path and recommend a QSE rescan to confirm the findings are gone.
   - **PR Description Formatting:** When the user requests creating a Pull Request or reviewing findings for a PR, read `.bob/skills/qse-remediation/references/pr_template.md` and generate a structured PR description containing:
     - Executive summary and modified files matrix
     - Categorized vulnerability breakdown with CWEs, root causes, and applied fixes
     - Before vs. after security impact comparison
     - Verification checklist (test results and QSE rescan recommendations)
     - Standards compliance checklist (NIST SP 800-175B, FIPS 140-3, FIPS 203/204/205, OWASP)
     - Research methodology and source citations (if permission-gated research was approved)
   - Per project standards, also save the final chat outcome in `task-outcomes/` (prompt first, then `date`).

## Persistence and multi-session work
Everything needed lives in `qs_explorer_result/remediation/`: `state.json` (findings, statuses, validations),
`changelog.md` (append-only), `originals/` (pre-change copies), `remediation_report.md`. At the start of any
session, if `state.json` exists, run `TOOL status`, tell the user what is done/pending, and continue from there.
Do not delete or hand-edit these files. After a rescan that overwrites the findings, archive the old
`remediation/` folder first so evidence is not mixed.

## Notes
- Findings paths are relative to the workspace root. The tool resolves them; if a file is not found, ask the user.
- Files may already carry uncommitted user changes (check `git status`); the backup captures the current state,
  and the report records the git HEAD at `init`.
- Never commit or push as part of this skill unless the user asks.
