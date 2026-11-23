---
name: qse
description: Analyze codebases for quantum computing readiness and cryptographic vulnerabilities using the Quantum Safe Explorer (QSE) CLI. Use when scanning Java, Go, Python, Dart, or C++ projects for quantum-safe cryptography compliance, running cryptographic analytics or API discovery scans, or uploading findings to IBM Guardium Cryptographic Manager (QCM).
---

# Quantum Safe Explorer Skill

> **Configuration required:** replace the `<QSE_CLI_DIR>` placeholder (used throughout this skill) with the absolute path of your local, licensed QSE CLI directory. See `3_command_construction.md` ("REQUIRED CONFIGURATION"). If the placeholder is still present, ask the user for the path before scanning.

## What this skill does
Runs IBM Quantum Safe Explorer (QSE) scans against codebases to identify quantum-vulnerable cryptographic APIs and implementations. Covers the complete scan lifecycle: language detection, command construction, scan execution, findings location, repository URL stamping, and optional upload to Quantum Cryptographic Manager (QCM) via the `gcm_api` MCP tool.

## When to use it
Use this skill when you need to:
- Scan a Java, Go, Python, Dart, or C++ project for quantum-safe cryptography compliance
- Run a **Cryptographic Analytics** scan (Java only, bytecode-level deep analysis)
- Run an **API Discovery** scan (all supported languages)
- Perform a complete quantum readiness assessment (Java: both scans required)
- Upload QSE findings JSON to IBM Guardium / QCM for centralized tracking
- Troubleshoot QSE command failures or interpret scan parameters

## How to work with this skill

<Steps>
<Step>
**Understand the request** — determine the desired scan type (quantum readiness, crypto analysis, API discovery, or QCM upload) and whether a specific directory was specified.
</Step>
<Step>
**Detect the project language** — use `list_files` recursively on the project root. Count source file extensions and verify with language markers (e.g., `pom.xml` → Java, `go.mod` → Go). See `4_language_detection.md` for full rules.
</Step>
<Step>
**Determine scan parameters** — resolve the input path (`-i`), language flag (`-l`), and for Java Cryptographic Analytics: locate the class file directory (`-cf`) by searching `target/classes` → `build/classes/java/main` → `out/production` → `bin`, falling back to the input path.
</Step>
<Step>
**Construct the QSE command** — always use the exact base `cd <QSE_CLI_DIR> && ./cli.sh`. **Always** add `-ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"` (comma-separated, relative to `-i`, prefix match from the input root, so add nested dirs like `web/node_modules` explicitly) so language/dependency and assistant/tooling directories are never scanned. See `3_command_construction.md` for parameter rules and algorithm examples.
</Step>
<Step>
**Execute the scan** — for Java, run Cryptographic Analytics first (with `-da`), then API Discovery (without `-da`). For all other languages, run API Discovery only. Use `execute_command` for each.
</Step>
<Step>
**Locate the findings file** — after the scan, use `list_files` on `./qse_explorer_result/` in the working directory. Select the most recent JSON file.
</Step>
<Step>
**Update the repository URL** — run `git -C [workspace] remote get-url origin` to get the GitHub URL, then use `sed -i.bak` to update the `repositoryUrl` field in the findings JSON. Validate with `jq -r '.findings.repositoryUrl'`.
</Step>
<Step>
**Upload to QCM (optional)** — list import profiles via `gcm_api`, extract the QSE profile ID, then call `import.upload` with the absolute findings file path. Confirm success. See `6_qcm_integration.md` for full API details.
</Step>
</Steps>

## Supporting files
| File | Purpose |
|---|---|
| `1_workflow.md` | Full 10-step workflow with decision tree and error handling |
| `2_best_practices.md` | Principles, pitfalls, and quality checklist |
| `3_command_construction.md` | Command anatomy, parameter details, and construction algorithms |
| `4_language_detection.md` | Detection strategy, algorithms, directory patterns, and special cases |
| `5_examples.md` | Complete worked examples for Java, Go, Python, Dart, C++ |
| `6_qcm_integration.md` | QCM API operations, file detection, upload workflow |

## Source mode details
- **Original mode:** 🔐 Quantum Safe Explorer
- **Mode slug:** `qse`
- **Tool permissions:** `read`, `execute`, `mcp`
- **MCP tool used:** `gcm_api` on `gcm-mcp-server` (IBM Guardium / QCM integration)

## Additional notes
`.bob/mcp.json` was found in the source workspace. dDeploying this skill with QCM upload capability, you must use the `gcm-mcp-server` MCP server.
