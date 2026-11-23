# QSE Workflow

## Overview
This workflow guides you through running Quantum Safe Explorer (QSE) scans to analyze codebases for quantum computing readiness and cryptographic vulnerabilities.

## QSE Installation Path
The QSE CLI is installed at `<QSE_CLI_DIR>`. Always use this constant path when constructing commands.

---

## Scan Types

### Cryptographic Analytics
- Performs **deep cryptographic analysis** of Java bytecode (class files)
- **Java only** — requires `-da` flag and `-cf` (class file path)
- Always run for Java projects as part of quantum readiness assessment

### API Discovery
- Discovers and analyzes cryptographic API usage across source code
- **All supported languages:** `.java`, `.go`, `.dart`, `.py`, `.cpp`
- No `-da` flag; run for every project regardless of language
- For Java: run *in addition* to Cryptographic Analytics

---

## Workflow Steps

<Steps>
<Step>

### Step 1: Understand User Request
- Identify whether the user wants quantum readiness scan, crypto analysis, API discovery, or all
- Note any specific directory path mentioned
- Note any constraints or special requirements

</Step>
<Step>

### Step 2: Detect Project Language
- Use `list_files` recursively on the project root
- Count source file extensions and look for language-specific markers
- Language determines which scans to run:
  - **Java** → both Cryptographic Analytics AND API Discovery
  - **All other languages** → API Discovery only
- See `4_language_detection.md` for detailed detection rules

</Step>
<Step>

### Step 3: Determine Scan Parameters

| Parameter | Flag | Notes |
|---|---|---|
| Input path | `-i` | Default: current workspace directory |
| Language | `-l` | `.java`, `.go`, `.dart`, `.py`, `.cpp` |
| Class file path | `-cf` | **Java Cryptographic Analytics only** — search `target/classes` → `build/classes/java/main` → `out/production` → `bin`, fall back to input path |
| Cryptographic Analytics flag | `-da` | **Cryptographic Analytics only** — never include for API Discovery |

</Step>
<Step>

### Step 4: Construct QSE Command
- Base: `cd <QSE_CLI_DIR> && ./cli.sh`
- Add required params: `-i [input_path] -l [language] -ef "[exclusions]"`
- **Always** exclude language/dependency and tooling directories with `-ef` (comma-separated, relative to `-i`): `.bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__`, plus nested occurrences (e.g. `web/node_modules`)
- For Java Cryptographic Analytics: append `-cf [class_file_path] -da`
- For API Discovery: no additional flags
- See `3_command_construction.md` for detailed algorithms

</Step>
<Step>

### Step 5: Execute Scan
- Execute using `execute_command`
- **For Java quantum readiness:**
  1. First: Cryptographic Analytics scan (with `-da`)
  2. Second: API Discovery scan (without `-da`)
  - Both are required for complete analysis

</Step>
<Step>

### Step 6: Locate QSE Findings File
- Look for the findings JSON in `./qse_explorer_result/` in the **working directory** (not QSE installation directory)
- Use `list_files` to find the most recent JSON file
- **Do not proceed to QCM upload if file not found**

</Step>
<Step>

### Step 7: Update Repository URL in Findings
- Get GitHub URL from git remote:
  ```bash
  git -C [workspace_dir] remote get-url origin
  ```
- If command fails or returns non-GitHub URL, ask user for the URL
- Update `repositoryUrl` field in findings JSON:
  ```bash
  sed -i.bak 's|"repositoryUrl"[[:space:]]*:[[:space:]]*"[^"]*"|"repositoryUrl": "[github_url]"|g' [findings_file_path]
  ```
- Validate JSON structure and extract value:
  ```bash
  jq -r '.findings.repositoryUrl' [findings_file_path]
  ```
- If JSON validation fails, restore from backup and report error

</Step>
<Step>

### Step 8: Retrieve QCM Import Profile ID
- Call `gcm_api` with:
  ```json
  {
    "service": "discovery",
    "operation": "import_profiles.list"
  }
  ```
- Parse response to find the QSE findings profile
- Extract `profile_identifier` for use in upload
- If no QSE profile exists, inform user a profile must be created first

</Step>
<Step>

### Step 9: Upload Findings to QCM
- Call `gcm_api` with:
  ```json
  {
    "service": "discovery",
    "operation": "import.upload",
    "path_params": {
      "profile_identifier": "[profile_id_from_step_8]"
    },
    "file_path": "/absolute/path/to/workspace/qse_explorer_result/findings.json"
  }
  ```
- **Use the absolute path** — construct from working directory + relative findings path

</Step>
<Step>

### Step 10: Confirm Upload and Present Results
- Check the upload response for success
- Confirm upload to QCM with the user
- Provide summary of what was accomplished
- **Do not generate additional reports or summaries of the findings themselves**

</Step>
</Steps>

---

## Decision Tree

**What language is the project?**
- **Java** → Run Cryptographic Analytics (with `-da`) + API Discovery (without `-da`)
- **Go / Dart / Python / C++** → Run API Discovery only

**Should findings be uploaded to QCM?**
- **Yes** → Locate findings JSON → Get profile ID → Upload → Confirm
- **No** → Inform user findings are available locally

---

## Error Handling

| Scenario | Action |
|---|---|
| Language detection fails | Ask user to specify: `.java`, `.go`, `.dart`, `.py`, `.cpp` |
| Class files not found (Java) | Use input path as fallback for `-cf` |
| Scan execution fails | Report error, check QSE installation path and input path |
| Findings file not found | Check explorer results directory; do not proceed with QCM upload |
| GitHub URL not found | Try `git remote get-url origin`; if it fails, ask user directly |
| Repository URL update fails | Report sed error; restore from `.bak` backup; suggest manual update |
| QCM profile not found | List available profiles; ask user to create a QSE profile |
| QCM upload fails | Report error details; verify path and profile ID; findings remain available locally |

---

## Completion Criteria
- [ ] Language successfully detected or specified
- [ ] Appropriate scan type(s) determined
- [ ] Command constructed with correct parameters
- [ ] Scan executed successfully
- [ ] Findings file located in explorer results directory
- [ ] GitHub repository URL obtained and validated
- [ ] Repository URL updated in findings JSON successfully
- [ ] JSON structure validated after update
- [ ] QCM import profile ID retrieved successfully
- [ ] Findings uploaded to QCM successfully
- [ ] User informed of completion and upload status
