# QCM Integration Guide

## Overview
Detailed instructions for integrating QSE findings with IBM Quantum Cryptographic Manager (QCM) using the `gcm_api` MCP tool.

---

## QCM MCP Server

The `gcm-mcp-server` provides tools to interact with IBM Guardium Cryptographic Manager (GCM/QCM) APIs. It enables uploading QSE findings for centralized cryptographic asset management and policy enforcement.

**Authentication:** Use the same authorization and token_type headers from the gcm-mcp-server configuration 

---

## Prerequisites Before Upload
- [ ] QSE scan completed successfully
- [ ] Findings JSON file exists in the explorer results directory
- [ ] QCM server is accessible
- [ ] QSE import profile exists in QCM
- [ ] Repository URL has been updated in the findings JSON

---

## When to Upload
- After a QSE scan completes and a findings JSON file is generated
- When the user explicitly requests QCM integration
- After successfully updating the `repositoryUrl` field in the findings file

---

## API Operations

### Operation 1: List Import Profiles

**Purpose:** Retrieve all import profiles to find the QSE profile ID.

```json
{
  "service": "discovery",
  "operation": "import_profiles.list"
}
```

**MCP call:**
```
server: gcm-mcp-server
tool: gcm_api
arguments: { "service": "discovery", "operation": "import_profiles.list" }
```

**Response handling:**
1. Parse response to find profiles
2. Look for QSE-related profile by name or description
3. Extract the `profile_identifier` field
4. Store profile ID for the upload step

**Error scenarios:**
- No profiles found → inform user to create a QSE profile first
- Multiple QSE profiles → ask user which one to use
- API error → report error and check connectivity

---

### Operation 2: Upload Findings

**Purpose:** Upload the QSE findings JSON file to QCM.

```json
{
  "service": "discovery",
  "operation": "import.upload",
  "path_params": {
    "profile_identifier": "[profile_id_from_list_operation]"
  },
  "file_path": "/absolute/path/to/workspace/qse_explorer_result/findings.json"
}
```

**MCP call:**
```
server: gcm-mcp-server
tool: gcm_api
arguments: {
  "service": "discovery",
  "operation": "import.upload",
  "path_params": { "profile_identifier": "profile_id_123" },
  "file_path": "/Users/user/project/qse_explorer_result/findings.json"
}
```

> ⚠️ **IMPORTANT:** `file_path` must be an **absolute path**. Construct it by combining the working directory with `qse_explorer_result/[filename]`.

**Validation before upload:**
- [ ] File exists at specified path
- [ ] File is valid JSON format
- [ ] File is not empty
- [ ] `profile_identifier` is valid

**Success response handling:**
- Confirm upload completed
- Inform user findings are now in QCM
- Provide any upload ID or reference from the response

**Failure response handling:**
- Report the specific error message
- Verify file path is correct
- Verify profile ID is valid
- Check QCM server connectivity
- Remind user findings remain available locally

---

## Findings File Location

QSE generates findings files in the explorer results directory **relative to the working directory where the scan was executed** — NOT in the QSE installation directory.

### Typical locations
```
./qse_explorer_result/                 (relative to working directory)
[workspace_directory]/qse_explorer_result/
```

### File patterns
```
findings*.json
*_findings.json
qse_results*.json
*.json          (any JSON file in the explorer results directory)
```

### Detection strategy

<Steps>
<Step>
Use `list_files` on `./qse_explorer_result/`
</Step>
<Step>
Filter for JSON files
</Step>
<Step>
Sort by modification time (most recent first)
</Step>
<Step>
Select the most recent findings file
</Step>
<Step>
Verify file is not empty and contains valid JSON
</Step>
<Step>
Construct the full absolute path:
```bash
# Example: if working dir is /Users/user/project
# and file is qse_explorer_result/findings.json
# → /Users/user/project/qse_explorer_result/findings.json
```
</Step>
</Steps>

---

## Complete QCM Upload Workflow

<Steps>
<Step>

