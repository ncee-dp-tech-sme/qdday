# QSE Command Construction Guide

## Overview
Detailed instructions for constructing Quantum Safe Explorer CLI commands based on project context, language, and scan type.

---

## ⚙️ REQUIRED CONFIGURATION: QSE CLI path (`<QSE_CLI_DIR>`)

Every command in this skill (and in the other `qse` skill files) uses the placeholder `<QSE_CLI_DIR>` for the location of the QSE CLI. **You must replace it with the absolute path of your local QSE installation before running any scan.**

**What the value must be:** a local directory containing **all files from your licensed QSE CLI package** (extracted as delivered), including `cli.sh` (macOS/Linux), `cli.ps1` (Windows), `configuration.prop`, `lib/`, `LicenseAcceptance.config`, `la_home/`, `swidtag/`, `version` and `vulnerability_severity.json`. The QSE CLI is licensed software and is **not** included in this package.

**How to configure it** (choose one):

1. **Recommended:** search and replace `<QSE_CLI_DIR>` with your absolute path in all files under `.bob/skills/qse/`:
   ```bash
   # macOS
   grep -rl '<QSE_CLI_DIR>' .bob/skills/qse | xargs sed -i '' 's#<QSE_CLI_DIR>#/absolute/path/to/qse-cli#g'
   # Linux
   grep -rl '<QSE_CLI_DIR>' .bob/skills/qse | xargs sed -i 's#<QSE_CLI_DIR>#/absolute/path/to/qse-cli#g'
   ```
2. Or tell Bob in the QSE mode: "The QSE CLI is installed at `/absolute/path/to/qse-cli`" and it will use that path for the session.

**Verify:** `ls <your path>/cli.sh` succeeds and `chmod +x <your path>/cli.sh` has been applied. Use an absolute path (no `~` or relative paths) because the command changes into this directory before running.

Other placeholders used in the examples (`/path/to/...`) are illustrative project paths and do not need configuring.

---

## Command Anatomy

### Base Structure
```bash
cd <QSE_CLI_DIR> && ./cli.sh -i [input_path] -l [language] -ef "[exclusions]" [-cf [class_path]] [-da]
```

| Component | Value | Required |
|---|---|---|
| Change directory | `cd <QSE_CLI_DIR>` | ✅ Yes |
| Command separator | `&&` | ✅ Yes |
| QSE script | `./cli.sh` | ✅ Yes |
| Parameters | `-i [path] -l [ext] -ef "[dirs]" [-cf [path]] [-da]` | ✅ Yes (`-i`, `-l` and `-ef`) |

---

## Parameter Reference

### `-i` — Input Path
The directory containing the source code to scan.

- **Required:** Yes
- **Default:** Current working directory
- **Construction logic:**
  1. Check if user specified a custom path
  2. If not, use current workspace directory
  3. Ensure path is absolute when possible
  4. Verify path exists before constructing command

```bash
-i /path/to/gsi/quantum/qse/crypto-samples
-i /path/to/project
-i .
```

---

### `-l` — Language
File extension indicating the programming language.

- **Required:** Yes
- **Possible values:** `.java`, `.go`, `.dart`, `.py`, `.cpp`
- **Construction logic:**
  1. Detect language using `4_language_detection.md` rules
  2. Map detected language to appropriate extension
  3. If detection fails, ask user to specify

```bash
-l .java
-l .go
-l .py
```

---

### `-cf` — Class File Path
Path to compiled Java class files (bytecode).

- **Required:** Only for Java Cryptographic Analytics scan
- **Default:** Same as input path (`-i`)
- **Construction logic:**
  1. Only include for Java projects with `-da` flag
  2. Search for build output in this order:
     - `target/classes` (Maven)
     - `build/classes/java/main` (Gradle)
     - `out/production` (IntelliJ IDEA)
     - `bin` (Eclipse)
  3. If found, use that path; otherwise use input path as fallback

```bash
-cf /path/to/project/target/classes
-cf /path/to/project/build/classes
-cf /path/to/project    # fallback: same as input path
```

---

### `-ef` — Path Exclusion Filter (ALWAYS INCLUDE)
Excludes directories from the scan. Dependency, virtual-environment and VCS directories must **always** be excluded from every scan (all languages, all scan types).

- **Required:** Yes — always include
- **Format:** comma-separated list of paths **relative to the `-i` input path**, in one quoted string. Semicolons do not work.
- **Matching:** prefix match from the input root only. `node_modules` does NOT match `web/node_modules`; nested directories need their own relative path (`web/node_modules`).
- **Default exclusion list:**
  ```
  .bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__
  ```
- **Construction logic:**
  1. Start with the default list above
  2. Find nested occurrences of these directory names (e.g. `find [input_path] -type d \( -name node_modules -o -name .venv -o -name venv -o -name site-packages -o -name .bob \) -prune`) and append each as a path relative to `-i`
  3. Add any extra exclusions the user requests
  4. Never exclude real source directories; do not exclude `build`/`target`/`dist` unless the user asks

