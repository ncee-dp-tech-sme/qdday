# 🔐 Quantum Safe Explorer (QSE) Mode for Bob

A custom Bob mode (`qse`) plus two skills that take a codebase from **scan** to **remediation**:

1. **Scan** for quantum-vulnerable cryptography with the IBM Quantum Safe Explorer CLI.
2. **Upload** findings to IBM Guardium Cryptographic Manager (QCM) (optional).
3. **Remediate** the findings with reviewed, documented, user-approved code changes.

> This file documents the Bob mode. The root [`README.md`](README.md) describes the sample application being scanned.

---

## Contents

| Component | Location | Purpose |
|---|---|---|
| Mode definition | [`.bob/custom_modes.yaml`](.bob/custom_modes.yaml) | Defines the `🔐 Quantum Safe Explorer` mode (slug `qse`) |
| Scan skill | [`.bob/skills/qse/`](.bob/skills/qse/SKILL.md) | Language detection, QSE CLI command construction, scan execution, QCM upload |
| Remediation skill | [`.bob/skills/qse-remediation/`](.bob/skills/qse-remediation/SKILL.md) | Per-file fix proposals, approved edits, change log, report |
| Remediation helper | [`.bob/skills/qse-remediation/remediation_tool.py`](.bob/skills/qse-remediation/remediation_tool.py) | Python 3 stdlib-only state/evidence tool |
| Fix guidance | [`.bob/skills/qse-remediation/references/remediation_patterns.md`](.bob/skills/qse-remediation/references/remediation_patterns.md) | Remediation patterns per algorithm/vulnerability |
| MCP servers | [`.bob/mcp.json`](.bob/mcp.json) | `gcm-mcp-server` (QCM upload), `bob-marketplace` |

### Mode configuration

| Setting | Value |
|---|---|
| Slug | `qse` |
| Name | 🔐 Quantum Safe Explorer |
| Tool groups | `read`, `execute`, `mcp`, `edit`, `skill`, `subtask`, `subagent`, `mode` |
| Role | Quantum cryptography security specialist: runs QSE scans, interprets results, explains post-quantum requirements |

The `edit` group is enabled, so the remediation skill can apply approved changes without switching modes.

---

## Supported languages and scan types

| Language | `-l` value | Cryptographic Analytics (`-da`) | API Discovery |
|---|---|---|---|
| Java | `.java` | Yes (bytecode, needs `-cf`) | Yes |
| Go | `.go` | No | Yes |
| Python | `.py` | No | Yes |
| Dart | `.dart` | No | Yes |
| C++ | `.cpp` | No | Yes |

For **Java**, a complete readiness assessment needs both scans: Cryptographic Analytics first, then API Discovery. All other languages run API Discovery only.

---

## Prerequisites

- IBM Bob with this workspace open (the mode and skills are loaded from `.bob/`).
- The QSE CLI installed. The skill uses this fixed path: `/Users/erwin/development/gcmmcp/CLI` (`./cli.sh`). On another machine, update the path in the `qse` skill files (`SKILL.md`, `1_workflow.md`, `3_command_construction.md`, `5_examples.md`).
- `git` and `jq` (used to stamp and validate `repositoryUrl` in the findings JSON).
- Python 3 for the remediation helper. Use the project `.venv` for tests and validation.
- Optional, for QCM upload: access to the `gcm-mcp-server` MCP server and a QSE import profile in QCM.

---

## Usage

1. Open Bob and select the **🔐 Quantum Safe Explorer** mode.
2. Ask in plain language. Examples:
   - "Scan this project for quantum-vulnerable cryptography."
   - "Run an API discovery scan on `./services/api`."
   - "Scan and upload the findings to QCM."
   - "Remediate the findings from the last scan."
3. Review the results in the output folders described below.

### Scan workflow (`qse` skill)

1. Understand the request (scan type, optional directory).
2. Detect the project language (file extensions plus markers such as `pom.xml`, `go.mod`).
3. Determine parameters: `-i` input path, `-l` language, and for Java Cryptographic Analytics `-cf` (searches `target/classes`, `build/classes/java/main`, `out/production`, `bin`).
4. Build and run the command:

   ```bash
   cd /Users/erwin/development/gcmmcp/CLI && ./cli.sh \
     -i <path> -l <.ext> \
     -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__" \
     [-cf <class_dir> -da]   # Java Cryptographic Analytics only
   ```

   `-ef` is always added so tooling and dependency directories are never scanned. It is comma-separated, relative to `-i`, and prefix-matched, so nested directories (for example `web/node_modules`) are added explicitly.