### Step 1: Locate Findings File
```
list_files(path="./qse_explorer_result/")
```
Identify the most recent JSON file and construct its absolute path.

</Step>
<Step>

### Step 2: Update Repository URL in Findings JSON

Get GitHub URL from git remote:
```bash
git -C [workspace_dir] remote get-url origin
```
If this fails or returns a non-GitHub URL, ask the user for the URL.

Update `repositoryUrl` field using `sed` (creates backup automatically):
```bash
sed -i.bak 's|"repositoryUrl"[[:space:]]*:[[:space:]]*"[^"]*"|"repositoryUrl": "[github_url]"|g' [findings_file_path]
```

Validate JSON structure:
```bash
jq -r '.findings.repositoryUrl' [findings_file_path]
```

> If validation fails: restore from backup using `mv [file].bak [file]` and report the error.

</Step>
<Step>

### Step 3: Get QCM Import Profiles
```json
{
  "service": "discovery",
  "operation": "import_profiles.list"
}
```
Extract the `profile_identifier` for the QSE profile.

</Step>
<Step>

### Step 4: Upload Findings
```json
{
  "service": "discovery",
  "operation": "import.upload",
  "path_params": {
    "profile_identifier": "[profile_id_from_step_3]"
  },
  "file_path": "/absolute/path/to/workspace/qse_explorer_result/[filename]"
}
```
The file now contains the updated `repositoryUrl`.

</Step>
<Step>

### Step 5: Confirm Completion
- Inform user scan completed and findings uploaded
- Provide upload reference if available in the response
- Mention local file path for reference

</Step>
</Steps>

---

## Best Practices

| Practice | Details |
|---|---|
| Verify file before upload | Use `list_files` to confirm the file exists and get its exact absolute path |
| Always use absolute paths | `gcm_api` requires absolute paths for file uploads |
| Cache profile ID | If running multiple scans, reuse the profile ID to avoid repeated API calls |
| Provide clear error messages | When upload fails, guide the user; remind them findings remain available locally |
| Handle auth gracefully | If auth fails, inform user about `GCM_USERNAME`/`GCM_PASSWORD` env vars |
| Validate JSON before upload | Optionally read and validate structure before uploading |
| Update repository URL first | Always update `repositoryUrl` in findings JSON **before** uploading to QCM |
| Create backup before modifying | The `sed -i.bak` flag creates a `.bak` backup for recovery |

---

## Error Recovery

| Scenario | Symptoms | Resolution |
|---|---|---|
| Profile not found | `import_profiles.list` returns empty or no QSE profile | Inform user to create a QSE import profile in QCM; do not proceed with upload |
| File not found | Findings file doesn't exist at expected location | List `qse_explorer_result/` contents; check if scan actually completed; look for alternative filenames |
| Upload fails | API returns error | Report specific error; verify path and profile ID; check connectivity; remind user findings are local |
| Authentication fails | API returns auth error | Check authorization and token_type; do not proceed until authenticated |
| Explorer results missing | `qse_explorer_result/` directory doesn't exist | Verify scan ran and completed; check if scan ran from a different directory |
| GitHub URL not available | `git remote` fails or returns non-GitHub URL | Ask user for GitHub repository URL; validate it contains `github.com` |
| Repository URL update fails | `sed` command fails or `jq` validation fails | Restore from `.bak` backup; suggest manual update; do not upload until URL is correct |

---

## User Communication Templates

**Success:**
```
QSE scan completed successfully. Findings have been uploaded to Quantum
Cryptographic Manager (QCM) and are now available for analysis and policy
enforcement. The findings file remains available locally at [absolute_path].
```

**Partial success (upload failed):**
```
QSE scan completed successfully. However, upload to QCM failed: [error_details].
The findings file is available locally at [absolute_path] and can be manually
uploaded or the upload can be retried.
```

**Failure (findings not located):**
```
QSE scan completed but the findings file could not be located. Please check
the explorer results directory in your working directory for scan results.
```
