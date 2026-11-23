# 🔐 Quantum Safe Explorer (QSE) Mode for Bob: Distribution Package

A custom Bob mode (`qse`) plus two skills that take a codebase from **scan** to **remediation**:

1. **Scan** for quantum-vulnerable cryptography with the IBM Quantum Safe Explorer CLI.
2. **Upload** findings to IBM Guardium Cryptographic Manager (QCM) (optional).
3. **Remediate** the findings with reviewed, documented, user-approved code changes.

---

## ⚠️ Configuration required before first use

This package contains **placeholders** for values that are specific to your environment. Bob cannot scan or upload until you replace them. Each placeholder is written in `<ANGLE_BRACKETS>`.

| Placeholder | Where it is used | What you must provide |
|---|---|---|
| `<QSE_CLI_DIR>` | `.bob/skills/qse/*.md` (all scan commands) | **Absolute path to a local directory that contains all files of your licensed QSE CLI package** (`cli.sh`, `cli.ps1`, `configuration.prop`, `lib/`, `LicenseAcceptance.config`, `la_home/`, `swidtag/`, `version`, `vulnerability_severity.json`). The QSE CLI is licensed IBM software and is **not** included here. |
| `<GCM_MCP_SERVER_URL>` | `.bob/mcp.json` → `url` | The HTTPS URL of your QCM / Guardium Cryptographic Manager MCP endpoint (ask your QCM administrator). |
| `<GCM_BEARER_TOKEN>` | `.bob/mcp.json` → `headers.Authorization` | Your QCM API token. Keep the `Bearer ` prefix and replace only `<GCM_BEARER_TOKEN>`. |

> **Users must configure these placeholder items for their local installation.** Nothing in this package is pre-configured for your machine, your QCM server, or your credentials.

> The two `gcm-mcp-server` placeholders are only needed for the optional QCM upload. Local scanning and remediation need only `<QSE_CLI_DIR>`. If you do not use QCM, you can leave `mcp.json` unconfigured and set `"disabled": true` for the server.

### 1. Configure `<QSE_CLI_DIR>`

Replace the placeholder in all scan skill files, using the absolute path of your QSE CLI directory:

```bash
# macOS
grep -rl '<QSE_CLI_DIR>' .bob/skills/qse | xargs sed -i '' 's#<QSE_CLI_DIR>#/absolute/path/to/qse-cli#g'
# Linux
grep -rl '<QSE_CLI_DIR>' .bob/skills/qse | xargs sed -i 's#<QSE_CLI_DIR>#/absolute/path/to/qse-cli#g'
```

Then confirm that `/absolute/path/to/qse-cli/cli.sh` exists and is executable (`chmod +x`). Detailed guidance is in [`.bob/skills/qse/3_command_construction.md`](.bob/skills/qse/3_command_construction.md) ("REQUIRED CONFIGURATION").

### 2. Configure `.bob/mcp.json` (optional, for QCM upload)

Edit [`.bob/mcp.json`](.bob/mcp.json) and replace both placeholders:

```json
"url": "<GCM_MCP_SERVER_URL>",
"headers": { "Authorization": "Bearer <GCM_BEARER_TOKEN>", ... }
```

**Security:** the token is a credential. Never commit the configured `mcp.json` to version control (add `.bob/mcp.json` to your `.gitignore`), do not share it, and rotate it if it is exposed. Use an HTTPS URL and a certificate trusted by your system.

---

## Requirements

- **A licensed version of IBM Quantum Safe Explorer (QSE) is required.** The QSE CLI is not included in this package and the scan skill cannot run without it. See `<QSE_CLI_DIR>` above.
- **Python 3.11 or later must be installed** (used by the remediation helper `remediation_tool.py`). The script itself only needs Python 3.7 or later, but older Python releases are end-of-life, so 3.11+ is required for this package.
- IBM Bob with the workspace open (the mode and skills load from `.bob/`).
- `git` (used by the helper to record the repository state) and `jq` (used to set and validate `repositoryUrl` in the findings JSON).
- macOS or Linux shell for the scan commands, which call `cli.sh`. On Windows, use WSL or adapt the commands to the `cli.ps1` script shipped with your QSE package.
- Optional, for QCM upload: a reachable QCM MCP server, `.bob/mcp.json` configured, and a QSE import profile in QCM.

**Python packages:** `remediation_tool.py` was analyzed and imports only standard-library modules (`argparse`, `datetime`, `difflib`, `glob`, `hashlib`, `json`, `os`, `re`, `subprocess`, `sys`). There are **no third-party (pip) dependencies**.

---

## Package Contents

