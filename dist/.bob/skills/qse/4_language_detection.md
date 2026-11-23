# QSE Language Detection Guide

## Overview
Rules and strategies for automatically detecting the primary programming language of a project to determine the appropriate QSE scan configuration.

---

## Supported Languages

| Language | Extension | QSE Flag | Scan Types |
|---|---|---|---|
| Java | `.java` | `-l .java` | Cryptographic Analytics + API Discovery |
| Go | `.go` | `-l .go` | API Discovery only |
| Dart | `.dart` | `-l .dart` | API Discovery only |
| Python | `.py` | `-l .py` | API Discovery only |
| C++ | `.cpp` | `-l .cpp` | API Discovery only (also covers `.cc`, `.cxx`, `.c++`) |

> **Note:** Java is the only language that supports Cryptographic Analytics and therefore requires the `-cf` class file path parameter.

---

## Detection Strategy

<Steps>
<Step>

### Step 1: Use `list_files` Tool
Get a recursive listing of all files in the project directory:
```
list_files(path=project_root, recursive=true)
```

</Step>
<Step>

### Step 2: Count File Extensions
Count occurrences of each supported extension. **Exclude** the following directories:
```
node_modules/  vendor/  .git/  build/  dist/  target/  __pycache__/  .venv/  venv/
```

Count these extensions:
- `.java`
- `.go`
- `.dart`
- `.py`
- `.cpp` (also `.cc`, `.cxx`, `.c++`, `.h`, `.hpp`)

</Step>
<Step>

### Step 3: Identify Primary Language
- Language with the **highest count** of source files is primary
- If counts are close (within 20%), check for language-specific markers
- If still ambiguous, **ask the user** to specify

</Step>
<Step>

### Step 4: Verify with Language Markers

| Language | Markers |
|---|---|
| Java | `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`, `.classpath`, `.idea/` |
| Go | `go.mod`, `go.sum`, `Gopkg.toml` |
| Dart | `pubspec.yaml`, `pubspec.lock`, `.dart_tool/` |
| Python | `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile`, `poetry.lock` |
| C++ | `CMakeLists.txt`, `Makefile`, `*.vcxproj`, `configure.ac` |

</Step>
</Steps>

---

## Detection Algorithms

### Simple Count Algorithm
```
1. Get recursive file listing
2. Initialize counters for each extension
3. For each file:
   - If file is in excluded directory → skip
   - If .java extension → increment java_count
   - If .go extension → increment go_count
   - If .dart extension → increment dart_count
   - If .py extension → increment python_count
   - If .cpp / .cc / .cxx extension → increment cpp_count
4. Return language with highest count
5. If no files found → return null (ask user)
```

### Weighted Detection Algorithm (Preferred)
```
1. Perform simple count algorithm
2. Check for language-specific markers:
   - pom.xml or build.gradle present → boost Java score
   - go.mod present → boost Go score
   - pubspec.yaml present → boost Dart score
   - requirements.txt or setup.py present → boost Python score
   - CMakeLists.txt present → boost C++ score
3. Check source file locations:
   - Files in src/main/java/ → strongly indicates Java
   - Files in cmd/ or pkg/ → indicates Go
   - Files in lib/*.dart → indicates Dart
   - Files in src/*.py → indicates Python
4. Return language with highest weighted score
5. If ambiguous (scores within 20%) → ask user
```

---

## Directory Patterns

### Java
```
src/main/java/   — Main source files
src/test/java/   — Test files
target/          — Build output (Maven)
build/           — Build output (Gradle)
```
Strong indicators: `src/main/java/com/`, `src/main/java/org/`

### Go
```
cmd/      — Command line applications
pkg/      — Library packages
internal/ — Private packages
vendor/   — Dependencies
```
Strong indicators: `main.go` in `cmd/`, `go.mod` in root

### Dart
```
lib/  — Library code
bin/  — Executables
test/ — Tests
web/  — Web files (Flutter)
```
Strong indicators: `pubspec.yaml` in root, `lib/main.dart`

### Python
```
src/ or package_name/ — Source code
tests/                 — Test files
venv/ or .venv/        — Virtual environment
```
Strong indicators: `setup.py` or `pyproject.toml` in root, `__init__.py` files

### C++
```
src/     — Source files
include/ — Header files
build/   — Build output
lib/     — Libraries
```
Strong indicators: `CMakeLists.txt`, `.h` and `.cpp` file pairs

---

## Special Cases

### Polyglot Project (Multiple Languages)
**Example:** Java backend + Python scripts

1. Identify dominant language by file count
2. If Java:Python > 3:1 → default to Java
3. Otherwise → ask user which language to scan

### No Source Files Found
1. Report that no supported language was detected
2. List supported languages: Java, Go, Dart, Python, C++
3. Ask user to specify language or provide correct path

### Test Files Only
1. Count test files to determine language
2. Warn user that only test files were found
3. Proceed with detected language

### Ambiguous C++ (Mixed Extensions)
- Count `.cpp`, `.cc`, `.cxx` together
- Use `.cpp` as the standard extension for QSE flag
- QSE will scan all C++ variants

---

## Validation Rules
- Always verify detected language makes sense for the project structure
- If file count is very low (< 5 files), consider asking user for confirmation
- If multiple languages have similar counts (within 20%), check for markers
- **Never assume language without evidence from the file system**
- When in doubt, ask the user rather than guessing

---

## Fallback: Ask User
When language detection fails or is ambiguous:

```
"I couldn't automatically detect the programming language of this project.
Which language should I scan for quantum safety?"
```

**Options to present:**
- Java (`.java`) — Supports both Cryptographic Analytics and API Discovery
- Go (`.go`) — API Discovery scan
- Python (`.py`) — API Discovery scan
- Dart (`.dart`) — API Discovery scan
- C++ (`.cpp`) — API Discovery scan