```bash
-ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
-ef ".bob,.venv,venv,node_modules,web/node_modules,services/api/.venv"
```

---

### `-da` — Discovery Analytics Flag
Enables Cryptographic Analytics mode.

- **Required:** Only for Cryptographic Analytics scan
- **Include when:** Language is Java AND scan type is Cryptographic Analytics
- **Exclude when:** Scan type is API Discovery OR language is not Java

---

## Construction Algorithms

### Algorithm 1: Java — Cryptographic Analytics

```
1. Start: cd <QSE_CLI_DIR> && ./cli.sh
2. Add: -i [workspace_or_specified_path]
3. Add: -l .java
3a. Add: -ef "[default exclusions + nested matches]"
4. Determine class file path:
     - Search for target/classes, build/classes, out/production, bin
     - If found → use that path
     - If not found → use input path as fallback
5. Add: -cf [determined_path]
6. Add: -da
```

**Example output:**
```bash
cd <QSE_CLI_DIR> && ./cli.sh -i /path/to/project -l .java -ef ".venv,venv,node_modules,.git" -cf /path/to/project/target/classes -da
```

---

### Algorithm 2: Java — API Discovery

```
1. Start: cd <QSE_CLI_DIR> && ./cli.sh
2. Add: -i [workspace_or_specified_path]
3. Add: -l .java
3a. Add: -ef "[default exclusions + nested matches]"
4. DO NOT add -cf flag
5. DO NOT add -da flag
```

**Example output:**
```bash
cd <QSE_CLI_DIR> && ./cli.sh -i /path/to/project -l .java -ef ".venv,venv,node_modules,.git"
```

---

### Algorithm 3: Non-Java — API Discovery

```
1. Start: cd <QSE_CLI_DIR> && ./cli.sh
2. Add: -i [workspace_or_specified_path]
3. Add: -l [detected_extension]
3a. Add: -ef "[default exclusions + nested matches]"
4. DO NOT add -cf flag (not applicable)
5. DO NOT add -da flag (not applicable)
```

**Example output:**
```bash
cd <QSE_CLI_DIR> && ./cli.sh -i /path/to/project -l .go -ef ".venv,venv,node_modules,vendor,.git"
```

---

## Common Patterns

### Scan current workspace directory
```bash
cd <QSE_CLI_DIR> && ./cli.sh -i . -l [language] -ef "[exclusions]"
```

### Scan a user-specified directory
```bash
cd <QSE_CLI_DIR> && ./cli.sh -i [user_path] -l [language] -ef "[exclusions]"
```

### Java — complete quantum readiness (both scans)
```bash
# Scan 1: Cryptographic Analytics
cd <QSE_CLI_DIR> && ./cli.sh -i [path] -l .java -ef "[exclusions]" -cf [class_path] -da

# Scan 2: API Discovery
cd <QSE_CLI_DIR> && ./cli.sh -i [path] -l .java -ef "[exclusions]"
```

---

## Validation Checklist
Before executing any QSE command, verify:

- [ ] Base path is `<QSE_CLI_DIR>`
- [ ] Script name is `./cli.sh`
- [ ] `-i` parameter is present with a valid path
- [ ] `-l` parameter is present with a valid extension
- [ ] `-ef` parameter is present and excludes `.bob`, `.venv`, `venv`, `node_modules` (plus other defaults and nested matches)
- [ ] For Java Cryptographic Analytics: `-cf` and `-da` are both present
- [ ] For API Discovery: `-da` is **not** present
- [ ] For non-Java: `-cf` is **not** present
- [ ] Command uses `&&` to chain `cd` and execution

---

## Error Prevention Rules
- Never include `-da` for API Discovery scans
- Never include `-cf` for non-Java languages
- Always verify input path exists before executing
- Always use absolute path for QSE installation
- Always include `-i`, `-l` and `-ef` parameters
- Always exclude language/dependency and tooling directories (`.bob`, `.venv`, `venv`, `node_modules`, ...) via `-ef`; separate entries with commas, never semicolons
- For Java Cryptographic Analytics, always include both `-cf` and `-da`

---

## Path Resolution Notes

**Input path (`-i`):**
1. If user specifies a path → use it as provided
2. If no path specified → use current workspace directory
3. Convert relative paths to absolute when possible
4. Verify path exists before constructing command

**Class file path (`-cf`) for Java:**
1. Use `list_files` to check for build output directories
2. Search in order: `target/classes` → `build/classes` → `out/production` → `bin`
3. If multiple found, prefer Maven (`target`) over Gradle (`build`)
4. If none found, use input path as fallback
5. Always use absolute paths

**Why absolute paths matter:**
> The command changes working directory to `<QSE_CLI_DIR>` before executing, so relative project paths may not resolve correctly.