5. Locate the newest findings JSON in `./qs_explorer_result/`.
6. Set `repositoryUrl` in the findings from `git remote get-url origin` (a `.bak` backup is kept and the JSON is validated with `jq`).
7. Optional: upload to QCM through `gcm_api` (`import_profiles.list`, then `import.upload` with an absolute file path).

Full details are in the [`.bob/skills/qse/`](.bob/skills/qse/) reference files (`1_workflow.md` to `6_qcm_integration.md`).

### Remediation workflow (`qse-remediation` skill)

Run after a scan has produced findings in `qs_explorer_result/`.

1. `init` loads the findings, groups them per source file, and assigns stable IDs (`F-001`, ...). Re-running it keeps existing statuses, so work can resume across sessions.
2. Files are processed one at a time, highest severity first.
3. For each file Bob reads the code, confirms the finding is still current, and proposes a diff. The proposal includes the CWE, the rationale, what stays the same, and any **BEHAVIOR-CHANGING** items.
4. **Nothing is edited without your explicit approval** of that specific proposal.
5. Approved changes are backed up first, applied with a timestamped comment block (finding IDs, vulnerability, change, rationale, notes), and recorded in the change log.
6. Each change is validated (syntax or compile check, linter, tests) and the result is recorded.
7. A final report with before/after diffs and validation evidence is generated. A QSE rescan is recommended to confirm the findings are gone.

Helper commands (run from the workspace root):

```bash
python3 .bob/skills/qse-remediation/remediation_tool.py init     # load findings / resume
python3 .bob/skills/qse-remediation/remediation_tool.py status   # progress summary
python3 .bob/skills/qse-remediation/remediation_tool.py show --file <path>
python3 .bob/skills/qse-remediation/remediation_tool.py backup --file <path>
python3 .bob/skills/qse-remediation/remediation_tool.py record --ids F-001 --status applied|skipped|rejected|deferred --summary "<text>"
python3 .bob/skills/qse-remediation/remediation_tool.py record-validation --file <path> --command "<cmd>" --exit-code <n> --summary "<text>"
python3 .bob/skills/qse-remediation/remediation_tool.py report   # writes remediation_report.md
```

---

## Output locations

| Path | Content |
|---|---|
| `qs_explorer_result/` | QSE findings, CBOM, crypto inventory and report JSON files |
| `qs_explorer_result/remediation/state.json` | Findings, statuses, validation results (source of truth) |
| `qs_explorer_result/remediation/changelog.md` | Append-only change log |
| `qs_explorer_result/remediation/originals/` | Pristine pre-change copies of edited files |
| `qs_explorer_result/remediation/remediation_report.md` | Final remediation report |
| `task-outcomes/` | Saved task summaries (prompt first, then timestamp) |

Do not delete or hand-edit the `remediation/` files. If a rescan overwrites the findings, archive the old `remediation/` folder first so evidence is not mixed.

---

## Configuration and security notes

- **MCP credentials:** `.bob/mcp.json` contains the QCM authorization header. Keep it out of version control and rotate the token if it was ever shared. Do not paste it into documentation or chat.
- **Git ignore:** [`.gitignore`](.gitignore) currently excludes `.bob/custom_modes.yaml`, `.bob/mcp.json`, and the skill files. The mode is therefore **not shared through git**. To share it with a team, remove the skill and mode entries from `.gitignore` and keep only `.bob/mcp.json` ignored.
- **Machine-specific path:** the QSE CLI path is hard-coded in the scan skill (see Prerequisites).
- **Approval gate:** remediation never edits code, commits, or pushes without your explicit request.

---

## Troubleshooting

| Symptom | Action |
|---|---|
| Language not detected | Tell Bob the language: `.java`, `.go`, `.dart`, `.py` or `.cpp` |
| Scan command fails | Check the CLI path, that `./cli.sh` is executable, and that the input path exists |
| No findings file | List `qs_explorer_result/` in the working directory (not the CLI install dir) and confirm the scan completed |
| `repositoryUrl` update fails | Restore the `.bak` file and supply the GitHub URL manually |
| QCM profile not found | Create a QSE import profile in QCM, then retry |
| QCM upload fails | Check connectivity and credentials, and use an absolute `file_path`. Findings stay available locally |
| Remediation finding looks stale | Bob marks it `skipped` with a reason. Rescan to refresh |
| Remediation cannot edit files | Confirm the `edit` group is present in `.bob/custom_modes.yaml`, or switch to Agent mode. State is on disk, so nothing is lost |

---

## Further reading

- [`.bob/skills/qse/SKILL.md`](.bob/skills/qse/SKILL.md): scan skill overview
- [`.bob/skills/qse/5_examples.md`](.bob/skills/qse/5_examples.md): worked examples per language
- [`.bob/skills/qse-remediation/SKILL.md`](.bob/skills/qse-remediation/SKILL.md): remediation workflow and ground rules