Packaged release: [`bob-qse-remediation-1.0.0.zip`](bob-qse-remediation-1.0.0.zip) (see [Installation](#installation)). It extracts to a folder `bob-qse-remediation-1.0.0/` with this layout:

```
bob-qse-remediation-1.0.0/
├── README.md                                  this file
├── requirements.txt                           Python dependency list (no third-party packages)
└── .bob/
    ├── custom_modes.yaml                      defines the qse mode
    ├── mcp.json                               gcm-mcp-server (placeholders, configure!)
    └── skills/
        ├── qse/                               scan skill
        │   ├── SKILL.md
        │   ├── 1_workflow.md
        │   ├── 2_best_practices.md
        │   ├── 3_command_construction.md      contains the QSE CLI path instructions
        │   ├── 4_language_detection.md
        │   ├── 5_examples.md
        │   └── 6_qcm_integration.md
        └── qse-remediation/                   remediation skill
            ├── SKILL.md
            ├── remediation_tool.py
            └── references/
                ├── pr_template.md
                └── remediation_patterns.md
```

### Mode configuration

| Setting | Value |
|---|---|
| Slug | `qse` |
| Name | 🔐 Quantum Safe Explorer |
| Description | Scan codebases for quantum-readiness, analyze cryptographic APIs, and remediate vulnerabilities with post-quantum cryptography best practices. |
| Tool groups | `read`, `execute`, `mcp`, `edit`, `skill`, `subtask`, `subagent`, `mode` |
| Role | Quantum cryptography security specialist: runs QSE scans, interprets results, guides post-quantum crypto migrations (FIPS 203/204/205), and performs safe code remediation |

The `edit` group is enabled, so the remediation skill can apply approved changes without switching modes.

---

## Virtual Environment Setup

The remediation helper has no third-party dependencies, but running it in a virtual environment keeps your Python setup isolated and gives every user the same, reproducible interpreter. Create the environment in the root of the workspace you want to scan. The scan skill already excludes `.venv` from scans.

### 1. Create the virtual environment

Requires Python 3.11 or later (see [Requirements](#requirements)).

| OS | Command |
|---|---|
| macOS | `python3 -m venv .venv` |
| Linux | `python3 -m venv .venv` (on Debian/Ubuntu you may first need `sudo apt install python3-venv`) |
| Windows (PowerShell or cmd) | `py -3 -m venv .venv` (or `python -m venv .venv`) |

### 2. Activate it

| OS / shell | Command |
|---|---|
| macOS / Linux (bash, zsh) | `source .venv/bin/activate` |
| macOS / Linux (fish) | `source .venv/bin/activate.fish` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows cmd | `.venv\Scripts\activate.bat` |

On Windows PowerShell, if activation is blocked by the execution policy, run once: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.
Your prompt shows `(.venv)` when the environment is active. Leave it with `deactivate`.

### 3. Install the dependencies

Identified third-party dependencies of `remediation_tool.py`: **none** (standard library only). The complete installation command is still provided so the setup is the same for every user and stays valid if dependencies are added in a later release:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` is shipped in the package root. It currently lists no packages, so the second command completes without installing anything.

### 4. Verify the installation

```bash
python --version                  # expect Python 3.11.x or later
python -m pip --version           # path must point inside your .venv folder
python -m pip check               # expect: No broken requirements found.
python -m pip list                # expect only pip (and possibly setuptools): no other packages are needed
python .bob/skills/qse-remediation/remediation_tool.py --help   # expect the list of commands: init, status, show, backup, record, record-validation, report
```

If the last command prints the usage text, the helper runs correctly in your environment. Inside an activated environment, use `python` instead of `python3` in the helper commands shown later in this document.

---

## Installation

**From the packaged release** (`bob-qse-remediation-1.0.0.zip`, in the same folder as this README):

```bash
unzip bob-qse-remediation-1.0.0.zip          # Windows: Expand-Archive bob-qse-remediation-1.0.0.zip .
cp -R bob-qse-remediation-1.0.0/.bob/. <your-workspace>/.bob/
cp bob-qse-remediation-1.0.0/requirements.txt <your-workspace>/
```

Then:

1. If a `.bob/` folder already exists in your workspace, merge instead of overwriting. Do not replace your existing `mcp.json`; add only the `gcm-mcp-server` entry. (You can also install into your home Bob configuration to make the mode available everywhere.)
2. Complete the placeholder configuration above.
3. Set up the virtual environment (see [Virtual Environment Setup](#virtual-environment-setup)).
4. Restart or reload Bob so it picks up the `qse` mode.
5. Select the **🔐 Quantum Safe Explorer** mode.

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

## Usage

Select the QSE mode and ask in plain language, for example:

- "Scan this project for quantum-vulnerable cryptography."
- "Run an API discovery scan on `./services/api`."
- "Scan and upload the findings to QCM."
- "Remediate the findings from the last scan."

### Scan workflow (`qse` skill)

1. Understand the request (scan type, optional directory).
2. Detect the project language (file extensions plus markers such as `pom.xml`, `go.mod`).
3. Determine parameters: `-i` input path, `-l` language, and for Java Cryptographic Analytics `-cf` (searches `target/classes`, `build/classes/java/main`, `out/production`, `bin`).
4. Build and run the command:

   ```bash
   cd <QSE_CLI_DIR> && ./cli.sh \
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
4. **Permission-gated Web Research:** If an unfamiliar algorithm or novel CVE is encountered, Bob checks offline patterns first. If online lookup is needed, Bob prompts for explicit user approval, displaying the exact search query and target domains, and confirming no repository code or secrets will be sent.
5. **Nothing is edited without your explicit approval** of that specific proposal.
6. Approved changes are backed up first, applied with a timestamped comment block, and recorded in the change log.
7. Each change is validated (syntax or compile check, linter, tests) and the result is recorded.
8. A final report with before/after diffs and validation evidence is generated. A QSE rescan is recommended to confirm the findings are gone.
9. **PR Generation:** When requested, Bob formats a comprehensive, structured Pull Request description following [`.bob/skills/qse-remediation/references/pr_template.md`](.bob/skills/qse-remediation/references/pr_template.md).

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

Do not delete or hand-edit the `remediation/` files. If a rescan overwrites the findings, archive the old `remediation/` folder first so evidence is not mixed.

---

## Troubleshooting

| Symptom | Action |
|---|---|
| Bob asks for the QSE CLI path, or commands contain `<QSE_CLI_DIR>` | The placeholder is not configured. See "Configure `<QSE_CLI_DIR>`" |
| `No such file or directory` for `cli.sh` | The path is wrong or incomplete. It must be the directory containing all files of the licensed package, and `cli.sh` must be executable |
| Language not detected | Tell Bob the language: `.java`, `.go`, `.dart`, `.py` or `.cpp` |
| No findings file | List `qs_explorer_result/` in the working directory (not the CLI install dir) and confirm the scan completed |
| `repositoryUrl` update fails | Restore the `.bak` file and supply the GitHub URL manually |
| `gcm-mcp-server` fails to connect or returns an authentication error | Check that `<GCM_MCP_SERVER_URL>` and `<GCM_BEARER_TOKEN>` in `.bob/mcp.json` were replaced with valid values |
| QCM profile not found | Create a QSE import profile in QCM, then retry |
| QCM upload fails | Check connectivity and credentials, and use an absolute `file_path`. Findings stay available locally |
| Remediation finding looks stale | Bob marks it `skipped` with a reason. Rescan to refresh |
| Remediation cannot edit files | Confirm the `edit` group is present in `.bob/custom_modes.yaml`, or switch to Agent mode. State is on disk, so nothing is lost |

---

## Further reading

- [`.bob/skills/qse/SKILL.md`](.bob/skills/qse/SKILL.md): scan skill overview
- [`.bob/skills/qse/3_command_construction.md`](.bob/skills/qse/3_command_construction.md): CLI parameters and path configuration
- [`.bob/skills/qse/5_examples.md`](.bob/skills/qse/5_examples.md): worked examples per language
- [`.bob/skills/qse-remediation/SKILL.md`](.bob/skills/qse-remediation/SKILL.md): remediation workflow and ground rules

---

## Release Notes

### Version 1.0.0 (2026-11-23): initial release

- Initial release of the `🔐 Quantum Safe Explorer` (`qse`) Bob mode.
- `qse` scan skill: language detection, QSE CLI command construction, Cryptographic Analytics (Java) and API Discovery scans (Java, Go, Python, Dart, C++), repository URL stamping, optional upload of findings to QCM through `gcm-mcp-server`.
- `qse-remediation` skill and `remediation_tool.py` helper: per-file fix proposals, user-approved edits only, change log, validation records, before/after remediation report.
- Distribution placeholders for local configuration: `<QSE_CLI_DIR>`, `<GCM_MCP_SERVER_URL>`, `<GCM_BEARER_TOKEN>`.
- No third-party Python dependencies (standard library only). Requires Python 3.11 or later and a licensed QSE CLI.
- Packaged as `bob-qse-remediation-1.0.0.zip`.

---

## Disclaimer

This tool was created by Erwin Friethoff - Senior Security Architect at IBM and is **not officially supported by IBM**. IBM does not provide support, maintenance, warranties, or guarantees for it. It is provided "as is", without warranty of any kind. Review all proposed code changes before approving them, and test your software after remediation. IBM Quantum Safe Explorer, IBM Guardium, and IBM Bob are products and trademarks of IBM Corporation and remain subject to their own license terms. You need a valid license for QSE, which is not included in this package.

**For any questions, remarks or suggestions, please reach out to Erwin**