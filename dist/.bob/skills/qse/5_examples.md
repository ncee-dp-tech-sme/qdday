# QSE Usage Examples

## Overview
Complete workflow examples demonstrating how to use the Quantum Safe Explorer skill for different languages and scenarios.

---

## Example 1: Java — Complete Quantum Readiness Scan

**User request:** `"Scan this Java project for quantum safety"`

<Steps>
<Step>

**Detect language**
Use `list_files` recursively → detects Java project (`.java` files, `pom.xml`)

</Step>
<Step>

**Locate class files directory**
Use `list_files` → finds `target/classes` (Maven project)

</Step>
<Step>

**Execute Cryptographic Analytics**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/gsi/bob/qse/qse-mode \
  -l .java \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__" \
  -cf /path/to/gsi/bob/qse/qse-mode/target/classes \
  -da
```

</Step>
<Step>

**Execute API Discovery**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/gsi/bob/qse/qse-mode \
  -l .java \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
<Step>

**Confirm completion**
> Both Cryptographic Analytics and API Discovery scans completed successfully. QSE reports are available in the output directory.

</Step>
</Steps>

---

## Example 2: Go — API Discovery

**User request:** `"Check my Go code for quantum safety issues"`

<Steps>
<Step>

**Detect language**
Use `list_files` → detects Go project (`.go` files, `go.mod`)

</Step>
<Step>

**Execute API Discovery** (no `-da`, no `-cf` for Go)
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/projects/go-app \
  -l .go \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
<Step>

**Confirm completion**
> API Discovery scan completed successfully for Go project. QSE report available.

</Step>
</Steps>

---

## Example 3: Python — Current Directory Scan

**User request:** `"Run quantum safe scan on this Python project"`

<Steps>
<Step>

**Detect language**
Use `list_files` → detects Python project (`.py` files, `requirements.txt`)

</Step>
<Step>

**Use current workspace directory** (no explicit path given)

</Step>
<Step>

**Execute API Discovery**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/gsi/bob/qse/qse-mode \
  -l .py \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
<Step>

**Confirm completion**
> API Discovery scan completed for Python project. Cryptographic API usage analysis available in QSE report.

</Step>
</Steps>

---

## Example 4: C++ — Specific Directory

**User request:** `"Scan /path/to/cpp-project for quantum vulnerabilities"`

<Steps>
<Step>

**Verify path exists**
Use `list_files` on `/path/to/cpp-project`

</Step>
<Step>

**Detect language**
Detects C++ project (`.cpp`, `.h` files, `CMakeLists.txt`)

</Step>
<Step>

**Execute API Discovery**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/cpp-project \
  -l .cpp \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
<Step>

**Confirm completion**
> API Discovery scan completed for C++ project at specified path.

</Step>
</Steps>

---

## Example 5: Dart / Flutter Project

**User request:** `"Analyze my Flutter app for quantum safety"`

<Steps>
<Step>

**Detect language**
Use `list_files` → detects Dart project (`.dart` files, `pubspec.yaml`)

</Step>
<Step>

**Execute API Discovery**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/flutter-app \
  -l .dart \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
<Step>

**Confirm completion**
> API Discovery scan completed for Dart/Flutter project.

</Step>
</Steps>

---

## Example 6: Java Gradle Project

**User request:** `"Run cryptographic analysis on this Gradle project"`

<Steps>
<Step>

**Detect language**
Use `list_files` → detects Java project (`.java` files, `build.gradle`)

</Step>
<Step>

**Locate class files**
Use `list_files` → finds `build/classes/java/main` (Gradle project)

</Step>
<Step>

**Execute Cryptographic Analytics**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/gradle-project \
  -l .java \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__" \
  -cf /path/to/gradle-project/build/classes/java/main \
  -da
```

</Step>
<Step>

**Execute API Discovery**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/gradle-project \
  -l .java \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
<Step>

**Confirm completion**
> Complete quantum readiness assessment completed for Gradle project.

</Step>
</Steps>

---

## Example 7: Ambiguous Language Detection

**User request:** `"Scan this project for quantum vulnerabilities"` (polyglot project)

<Steps>
<Step>

**Attempt language detection**
`list_files` finds both Java and Python files in similar quantities

</Step>
<Step>

**Ask user to specify**
```
"This project contains multiple languages. Which language should I scan for quantum safety?"

Options:
- Java (.java) — Supports both Cryptographic Analytics and API Discovery
- Python (.py) — API Discovery scan
```

</Step>
<Step>

**User selects Java** → proceed with full Java workflow (both scans)

</Step>
</Steps>

---

## Example 8: Java — No Class Files Found

**User request:** `"Run quantum safe scan on this Java project"` (uncompiled)

<Steps>
<Step>

**Detect language** → Java confirmed

</Step>
<Step>

**Search for class files**
`list_files` → no `target/classes` or `build/classes` found

</Step>
<Step>

**Use input path as fallback** for `-cf`

> Note: QSE will handle missing class files appropriately

</Step>
<Step>

**Execute Cryptographic Analytics with fallback path**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/java-project \
  -l .java \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__" \
  -cf /path/to/java-project \
  -da
```

</Step>
<Step>

**Execute API Discovery**
```bash
cd <QSE_CLI_DIR> && ./cli.sh \
  -i /path/to/java-project \
  -l .java \
  -ef ".bob,.venv,venv,env,.env,node_modules,site-packages,vendor,.git,__pycache__"
```

</Step>
</Steps>

---

## Common User Request Patterns

| Request Pattern | Interpretation | Action |
|---|---|---|
| "scan for quantum" | Run appropriate QSE scan(s) | Detect language, construct command, execute |
| "quantum readiness / quantum safe / post-quantum" | Full assessment | Java: both scans; others: API Discovery |
| "cryptographic analysis / crypto scan" | Cryptographic Analytics | Java: run with `-da`; others: explain limitation |
| "API discovery / API scan" | API Discovery only | Run without `-da` for any supported language |
| "scan [path]" | Scan specific directory | Use provided path as `-i` |

---

## Response Templates

**Scan started:**
```
Starting Quantum Safe Explorer scan for [LANGUAGE] project.
Scan type: [SCAN_TYPE]
Input path: [PATH]
```

**Java — both scans:**
```
Running complete quantum readiness assessment for Java project:
1. Cryptographic Analytics scan (analyzing bytecode)
2. API Discovery scan (analyzing source code)
```

**Scan completed:**
```
Quantum Safe Explorer scan completed successfully.
[SCAN_TYPE] analysis finished for [LANGUAGE] project.
Results are available in the QSE output directory.
```

**Language not supported:**
```
The detected language [LANGUAGE] is not supported by Quantum Safe Explorer.
Supported languages: Java, Go, Dart, Python, C++
```

---

## Troubleshooting

| Issue | Symptom | Diagnosis | Solution |
|---|---|---|---|
| QSE not found | `No such file or directory` | QSE not installed or wrong path | Verify QSE is at `<QSE_CLI_DIR>` and `cli.sh` is executable |
| Invalid path | `Invalid input path` | Specified directory does not exist | Verify with `list_files`; use absolute paths |
| No source files | Scan completes, finds nothing | Wrong language or unexpected file location | Re-run language detection; verify extensions |
