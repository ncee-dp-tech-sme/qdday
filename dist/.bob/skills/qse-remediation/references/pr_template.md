# Pull Request (PR) Description Template & Guidelines for QSE Remediation
<!-- Created: Mon Nov 23 20:42:52 CET 2026 - Implemented Recommendation 6 (Structured PR Template) -->

This guide defines the standardized pull request format for cryptographic remediations performed via the `qse-remediation` skill.

When the user asks to generate a pull request description, create a PR, or summarize changes for code review, read `qs_explorer_result/remediation/state.json`, `changelog.md`, and `remediation_report.md` to populate the template below.

---

## Branch Naming Convention

Use clear, standardized branch names:
- Single file / focused fix: `fix/crypto-<algorithm-or-cwe>-<file-slug>` (e.g., `fix/crypto-rsa-user-auth`)
- Batch remediation: `fix/crypto-vulnerabilities-batch-remediation`

---

## PR Description Template

```markdown
## 🔐 Cryptographic Security Remediation: Quantum-Safe & Modernization Updates

### Summary
Remediated **[TOTAL_COUNT]** cryptographic vulnerabilities across **[FILE_COUNT]** files identified by Quantum Safe Explorer (QSE) scan.
All changes follow safe SDLC practices with pre-change backup copies, user-approved proposals, inline rationale comments, and test validation records.

- **Target Repository:** `[REPOSITORY_URL_OR_NAME]`
- **Scan Date / Assessment:** `[SCAN_DATE]`
- **Remediation State Reference:** `qs_explorer_result/remediation/state.json`

### Modified Files Overview
| File Path | Findings Resolved | Severity Breakdown | Status |
| :--- | :--- | :--- | :--- |
| `path/to/file1.ext` | `F-001`, `F-002` | 1 Critical, 1 Medium | Remediated & Validated |
| `path/to/file2.ext` | `F-003` | 1 High | Remediated & Validated |

---

### Remediated Vulnerabilities Breakdown

#### 1. [Vulnerability Category / Algorithm Name, e.g., Quantum-Vulnerable RSA Key Exchange]
- **Finding ID(s):** `F-001`, `F-002`
- **CWE:** CWE-327 (Use of a Broken or Risky Cryptographic Algorithm) / CWE-326 (Inadequate Encryption Strength)
- **Affected Locations:**
  - `path/to/file1.ext` (lines 45-52)
  - `path/to/file2.ext` (lines 12-18)

**Why This Was Vulnerable:**
[Explain the cryptographic weakness, e.g., RSA with Shor's algorithm vulnerability, insufficient key size, or lack of forward secrecy].

**Fix Applied & Behavior Impact:**
- **Change:** Replaced classical RSA key transport with ML-KEM (FIPS 203) / upgraded key size to >= 3072-bit with crypto-agile abstraction.
- **Behavior Impact:** [NONE / BEHAVIOR-CHANGING - describe ciphertext format, dependency changes, or peer compatibility requirements].

**Standards & References:**
- NIST FIPS 203 (*Module-Lattice-Based Key-Encapsulation Mechanism Standard*)
- NIST SP 800-175B Rev. 1 (*Guideline for Using Cryptographic Standards*)
- [Optional external reference / URL if researched]

---

#### 2. [Vulnerability Category / Algorithm Name, e.g., Deprecated Hash Function (MD5/SHA-1)]
- **Finding ID(s):** `F-003`
- **CWE:** CWE-328 (Use of Weak Hash)
- **Affected Locations:**
  - `path/to/file3.ext` (line 78)

**Why This Was Vulnerable:**
[Explain vulnerability: collision attacks against MD5/SHA-1, disallowed under NIST SP 800-131A].

**Fix Applied & Behavior Impact:**
- **Change:** Replaced `hashlib.md5()` / `MessageDigest.getInstance("MD5")` with SHA-256 (`hashlib.sha256()`).
- **Behavior Impact:** Digest size changes from 128 bits to 256 bits. DB column or API verification updated.

**Standards & References:**
- NIST SP 800-107 Rev. 1 (*Recommendation for Applications Using Approved Hash Algorithms*)
- OWASP Cryptographic Storage Cheat Sheet

---

### Security Impact Assessment

| Dimension | Before Remediation | After Remediation |
| :--- | :--- | :--- |
| **Quantum Attack Resistance** | Vulnerable to Shor's algorithm for key exchange / signing. | Migrated to PQC algorithms (ML-KEM/ML-DSA) or hardened classical keys with migration path. |
| **Cipher & Mode Security** | Weak ciphers (e.g., DES/3DES) or unauthenticated modes (ECB/CBC without MAC). | Modern AEAD mode (AES-256-GCM / ChaCha20-Poly1305) with unique random nonces. |
| **Secrets & Key Management** | Hard-coded keys/salts or deterministic PRNG. | Cryptographically secure random generators (CSPRNG) and runtime environment loading (`.env`). |
| **Auditability & Agility** | Fixed algorithm literals hard-coded across multiple modules. | Crypto-agile configuration and centralized parameter validation. |

---

### Changes Made Across All Files
- [x] Resolved [X] identified scanner findings across [Y] source files.
- [x] Added inline rationale comments with timestamps (`date`) above each modified code block.
- [x] Stored pristine pre-change file copies in `qs_explorer_result/remediation/originals/`.
- [x] Avoided hardcoded secrets by loading configuration via `.env` (with `.env.example` templates).
- [x] Documented all behavior-changing impacts and migration considerations.

---

### Testing & Validation Results
- [x] **Unit & Integration Tests:** Executed test suite (`[TEST_COMMAND]`) — Exit Code `0` (Passed).
- [x] **Syntax & Linting Checks:** Executed linter/compiler checks (`[LINT_COMMAND]`) — Passed.
- [ ] **QSE Rescan:** Recommend executing QSE scan rescan to confirm zero remaining vulnerable findings.

---

### Standards & Compliance Summary
- ✅ **NIST SP 800-175B Rev. 1** Compliant symmetric and asymmetric algorithm selections.
- ✅ **FIPS 203 / 204 / 205** Ready for post-quantum key encapsulation and digital signatures.
- ✅ **OWASP Top 10 (A02:2021 – Cryptographic Failures)** Addressed insecure hashing, ciphers, and static seeds.
- ✅ **FIPS 140-3** Compatible cryptographic parameters and approved key lengths.
```

---

## Instructions for Bob when Generating PR Descriptions

1. Extract finding IDs, severities, and files from `qs_explorer_result/remediation/state.json`.
2. Extract the unified diffs and validations from `qs_explorer_result/remediation/remediation_report.md`.
3. Fill in every bracketed placeholder (e.g. `[TOTAL_COUNT]`, `[FILE_COUNT]`).
4. If permission-gated web research was performed for novel findings, include the **Research Methodology & Sources** section with exact query terms and accessed dates.
5. Present the generated markdown in chat or write it to a PR description upon user request.
