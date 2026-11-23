# QSE Best Practices

## Overview
Guidelines for using the Quantum Safe Explorer mode effectively — ensuring accurate scans, proper command construction, and clear user communication.

---

## General Principles

### 🔴 Always Detect Before Executing (Critical)
Never assume the project language. Always use `list_files` to detect the language before constructing QSE commands.

**Why:** Different languages require different scan types and parameters. Incorrect language detection leads to failed scans or incomplete analysis.

| ✅ Good | ❌ Bad |
|---|---|
| Use `list_files`, count extensions, confirm with markers, then construct command | Assume Java because user mentioned "class files" without verification |

---

### 🔴 Java Requires Both Scans (Critical)
For a complete quantum readiness assessment of Java projects, **always** run both scans:
1. **Cryptographic Analytics** (with `-da`) — bytecode-level deep analysis
2. **API Discovery** (without `-da`) — source-code API usage

---

### 🟡 Use Absolute Paths (High)
Prefer absolute paths over relative paths when constructing QSE commands.

**Why:** The command changes directory to `<QSE_CLI_DIR>` before executing, so relative paths may not resolve correctly.

| ✅ Good | ❌ Bad |
|---|---|
| `-i /path/to/gsi/bob/qse/qse-mode` | `-i ../qse-mode` |

---

### 🟡 Verify Paths Before Execution (High)
Always verify that input paths exist using `list_files` before constructing and executing commands.

---

### 🟢 Don't Parse QSE Output (Medium)
Do **not** attempt to parse, interpret, or summarize QSE scan results. QSE generates its own comprehensive reports. Simply confirm scan completion and inform the user results are available in QSE output.

---

## Language Detection Best Practices

### Count Files, Not Just Check Existence
Don't just check if `.java` files exist — count how many of each type exist to determine the dominant language.

```
Project with 100 .java files and 5 .py files  → Java project
Project with 10 .java files and 50 .go files  → Go project
```

### Check Language-Specific Markers

| Language | Markers |
|---|---|
| Java | `pom.xml`, `build.gradle`, `settings.gradle` |
| Go | `go.mod`, `go.sum` |
| Dart | `pubspec.yaml`, `pubspec.lock` |
| Python | `requirements.txt`, `setup.py`, `pyproject.toml` |
| C++ | `CMakeLists.txt`, `Makefile` |

### Exclude Build and Dependency Directories
When counting files, exclude:
```
.bob/  node_modules/  vendor/  .git/  build/  dist/  target/  __pycache__/  .venv/  venv/  .idea/  .vscode/
```

### Handle Ambiguity Gracefully
When two languages are within **20%** of each other in file count, consider it ambiguous — ask the user to specify rather than guessing.

---

## Command Construction Best Practices

### Follow Exact Command Structure
```bash
cd <QSE_CLI_DIR> && ./cli.sh [parameters]
```

**Never do:**
```bash
./cli.sh [parameters]                           # ❌ missing cd
<QSE_CLI_DIR>/cli.sh [params] # ❌ wrong path format
```

### Parameter Order
Maintain consistent parameter order:
1. `-i [input_path]`
2. `-l [language]`
3. `-cf [class_path]` (Java only)
4. `-da` (Cryptographic Analytics only)

### Java Class File Path Search Order
For Java projects, search for class files in this priority order:

| Priority | Path | Build Tool |
|---|---|---|
| 1 | `target/classes` | Maven |
| 2 | `build/classes/java/main` | Gradle |
| 3 | `out/production` | IntelliJ IDEA |
| 4 | `bin` | Eclipse |
| 5 | Input path | Fallback |

### Flag Usage Rules (Strict)
| Flag | When to Use | When to Exclude |
|---|---|---|
| `-da` | Java Cryptographic Analytics ONLY | API Discovery, non-Java |
| `-cf` | Java Cryptographic Analytics ONLY | API Discovery, non-Java |

---

## Execution Best Practices

### Execute Commands Sequentially
For Java projects requiring both scans:
1. Execute Cryptographic Analytics command → wait for completion
2. Execute API Discovery command → wait for completion

### Monitor for Errors
| Error | Action |
|---|---|
| Path not found | Verify input path exists |
| Permission denied | Check file permissions |
| Command not found | Verify QSE installation path |

---

## User Communication Best Practices

### Be Clear About Scan Types
**For Java:**
```
"Running complete quantum readiness assessment for Java project:
1. Cryptographic Analytics scan (analyzing bytecode)
2. API Discovery scan (analyzing source code)"
```

**For other languages:**
```
"Running API Discovery scan for [language] project to identify
quantum-vulnerable cryptographic APIs."
```

### Confirm Completion Simply
```
"[Scan type] completed successfully for [language] project.
Results are available in the QSE output directory."
```

### Explain Limitations Clearly
If a user requests Cryptographic Analytics for a non-Java language:
```
"Cryptographic Analytics is only available for Java projects. For [language]
projects, I can run API Discovery scan which identifies quantum-vulnerable
cryptographic API usage."
```

---

## Error Handling Best Practices

### Graceful Degradation
When class files aren't found for Java, use the input path as fallback for `-cf` rather than failing. QSE can still perform useful analysis without compiled class files.

### Provide Actionable Error Messages
| ❌ Bad | ✅ Good |
|---|---|
| "Scan failed" | "Scan failed because the specified directory doesn't exist. Please verify the path: /path/to/project" |

### Validate Before Executing
- [ ] Input path exists
- [ ] Language is supported
- [ ] For Java: class file path search attempted
- [ ] Command structure is correct

---

## Workflow Optimization
- **Minimize tool calls:** Use one `list_files` call with `recursive=true` to get the full project structure, then analyze locally for language and class file detection
- **Cache detection results:** Once language is detected, don't re-detect for subsequent scans in the same session
- **Batch Java scan planning:** Prepare both Java commands before executing to ensure consistency

---

## Quality Checklist

### Before Execution
- [ ] Language detected or specified by user
- [ ] Input path verified to exist
- [ ] For Java: class file path determined
- [ ] Command structure validated
- [ ] Correct flags for scan type

### During Execution
- [ ] Commands executed sequentially
- [ ] Each command completion confirmed
- [ ] Errors handled appropriately

### After Execution
- [ ] User informed of completion
- [ ] Scan type(s) clearly stated
- [ ] No attempt to parse QSE output
- [ ] Results location mentioned

---

## Common Pitfalls

| Mistake | Why Wrong | Correct Approach |
|---|---|---|
| Running only API Discovery for Java | Misses deep bytecode analysis | Always run both scans for Java |
| Including `-da` for API Discovery | `-da` is only for Cryptographic Analytics | Only include `-da` for Crypto Analytics |
| Using `-cf` for non-Java languages | Class files are Java-specific | Only use `-cf` for Java Crypto Analytics |
| Assuming language without detection | Leads to wrong scan config and failures | Always detect via `list_files` |
| Using relative paths in commands | May not resolve after `cd` to QSE dir | Use absolute paths |
| Interpreting QSE output | QSE generates its own comprehensive reports | Simply confirm scan completion |

---

## Mode Boundaries
- **In scope:** Detecting language, constructing commands, executing scans
- **Out of scope:** Explaining quantum computing theory, recommending cryptographic algorithms
- **Tool permissions:** `read` and `execute` (and `mcp` for QCM) only — do not attempt file edits
