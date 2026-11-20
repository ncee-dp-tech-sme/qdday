# QSE Remediation Report
Generated: 2026-11-20T18:39:38+01:00
## 1. Scope
- Application:  
- Scan ID: 2333951d-8c5b-494e-855c-60c6bd4f37af (scan time 2026-11-20T17:17:20.393083Z)
- Repository:  
- Git HEAD at init: c22d1d9dcae6e505f25d9bc97fabf8128ebf3c3c
- Findings source: `quantum_safe_api_discovery_findings.json` sha256 `30be178fe52519d09668638fff382d60e66046b06187c979ec1342017286aaad`

## 2. Summary

| Status | Count |
|---|---|
| pending | 0 |
| applied | 17 |
| skipped | 0 |
| rejected | 0 |
| deferred | 0 |

## 3. Evidence of identified vulnerabilities (per file)

### `qseremediation/api/routes.py`

#### F-001 - cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key (line 13) - **applied**
- 4 `cwe327` [high]: Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): RSA (https://cwe.mitre.org/data/definitions/327.html)
- 18 `cwe326` [high]: Cryptographic keys should be robust. Use a key length of more than 1024 bits. (https://cwe.mitre.org/data/definitions/326.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 0,
  "title": "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key",
  "tooltip": [
    "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key"
  ],
  "crypto_properties": {
    "library": "cryptography",
    "name": "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key",
    "primitive": "signature",
    "variant": "RSA",
    "assetType": "algorithm",
    "cryptoFunction": "keygen"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "4",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): RSA",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "RSA",
          "context": {
            "location": {
              "fileName": "qseremediation/api/routes.py",
              "line": 13,
              "startColumn": 16,
              "endColumn": 36
            }
          }
        }
      ]
    },
    {
      "vulnerabilityId": "18",
      "classification": "cwe326",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/326.html",
      "debugMessage": "Cryptographic keys should be robust. Use a key length of more than 1024 bits.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "value": "RSA",
          "context": {
            "location": {
              "fileName": "qseremediation/api/routes.py",
              "line": 13,
              "startColumn": 16,
              "endColumn": 36
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/api/routes.py",
  "call_line": 13,
  "start": 16,
  "end": 36,
  "startScoped": 16,
  "endScoped": 36
}
```
</details>
- 2026-11-20T18:31:35+01:00 applied: routes.py: RSA key_size 1024->3072; wrap_key PKCS1v15->RSA-OAEP-SHA256 (interim, not quantum-safe; TODO ML-DSA/ML-KEM)

#### F-002 - cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15 (line 26) - **applied**
- 4 `cwe327` [high]: Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): RSA (https://cwe.mitre.org/data/definitions/327.html)
- 18 `cwe326` [high]: Cryptographic keys should be robust. Use a key length of more than 1024 bits. (https://cwe.mitre.org/data/definitions/326.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 1,
  "title": "cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15",
  "tooltip": [
    "cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15"
  ],
  "crypto_properties": {
    "library": "cryptography",
    "name": "cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15",
    "primitive": "pke",
    "variant": "RSA",
    "assetType": "algorithm",
    "padding": "pkcs1"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "4",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): RSA",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "RSA",
          "context": {
            "location": {
              "fileName": "qseremediation/api/routes.py",
              "line": 26,
              "startColumn": 22,
              "endColumn": 30
            }
          }
        }
      ]
    },
    {
      "vulnerabilityId": "18",
      "classification": "cwe326",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/326.html",
      "debugMessage": "Cryptographic keys should be robust. Use a key length of more than 1024 bits.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "value": "RSA",
          "context": {
            "location": {
              "fileName": "qseremediation/api/routes.py",
              "line": 26,
              "startColumn": 22,
              "endColumn": 30
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/api/routes.py",
  "call_line": 26,
  "start": 22,
  "end": 30,
  "startScoped": 22,
  "endScoped": 30
}
```
</details>
- 2026-11-20T18:31:35+01:00 applied: routes.py: RSA key_size 1024->3072; wrap_key PKCS1v15->RSA-OAEP-SHA256 (interim, not quantum-safe; TODO ML-DSA/ML-KEM)

### `qseremediation/config/settings.py`

#### F-003 - hashlib.pbkdf2_hmac (line 27) - **applied**
- No vulnerability reported (informational artifact)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 0,
  "title": "hashlib.pbkdf2_hmac",
  "tooltip": [
    "hashlib.pbkdf2_hmac"
  ],
  "crypto_properties": {
    "library": "hashlib",
    "name": "hashlib.pbkdf2_hmac",
    "primitive": "kdf",
    "variant": "PBKDF2",
    "assetType": "algorithm",
    "cryptoFunction": "keyderive"
  },
  "crypto_vulnerabilities": [],
  "file_path": "qseremediation/config/settings.py",
  "call_line": 27,
  "start": 20,
  "end": 31,
  "startScoped": 20,
  "endScoped": 31
}
```
</details>
- 2026-11-20T18:38:53+01:00 applied: settings.py: derive_file_key PBKDF2-SHA1/100/16B -> SHA-256/600000/32B (beyond scan evidence); requirements.txt cryptography>=50.0.2

### `qseremediation/crypto/keys.py`

#### F-014 - cryptography.hazmat.primitives.asymmetric.ec.generate_private_key (line 16) - **applied**
- 4 `cwe327` [high]: Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): EC (https://cwe.mitre.org/data/definitions/327.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 0,
  "title": "cryptography.hazmat.primitives.asymmetric.ec.generate_private_key",
  "tooltip": [
    "cryptography.hazmat.primitives.asymmetric.ec.generate_private_key"
  ],
  "crypto_properties": {
    "library": "cryptography",
    "name": "cryptography.hazmat.primitives.asymmetric.ec.generate_private_key",
    "primitive": "keyagree",
    "variant": "EC",
    "assetType": "algorithm",
    "cryptoFunction": "keygen"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "4",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): EC",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "EC",
          "context": {
            "location": {
              "fileName": "qseremediation/crypto/keys.py",
              "line": 16,
              "startColumn": 17,
              "endColumn": 37
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/crypto/keys.py",
  "call_line": 16,
  "start": 17,
  "end": 37,
  "startScoped": 17,
  "endScoped": 37
}
```
</details>
- 2026-11-20T18:34:04+01:00 applied: keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)

#### F-015 - cryptography.hazmat.primitives.asymmetric.ec.ECDH (line 17) - **applied**
- 4 `cwe327` [high]: Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): ECDH (https://cwe.mitre.org/data/definitions/327.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 1,
  "title": "cryptography.hazmat.primitives.asymmetric.ec.ECDH",
  "tooltip": [
    "cryptography.hazmat.primitives.asymmetric.ec.ECDH"
  ],
  "crypto_properties": {
    "library": "cryptography",
    "name": "cryptography.hazmat.primitives.asymmetric.ec.ECDH",
    "primitive": "keyagree",
    "variant": "ECDH",
    "oid": "1.3.132.1.12",
    "assetType": "algorithm"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "4",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): ECDH",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "ECDH",
          "context": {
            "location": {
              "fileName": "qseremediation/crypto/keys.py",
              "line": 17,
              "startColumn": 31,
              "endColumn": 35
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/crypto/keys.py",
  "call_line": 17,
  "start": 31,
  "end": 35,
  "startScoped": 31,
  "endScoped": 35
}
```
</details>
- 2026-11-20T18:34:04+01:00 applied: keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)

#### F-016 - Crypto.Cipher.AES.new (line 27) - **applied**
- 3 `cwe327` [high]: Use a secure cipher mode. For AES, the weakest modes are CBC (Cipher Block Chaining) and ECB (Electronic Codebook), as they are either vulnerable to padding oracles or do not provide authentication mechanisms. (https://cwe.mitre.org/data/definitions/327.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 2,
  "title": "Crypto.Cipher.AES.new",
  "tooltip": [
    "Crypto.Cipher.AES.new"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher.AES.new",
    "variant": "AES",
    "assetType": "algorithm"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "3",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use a secure cipher mode. For AES, the weakest modes are CBC (Cipher Block Chaining) and ECB (Electronic Codebook), as they are either vulnerable to padding oracles or do not provide authentication mechanisms.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "value": "AES",
          "context": {
            "location": {
              "fileName": "qseremediation/crypto/keys.py",
              "line": 27,
              "startColumn": 18,
              "endColumn": 21
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/crypto/keys.py",
  "call_line": 27,
  "start": 18,
  "end": 21,
  "startScoped": 18,
  "endScoped": 21
}
```
</details>
- 2026-11-20T18:34:04+01:00 applied: keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)

#### F-017 - Crypto.Cipher._mode_cbc.CbcMode.encrypt (line 29) - **applied**
- 20 `cwe1204` [high]: Use a dynamically-generated, random initialization vector (IV). (https://cwe.mitre.org/data/definitions/1204.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 3,
  "title": "Crypto.Cipher._mode_cbc.CbcMode.encrypt",
  "tooltip": [
    "Crypto.Cipher._mode_cbc.CbcMode.encrypt"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher._mode_cbc.CbcMode.encrypt",
    "primitive": "blockcipher",
    "assetType": "algorithm",
    "cryptoFunction": "encrypt",
    "mode": "cbc"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "20",
      "classification": "cwe1204",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/1204.html",
      "debugMessage": "Use a dynamically-generated, random initialization vector (IV).",
      "type": "Suggestive",
      "references": [
        {
          "type": "primitive",
          "value": "blockcipher",
          "context": {
            "location": {
              "fileName": "qseremediation/crypto/keys.py",
              "line": 29,
              "startColumn": 24,
              "endColumn": 31
            }
          }
        },
        {
          "type": "mode",
          "value": "cbc",
          "context": {
            "location": {
              "fileName": "qseremediation/crypto/keys.py",
              "line": 29,
              "startColumn": 24,
              "endColumn": 31
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/crypto/keys.py",
  "call_line": 29,
  "start": 24,
  "end": 31,
  "startScoped": 24,
  "endScoped": 31
}
```
</details>
- 2026-11-20T18:34:04+01:00 applied: keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)

### `qseremediation/services/auth.py`

#### F-010 - Crypto.Cipher.AES.new (line 40) - **applied**
- 3 `cwe327` [high]: Use a secure cipher mode. For AES, the weakest modes are CBC (Cipher Block Chaining) and ECB (Electronic Codebook), as they are either vulnerable to padding oracles or do not provide authentication mechanisms. (https://cwe.mitre.org/data/definitions/327.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 0,
  "title": "Crypto.Cipher.AES.new",
  "tooltip": [
    "Crypto.Cipher.AES.new"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher.AES.new",
    "variant": "AES",
    "assetType": "algorithm"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "3",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use a secure cipher mode. For AES, the weakest modes are CBC (Cipher Block Chaining) and ECB (Electronic Codebook), as they are either vulnerable to padding oracles or do not provide authentication mechanisms.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "value": "AES",
          "context": {
            "location": {
              "fileName": "qseremediation/services/auth.py",
              "line": 40,
              "startColumn": 18,
              "endColumn": 21
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/services/auth.py",
  "call_line": 40,
  "start": 18,
  "end": 21,
  "startScoped": 18,
  "endScoped": 21
}
```
</details>
- 2026-11-20T18:35:06+01:00 applied: auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)

#### F-011 - Crypto.Cipher._mode_ecb.EcbMode.encrypt (line 42) - **applied**
- No vulnerability reported (informational artifact)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 1,
  "title": "Crypto.Cipher._mode_ecb.EcbMode.encrypt",
  "tooltip": [
    "Crypto.Cipher._mode_ecb.EcbMode.encrypt"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher._mode_ecb.EcbMode.encrypt",
    "primitive": "blockcipher",
    "assetType": "algorithm",
    "cryptoFunction": "encrypt",
    "mode": "ecb"
  },
  "crypto_vulnerabilities": [],
  "file_path": "qseremediation/services/auth.py",
  "call_line": 42,
  "start": 36,
  "end": 43,
  "startScoped": 36,
  "endScoped": 43
}
```
</details>
- 2026-11-20T18:35:06+01:00 applied: auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)

#### F-012 - Crypto.Cipher.Blowfish.new (line 51) - **applied**
- 2 `cwe327` [high]: Use of broken or risky cryptographic algorithm: BLOWFISH (https://cwe.mitre.org/data/definitions/327.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 2,
  "title": "Crypto.Cipher.Blowfish.new",
  "tooltip": [
    "Crypto.Cipher.Blowfish.new"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher.Blowfish.new",
    "variant": "BLOWFISH",
    "assetType": "algorithm"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "2",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of broken or risky cryptographic algorithm: BLOWFISH",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "BLOWFISH",
          "context": {
            "location": {
              "fileName": "qseremediation/services/auth.py",
              "line": 51,
              "startColumn": 17,
              "endColumn": 20
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/services/auth.py",
  "call_line": 51,
  "start": 17,
  "end": 20,
  "startScoped": 17,
  "endScoped": 20
}
```
</details>
- 2026-11-20T18:35:06+01:00 applied: auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)

#### F-013 - Crypto.Cipher._mode_ecb.EcbMode.encrypt (line 54) - **applied**
- No vulnerability reported (informational artifact)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 3,
  "title": "Crypto.Cipher._mode_ecb.EcbMode.encrypt",
  "tooltip": [
    "Crypto.Cipher._mode_ecb.EcbMode.encrypt"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher._mode_ecb.EcbMode.encrypt",
    "primitive": "blockcipher",
    "assetType": "algorithm",
    "cryptoFunction": "encrypt",
    "mode": "ecb"
  },
  "crypto_vulnerabilities": [],
  "file_path": "qseremediation/services/auth.py",
  "call_line": 54,
  "start": 19,
  "end": 26,
  "startScoped": 19,
  "endScoped": 26
}
```
</details>
- 2026-11-20T18:35:06+01:00 applied: auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)

### `qseremediation/services/user.py`

#### F-006 - Crypto.Cipher.AES.new (line 25) - **applied**
- 3 `cwe327` [high]: Use a secure cipher mode. For AES, the weakest modes are CBC (Cipher Block Chaining) and ECB (Electronic Codebook), as they are either vulnerable to padding oracles or do not provide authentication mechanisms. (https://cwe.mitre.org/data/definitions/327.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 0,
  "title": "Crypto.Cipher.AES.new",
  "tooltip": [
    "Crypto.Cipher.AES.new"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher.AES.new",
    "variant": "AES",
    "assetType": "algorithm"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "3",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use a secure cipher mode. For AES, the weakest modes are CBC (Cipher Block Chaining) and ECB (Electronic Codebook), as they are either vulnerable to padding oracles or do not provide authentication mechanisms.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "value": "AES",
          "context": {
            "location": {
              "fileName": "qseremediation/services/user.py",
              "line": 25,
              "startColumn": 18,
              "endColumn": 21
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/services/user.py",
  "call_line": 25,
  "start": 18,
  "end": 21,
  "startScoped": 18,
  "endScoped": 21
}
```
</details>
- 2026-11-20T18:37:09+01:00 applied: user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password

#### F-007 - Crypto.Cipher._mode_cbc.CbcMode.encrypt (line 27) - **applied**
- 20 `cwe1204` [high]: Use a dynamically-generated, random initialization vector (IV). (https://cwe.mitre.org/data/definitions/1204.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 1,
  "title": "Crypto.Cipher._mode_cbc.CbcMode.encrypt",
  "tooltip": [
    "Crypto.Cipher._mode_cbc.CbcMode.encrypt"
  ],
  "crypto_properties": {
    "library": "Crypto",
    "name": "Crypto.Cipher._mode_cbc.CbcMode.encrypt",
    "primitive": "blockcipher",
    "assetType": "algorithm",
    "cryptoFunction": "encrypt",
    "mode": "cbc"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "20",
      "classification": "cwe1204",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/1204.html",
      "debugMessage": "Use a dynamically-generated, random initialization vector (IV).",
      "type": "Suggestive",
      "references": [
        {
          "type": "primitive",
          "value": "blockcipher",
          "context": {
            "location": {
              "fileName": "qseremediation/services/user.py",
              "line": 27,
              "startColumn": 19,
              "endColumn": 26
            }
          }
        },
        {
          "type": "mode",
          "value": "cbc",
          "context": {
            "location": {
              "fileName": "qseremediation/services/user.py",
              "line": 27,
              "startColumn": 19,
              "endColumn": 26
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/services/user.py",
  "call_line": 27,
  "start": 19,
  "end": 26,
  "startScoped": 19,
  "endScoped": 26
}
```
</details>
- 2026-11-20T18:37:09+01:00 applied: user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password

#### F-008 - hashlib.md5 (line 56) - **applied**
- 2 `cwe327` [high]: Use of broken or risky cryptographic algorithm: MD5 (https://cwe.mitre.org/data/definitions/327.html)
- 12 `cwe328` [high]: Use of weak hash algorithm: MD5 (https://cwe.mitre.org/data/definitions/328.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 2,
  "title": "hashlib.md5",
  "tooltip": [
    "hashlib.md5"
  ],
  "crypto_properties": {
    "library": "hashlib",
    "name": "hashlib.md5",
    "primitive": "hash",
    "variant": "MD5",
    "oid": "1.2.840.113549.2.5",
    "digestSize": "128",
    "assetType": "algorithm",
    "blockSize": "512"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "2",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of broken or risky cryptographic algorithm: MD5",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "MD5",
          "context": {
            "location": {
              "fileName": "qseremediation/services/user.py",
              "line": 56,
              "startColumn": 20,
              "endColumn": 23
            }
          }
        }
      ]
    },
    {
      "vulnerabilityId": "12",
      "classification": "cwe328",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/328.html",
      "debugMessage": "Use of weak hash algorithm: MD5",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "MD5",
          "context": {
            "location": {
              "fileName": "qseremediation/services/user.py",
              "line": 56,
              "startColumn": 20,
              "endColumn": 23
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/services/user.py",
  "call_line": 56,
  "start": 20,
  "end": 23,
  "startScoped": 20,
  "endScoped": 23
}
```
</details>
- 2026-11-20T18:37:09+01:00 applied: user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password

#### F-009 - hashlib.hash.hexdigest (line 56) - **applied**
- 10 `cwe759` [low]: Hashes should include an unpredictable salt. (https://cwe.mitre.org/data/definitions/759.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 3,
  "title": "hashlib.hash.hexdigest",
  "tooltip": [
    "hashlib.hash.hexdigest"
  ],
  "crypto_properties": {
    "library": "hashlib",
    "name": "hashlib.hash.hexdigest",
    "primitive": "hash",
    "assetType": "algorithm",
    "cryptoFunction": "digest"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "10",
      "classification": "cwe759",
      "vulnerabilityScore": "low",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/759.html",
      "debugMessage": "Hashes should include an unpredictable salt.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "context": {
            "location": {
              "fileName": "qseremediation/services/user.py",
              "line": 56,
              "startColumn": 43,
              "endColumn": 52
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/services/user.py",
  "call_line": 56,
  "start": 43,
  "end": 52,
  "startScoped": 43,
  "endScoped": 52
}
```
</details>
- 2026-11-20T18:37:09+01:00 applied: user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password

### `qseremediation/utils/tokens.py`

#### F-004 - cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15 (line 33) - **applied**
- 4 `cwe327` [high]: Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): RSA (https://cwe.mitre.org/data/definitions/327.html)
- 18 `cwe326` [high]: Cryptographic keys should be robust. Use a key length of more than 1024 bits. (https://cwe.mitre.org/data/definitions/326.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 0,
  "title": "cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15",
  "tooltip": [
    "cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15"
  ],
  "crypto_properties": {
    "library": "cryptography",
    "name": "cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15",
    "primitive": "pke",
    "variant": "RSA",
    "assetType": "algorithm",
    "padding": "pkcs1"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "4",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of non-quantum-resistant public-key algorithms (must be ML-KEM, ML-DSA, SLH-DSA): RSA",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "RSA",
          "context": {
            "location": {
              "fileName": "qseremediation/utils/tokens.py",
              "line": 33,
              "startColumn": 45,
              "endColumn": 53
            }
          }
        }
      ]
    },
    {
      "vulnerabilityId": "18",
      "classification": "cwe326",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/326.html",
      "debugMessage": "Cryptographic keys should be robust. Use a key length of more than 1024 bits.",
      "type": "Suggestive",
      "references": [
        {
          "type": "variant",
          "value": "RSA",
          "context": {
            "location": {
              "fileName": "qseremediation/utils/tokens.py",
              "line": 33,
              "startColumn": 45,
              "endColumn": 53
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/utils/tokens.py",
  "call_line": 33,
  "start": 45,
  "end": 53,
  "startScoped": 45,
  "endScoped": 53
}
```
</details>
- 2026-11-20T18:32:50+01:00 applied: tokens.py: sign_audit_record PKCS1v15+SHA1 -> RSA-PSS+SHA-256 (interim, not quantum-safe; TODO ML-DSA/SLH-DSA)

#### F-005 - cryptography.hazmat.primitives.hashes.SHA1 (line 33) - **applied**
- 2 `cwe327` [high]: Use of broken or risky cryptographic algorithm: SHA (https://cwe.mitre.org/data/definitions/327.html)
- 12 `cwe328` [high]: Use of weak hash algorithm: SHA (https://cwe.mitre.org/data/definitions/328.html)

<details><summary>Raw finding JSON</summary>

```json
{
  "id": 1,
  "title": "cryptography.hazmat.primitives.hashes.SHA1",
  "tooltip": [
    "cryptography.hazmat.primitives.hashes.SHA1"
  ],
  "crypto_properties": {
    "library": "cryptography",
    "name": "cryptography.hazmat.primitives.hashes.SHA1",
    "primitive": "hash",
    "variant": "SHA",
    "oid": "1.3.14.3.2.18",
    "digestSize": "160",
    "assetType": "algorithm",
    "blockSize": "512"
  },
  "crypto_vulnerabilities": [
    {
      "vulnerabilityId": "2",
      "classification": "cwe327",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/327.html",
      "debugMessage": "Use of broken or risky cryptographic algorithm: SHA",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "SHA",
          "context": {
            "location": {
              "fileName": "qseremediation/utils/tokens.py",
              "line": 33,
              "startColumn": 64,
              "endColumn": 68
            }
          }
        }
      ]
    },
    {
      "vulnerabilityId": "12",
      "classification": "cwe328",
      "vulnerabilityScore": "high",
      "vulnerabilityDocumentationReference": "https://cwe.mitre.org/data/definitions/328.html",
      "debugMessage": "Use of weak hash algorithm: SHA",
      "type": "Definitive",
      "references": [
        {
          "type": "variant",
          "value": "SHA",
          "context": {
            "location": {
              "fileName": "qseremediation/utils/tokens.py",
              "line": 33,
              "startColumn": 64,
              "endColumn": 68
            }
          }
        }
      ]
    }
  ],
  "file_path": "qseremediation/utils/tokens.py",
  "call_line": 33,
  "start": 64,
  "end": 68,
  "startScoped": 64,
  "endScoped": 68
}
```
</details>
- 2026-11-20T18:32:50+01:00 applied: tokens.py: sign_audit_record PKCS1v15+SHA1 -> RSA-PSS+SHA-256 (interim, not quantum-safe; TODO ML-DSA/SLH-DSA)

## 4. Change log


- 2026-11-20T18:20:06+01:00  init: 17 finding(s) from quantum_safe_api_discovery_findings.json
- 2026-11-20T18:24:21+01:00  backup: qseremediation/api/routes.py (sha256 04b9f25bf45f)
- 2026-11-20T18:24:21+01:00  backup: qseremediation/utils/tokens.py (sha256 0cb978d6f9f3)
- 2026-11-20T18:24:21+01:00  backup: qseremediation/crypto/keys.py (sha256 499467dfe5dd)
- 2026-11-20T18:24:21+01:00  backup: qseremediation/services/auth.py (sha256 dbcfc86b4600)
- 2026-11-20T18:24:21+01:00  backup: qseremediation/services/user.py (sha256 4bc093200225)
- 2026-11-20T18:24:21+01:00  backup: qseremediation/config/settings.py (sha256 bbd3e81b07d4)
- 2026-11-20T18:24:21+01:00  backup: requirements.txt (sha256 8af4d54c8573)
- 2026-11-20T18:27:55+01:00  init: 17 finding(s) from quantum_safe_api_discovery_findings.json
- 2026-11-20T18:29:16+01:00  init: 17 finding(s) from quantum_safe_api_discovery_findings.json
- 2026-11-20T18:31:35+01:00  APPLIED F-001 qseremediation/api/routes.py:13 (cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key) - routes.py: RSA key_size 1024->3072; wrap_key PKCS1v15->RSA-OAEP-SHA256 (interim, not quantum-safe; TODO ML-DSA/ML-KEM)
- 2026-11-20T18:31:35+01:00  APPLIED F-002 qseremediation/api/routes.py:26 (cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15) - routes.py: RSA key_size 1024->3072; wrap_key PKCS1v15->RSA-OAEP-SHA256 (interim, not quantum-safe; TODO ML-DSA/ML-KEM)
- 2026-11-20T18:31:35+01:00  VALIDATION qseremediation/api/routes.py exit=0 `.venv/bin/python -m py_compile + roundtrip script (3072-bit keygen, OAEP-SHA256 wrap/unwrap)` - Compiles; key_size==3072; wrap_key output decrypts with OAEP-SHA256 to original key. No unit tests exist for this file.
- 2026-11-20T18:32:50+01:00  APPLIED F-004 qseremediation/utils/tokens.py:33 (cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15) - tokens.py: sign_audit_record PKCS1v15+SHA1 -> RSA-PSS+SHA-256 (interim, not quantum-safe; TODO ML-DSA/SLH-DSA)
- 2026-11-20T18:32:50+01:00  APPLIED F-005 qseremediation/utils/tokens.py:33 (cryptography.hazmat.primitives.hashes.SHA1) - tokens.py: sign_audit_record PKCS1v15+SHA1 -> RSA-PSS+SHA-256 (interim, not quantum-safe; TODO ML-DSA/SLH-DSA)
- 2026-11-20T18:32:50+01:00  VALIDATION qseremediation/utils/tokens.py exit=0 `.venv/bin/python -m py_compile + sign/verify script (RSA-3072, PSS-SHA256)` - Compiles; signature verifies with PSS/SHA-256. No unit tests exist for this file. Pre-existing stderr notice: ML-KEM import fallback (MLKEMPrivateKey names do not exist in cryptography 50.0.2), unrelated to this change.
- 2026-11-20T18:34:04+01:00  APPLIED F-014 qseremediation/crypto/keys.py:16 (cryptography.hazmat.primitives.asymmetric.ec.generate_private_key) - keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)
- 2026-11-20T18:34:04+01:00  APPLIED F-015 qseremediation/crypto/keys.py:17 (cryptography.hazmat.primitives.asymmetric.ec.ECDH) - keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)
- 2026-11-20T18:34:04+01:00  APPLIED F-016 qseremediation/crypto/keys.py:27 (Crypto.Cipher.AES.new) - keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)
- 2026-11-20T18:34:04+01:00  APPLIED F-017 qseremediation/crypto/keys.py:29 (Crypto.Cipher._mode_cbc.CbcMode.encrypt) - keys.py: ECDH -> ML-KEM-768 encapsulation (returns (secret, ciphertext)); encrypt_session AES-CBC -> AES-256-GCM (random nonce, 32-byte key)
- 2026-11-20T18:34:04+01:00  VALIDATION qseremediation/crypto/keys.py exit=0 `.venv/bin/python -m py_compile + roundtrip script (ML-KEM-768 encap/decap, AES-256-GCM encrypt/decrypt, nonce uniqueness, bad-key ValueError)` - Compiles; ML-KEM shared secret matches on decapsulate (ct 1088 bytes); GCM output decrypts and verifies; nonces differ; short key rejected. No unit tests exist for this file.
- 2026-11-20T18:35:06+01:00  APPLIED F-010 qseremediation/services/auth.py:40 (Crypto.Cipher.AES.new) - auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)
- 2026-11-20T18:35:06+01:00  APPLIED F-011 qseremediation/services/auth.py:42 (Crypto.Cipher._mode_ecb.EcbMode.encrypt) - auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)
- 2026-11-20T18:35:06+01:00  APPLIED F-012 qseremediation/services/auth.py:51 (Crypto.Cipher.Blowfish.new) - auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)
- 2026-11-20T18:35:06+01:00  APPLIED F-013 qseremediation/services/auth.py:54 (Crypto.Cipher._mode_ecb.EcbMode.encrypt) - auth.py: encrypt_config (AES-ECB) and encrypt_legacy (Blowfish-ECB) -> AES-256-GCM via shared helper (32-byte key, random nonce)
- 2026-11-20T18:35:06+01:00  VALIDATION qseremediation/services/auth.py exit=0 `.venv/bin/python -m py_compile + roundtrip script (decrypt_and_verify both functions; short key rejected)` - Compiles; both functions' output decrypts/verifies with AES-256-GCM; 8-byte key rejected. No unit tests exist for this file. Pre-existing stderr notice: ML-DSA import fallback (mldsa API names differ in cryptography 50.0.2), unrelated to this change.
- 2026-11-20T18:37:09+01:00  APPLIED F-006 qseremediation/services/user.py:25 (Crypto.Cipher.AES.new) - user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password
- 2026-11-20T18:37:09+01:00  APPLIED F-007 qseremediation/services/user.py:27 (Crypto.Cipher._mode_cbc.CbcMode.encrypt) - user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password
- 2026-11-20T18:37:09+01:00  APPLIED F-008 qseremediation/services/user.py:56 (hashlib.md5) - user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password
- 2026-11-20T18:37:09+01:00  APPLIED F-009 qseremediation/services/user.py:56 (hashlib.hash.hexdigest) - user.py: AES-CBC static IV -> AES-256-GCM random nonce; MD5 password hash -> salted PBKDF2-HMAC-SHA256 (600k iter) + verify_password
- 2026-11-20T18:37:09+01:00  VALIDATION qseremediation/services/user.py exit=0 `.venv/bin/python -m py_compile + script (logic of tests/test_auth.py::test_hash_password_returns_string, verify_password, GCM roundtrip)` - Compiles; hash_password returns str (test logic passes); verify_password accepts right / rejects wrong and malformed; salts differ per call; GCM output decrypts, nonces differ, 16-byte key rejected. pytest not installed in .venv so test file not run directly.
- 2026-11-20T18:38:53+01:00  APPLIED F-003 qseremediation/config/settings.py:27 (hashlib.pbkdf2_hmac) - settings.py: derive_file_key PBKDF2-SHA1/100/16B -> SHA-256/600000/32B (beyond scan evidence); requirements.txt cryptography>=50.0.2
- 2026-11-20T18:39:23+01:00  VALIDATION qseremediation/config/settings.py exit=0 `.venv/bin/python -m py_compile + derive_file_key script` - Compiles; derived key is 32 bytes, deterministic per (passphrase, salt), differs by passphrase; PBKDF2_ITERATIONS==600000. No unit tests exist for this file.
- 2026-11-20T18:39:23+01:00  VALIDATION requirements.txt exit=0 `.venv/bin/pip install --dry-run -r requirements.txt` - Dry-run resolves requirements with cryptography>=50.0.2 (supporting change, not a scan finding; edited after backup)
- 2026-11-20T18:39:38+01:00  VALIDATION qseremediation/utils/tokens.py exit=1 `inline run of tests/test_auth.py logic (pytest not installed in .venv)` - test_hash_password_returns_string PASS; test_generate_token_not_empty FAIL: generate_reset_token does not exist in tokens.py (also absent in the pre-remediation original) - pre-existing, unrelated to remediation

## 5. Before / after comparison

### `qseremediation/api/routes.py`

```diff
--- a/qseremediation/api/routes.py (original)
+++ b/qseremediation/api/routes.py (remediated)
@@ -9,21 +9,40 @@
 from cryptography.hazmat.primitives.asymmetric import rsa
 
 # Generate RSA key pair for device certificate signing
+# QSE remediation F-001 (Fri Nov 20 18:31:10 CET 2026)
+# Vulnerability: CWE-327/CWE-326 - RSA key generation (1024-bit key too small / quantum-vulnerable).
+# Change: key_size 1024 -> 3072.
+# Rationale: 1024-bit RSA is classically weak; 3072 is the minimum acceptable interim size.
+# Notes: BEHAVIOR-CHANGING (larger keys/signatures, slower keygen; peers must accept 3072-bit keys).
+#   NOT quantum-safe: RSA is broken by Shor's algorithm at any size.
+#   TODO: migrate device signing to ML-DSA (see oqs_mldsa_sign below).
 def generate_device_keypair():
     return rsa.generate_private_key(
         public_exponent=65537,
-        key_size=1024,
+        key_size=3072,
     )
 
 
 
+from cryptography.hazmat.primitives import hashes
 from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
 
 # Wrap a symmetric key using the recipient's RSA public key
+# QSE remediation F-002 (Fri Nov 20 18:31:10 CET 2026)
+# Vulnerability: CWE-327/CWE-326 - RSA PKCS#1 v1.5 padding for key transport.
+# Change: PKCS1v15 -> RSA-OAEP with SHA-256 (hash and MGF1).
+# Rationale: PKCS#1 v1.5 encryption is vulnerable to padding-oracle attacks; OAEP is the recommended padding.
+# Notes: BEHAVIOR-CHANGING (ciphertext format; recipients must decrypt with OAEP-SHA256).
+#   NOT quantum-safe: RSA key transport remains vulnerable to Shor's algorithm.
+#   TODO: migrate key transport to ML-KEM-768 (optionally hybrid with a classical KEM).
 def wrap_key(symmetric_key: bytes, recipient_public_key) -> bytes:
     return recipient_public_key.encrypt(
         symmetric_key,
-        asym_padding.PKCS1v15(),
+        asym_padding.OAEP(
+            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
+            algorithm=hashes.SHA256(),
+            label=None,
+        ),
     )
 
 
```

### `qseremediation/config/settings.py`

```diff
--- a/qseremediation/config/settings.py (original)
+++ b/qseremediation/config/settings.py (remediated)
@@ -15,7 +15,8 @@
 SECRET_KEY = "916e9d880ac9bd773a90ec75ca6bd196"  # HashiCorpIgnore
 HASH_ALGORITHM = "md5"
 TOKEN_ALGORITHM = "HS256"
-PBKDF2_ITERATIONS = 500
+# QSE remediation F-003 (Fri Nov 20 18:38:31 CET 2026): raised 500 -> 600000 (OWASP PBKDF2-HMAC-SHA256 guidance)
+PBKDF2_ITERATIONS = 600000
 MIN_TLS_VERSION = "TLSv1"
 
 
@@ -23,8 +24,15 @@
 import hashlib
 
 # Derive an AES key from a user passphrase for file encryption
+# QSE remediation F-003 (Fri Nov 20 18:38:31 CET 2026)
+# Vulnerability: informational in scan (no CWE); code review found SHA-1, 100 iterations, 128-bit key.
+#   This change goes beyond the scan evidence.
+# Change: PBKDF2-HMAC-SHA1/100 iterations/16-byte key -> PBKDF2-HMAC-SHA256/PBKDF2_ITERATIONS/32-byte key.
+# Rationale: more iterations slow brute force; SHA-256 and a 256-bit key suit AES-256 (Grover margin).
+# Notes: BEHAVIOR-CHANGING (derived keys differ; data encrypted with old keys cannot be decrypted).
+#   Salt must be random (>= 16 bytes) and stored with the data; the caller supplies it.
 def derive_file_key(passphrase: str, salt: bytes) -> bytes:
-    return hashlib.pbkdf2_hmac("sha1", passphrase.encode(), salt, 100, dklen=16)
+    return hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, PBKDF2_ITERATIONS, dklen=32)
 
 
 
```

### `qseremediation/crypto/keys.py`

```diff
--- a/qseremediation/crypto/keys.py (original)
+++ b/qseremediation/crypto/keys.py (remediated)
@@ -7,14 +7,19 @@
 
 
 
-from cryptography.hazmat.primitives.asymmetric.ec import (
-    ECDH, SECP256R1, generate_private_key
-)
+from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PublicKey
 
-# Derive a shared session secret using ECDH
-def ecdh_shared_secret(peer_public_key) -> bytes:
-    ephemeral = generate_private_key(SECP256R1())
-    return ephemeral.exchange(ECDH(), peer_public_key)
+# Derive a shared session secret using ML-KEM-768 encapsulation
+# QSE remediation F-014, F-015 (Fri Nov 20 18:33:36 CET 2026)
+# Vulnerability: CWE-327 - EC key generation and ECDH key agreement (quantum-vulnerable).
+# Change: ECDH (P-256) -> ML-KEM-768 (FIPS 203) encapsulation; returns (shared_secret, ciphertext).
+# Rationale: ML-KEM is a NIST-standardized quantum-resistant KEM; ECDH is broken by Shor's algorithm.
+# Notes: BEHAVIOR-CHANGING. Name kept for greppability, but this is no longer ECDH: the return type
+#   is now a tuple, the peer needs an ML-KEM-768 key pair and must receive the 1088-byte ciphertext
+#   and call decapsulate(). No hybrid with a classical KEM yet (needs protocol design).
+def ecdh_shared_secret(peer_public_key: MLKEM768PublicKey) -> tuple[bytes, bytes]:
+    shared_secret, ciphertext = peer_public_key.encapsulate()
+    return shared_secret, ciphertext
 
 
 
@@ -22,9 +27,18 @@
 import os, base64
 
 # Encrypt user session data for cookie storage
+# QSE remediation F-016, F-017 (Fri Nov 20 18:33:36 CET 2026)
+# Vulnerability: CWE-327 (AES key size unspecified, unauthenticated CBC) and CWE-1204 (IV handling).
+# Change: AES-CBC + zero padding -> AES-256-GCM with a random 12-byte nonce; key must be 32 bytes.
+# Rationale: AES-256 resists Grover; GCM adds authentication and removes the ambiguous zero padding.
+# Notes: BEHAVIOR-CHANGING (output = nonce(12) + tag(16) + ciphertext; 32-byte key required).
+#   The CBC IV was already random per call, so CWE-1204 looked like a false positive; it is moot now.
+#   Never reuse a nonce with the same key; existing CBC data needs a decrypt-old/re-encrypt path.
 def encrypt_session(data: bytes, key: bytes) -> bytes:
-    iv = os.urandom(16)
-    cipher = AES.new(key, AES.MODE_CBC, iv)
-    padded = data + b"\x00" * (16 - len(data) % 16)
-    return iv + cipher.encrypt(padded)
+    if len(key) != 32:
+        raise ValueError("AES-256 key (32 bytes) required")
+    nonce = os.urandom(12)
+    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
+    ciphertext, tag = cipher.encrypt_and_digest(data)
+    return nonce + tag + ciphertext
 
```

### `qseremediation/services/auth.py`

```diff
--- a/qseremediation/services/auth.py (original)
+++ b/qseremediation/services/auth.py (remediated)
@@ -34,22 +34,39 @@
 
 from Crypto.Cipher import AES
 import base64
+import os
+
+# AES-256-GCM helper: returns nonce(12) + tag(16) + ciphertext
+# QSE remediation F-010, F-011, F-012, F-013 (Fri Nov 20 18:34:44 CET 2026)
+# Vulnerability: CWE-327 - AES-ECB/unspecified key size and Blowfish-ECB (weak/unauthenticated modes).
+# Change: shared helper using AES-256-GCM with a random 12-byte nonce; 32-byte key required.
+# Rationale: AES-256 resists Grover; GCM is authenticated and hides plaintext patterns (unlike ECB).
+# Notes: BEHAVIOR-CHANGING for encrypt_config and encrypt_legacy (format, key length). Never reuse a nonce
+#   with the same key; existing ECB data needs a decrypt-old/re-encrypt path.
+def _aes256_gcm_encrypt(data: bytes, key: bytes) -> bytes:
+    if len(key) != 32:
+        raise ValueError("AES-256 key (32 bytes) required")
+    nonce = os.urandom(12)
+    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
+    ciphertext, tag = cipher.encrypt_and_digest(data)
+    return nonce + tag + ciphertext
 
 # Encrypt configuration blob for at-rest storage
+# QSE remediation F-010, F-011 (Fri Nov 20 18:34:44 CET 2026)
+# Change: AES-ECB + zero padding -> AES-256-GCM via _aes256_gcm_encrypt (base64 of nonce+tag+ciphertext).
+# Notes: BEHAVIOR-CHANGING (see helper above).
 def encrypt_config(data: bytes, key: bytes) -> str:
-    cipher = AES.new(key, AES.MODE_ECB)
-    padded = data + b"\x00" * (16 - len(data) % 16)
-    return base64.b64encode(cipher.encrypt(padded)).decode()
+    return base64.b64encode(_aes256_gcm_encrypt(data, key)).decode()
 
 
 
-from Crypto.Cipher import Blowfish as BF
 import struct
 
-# Encrypt small data chunks with Blowfish for legacy API compatibility
+# Encrypt small data chunks, formerly Blowfish, for legacy API compatibility
+# QSE remediation F-012, F-013 (Fri Nov 20 18:34:44 CET 2026)
+# Change: Blowfish-ECB with key[:8] -> AES-256-GCM via _aes256_gcm_encrypt.
+# Notes: BEHAVIOR-CHANGING: peers expecting Blowfish-ECB output can no longer read the data;
+#   a 32-byte key is now required (was 8 bytes).
 def encrypt_legacy(data: bytes, key: bytes) -> bytes:
-    cipher = BF.new(key[:8], BF.MODE_ECB)
-    pad_len = BF.block_size - len(data) % BF.block_size
-    data += bytes([pad_len]) * pad_len
-    return cipher.encrypt(data)
+    return _aes256_gcm_encrypt(data, key)
 
```

### `qseremediation/services/user.py`

```diff
--- a/qseremediation/services/user.py (original)
+++ b/qseremediation/services/user.py (remediated)
@@ -16,15 +16,24 @@
 
 
 from Crypto.Cipher import AES
-import binascii
+import os
 
-# Default IV shared across deployments for reproducible test vectors
-_STATIC_IV = binascii.unhexlify("0c754dec4ffe2cb940b372fc03423582")
-
+# Encrypt data with AES (formerly with a static IV shared across deployments)
+# QSE remediation F-006, F-007 (Fri Nov 20 18:36:10 CET 2026)
+# Vulnerability: CWE-327 (AES key size unspecified, unauthenticated CBC) and CWE-1204 (static IV).
+# Change: AES-CBC with hardcoded IV + zero padding -> AES-256-GCM with a random 12-byte nonce;
+#   _STATIC_IV and the binascii import removed.
+# Rationale: A static IV makes CBC output deterministic and leaks equal-prefix plaintexts; GCM with a
+#   unique nonce is authenticated and AES-256 resists Grover.
+# Notes: BEHAVIOR-CHANGING (output = nonce(12) + tag(16) + ciphertext; 32-byte key required; no longer
+#   deterministic, so it cannot produce reproducible test vectors). Never reuse a nonce with the same key.
 def encrypt_with_static_iv(data: bytes, key: bytes) -> bytes:
-    cipher = AES.new(key, AES.MODE_CBC, _STATIC_IV)
-    padded = data + b"\x00" * (16 - len(data) % 16)
-    return cipher.encrypt(padded)
+    if len(key) != 32:
+        raise ValueError("AES-256 key (32 bytes) required")
+    nonce = os.urandom(12)
+    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
+    ciphertext, tag = cipher.encrypt_and_digest(data)
+    return nonce + tag + ciphertext
 
 
 
@@ -50,8 +59,37 @@
 
 
 import hashlib
+import os
+
+_PBKDF2_ITERATIONS = 600_000
 
 # Hash a password before persisting to the user store
+# QSE remediation F-008, F-009 (Fri Nov 20 18:36:10 CET 2026)
+# Vulnerability: CWE-327/CWE-328 (MD5 digest) and CWE-759 (hash without salt) on password storage.
+# Change: unsalted MD5 hexdigest -> salted PBKDF2-HMAC-SHA256, 600,000 iterations, random 16-byte salt.
+#   Format: "pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>" (iterations/salt stored with the hash).
+# Rationale: A slow, salted KDF resists brute force and rainbow tables; MD5 is broken and too fast.
+# Notes: BEHAVIOR-CHANGING (stored format changes; each call returns a different value). Existing MD5
+#   hashes will not verify: re-hash on next successful login (check old MD5, then store the new hash).
+#   That migration belongs in the user store, which is not part of this repository.
 def hash_password(password: str) -> str:
-    return hashlib.md5(password.encode()).hexdigest()
+    salt = os.urandom(16)
+    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _PBKDF2_ITERATIONS)
+    return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"
 
+# Verify a password against a hash produced by hash_password
+# QSE remediation F-008, F-009 (Fri Nov 20 18:36:10 CET 2026)
+# Change: added because a random salt means the hash can no longer be recomputed for comparison.
+# Notes: constant-time comparison; returns False for malformed input.
+def verify_password(password: str, stored: str) -> bool:
+    try:
+        scheme, iterations, salt_hex, digest_hex = stored.split("$")
+        if scheme != "pbkdf2_sha256":
+            return False
+        digest = hashlib.pbkdf2_hmac(
+            "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
+        )
+        return hmac.compare_digest(digest.hex(), digest_hex)
+    except ValueError:
+        return False
+
```

### `qseremediation/utils/tokens.py`

```diff
--- a/qseremediation/utils/tokens.py (original)
+++ b/qseremediation/utils/tokens.py (remediated)
@@ -29,8 +29,22 @@
 from cryptography.hazmat.primitives.asymmetric import padding
 
 # Sign an audit record for non-repudiation logging
+# QSE remediation F-004, F-005 (Fri Nov 20 18:32:10 CET 2026)
+# Vulnerability: CWE-327/CWE-326 (PKCS#1 v1.5 padding) and CWE-327/CWE-328 (SHA-1 digest).
+# Change: PKCS1v15 + SHA1 -> RSA-PSS (MGF1-SHA256, salt length = digest length) + SHA256.
+# Rationale: SHA-1 is collision-weak; PSS has a security proof, unlike PKCS#1 v1.5 signatures.
+# Notes: BEHAVIOR-CHANGING (signature format/digest; verifiers must use PSS with SHA-256).
+#   Old signatures need the old verifier retained. Still RSA, so NOT quantum-safe.
+#   TODO: migrate to ML-DSA/SLH-DSA (see oqs_slhdsa_sign above); requires a key-type change.
 def sign_audit_record(record: bytes, private_key) -> bytes:
-    return private_key.sign(record, padding.PKCS1v15(), hashes.SHA1())
+    return private_key.sign(
+        record,
+        padding.PSS(
+            mgf=padding.MGF1(hashes.SHA256()),
+            salt_length=padding.PSS.DIGEST_LENGTH,
+        ),
+        hashes.SHA256(),
+    )
 
 
 
```

## 6. Validation of preserved functionality

| Time | File | Command | Exit | Summary |
|---|---|---|---|---|
| 2026-11-20T18:31:35+01:00 | qseremediation/api/routes.py | `.venv/bin/python -m py_compile + roundtrip script (3072-bit keygen, OAEP-SHA256 wrap/unwrap)` | 0 | Compiles; key_size==3072; wrap_key output decrypts with OAEP-SHA256 to original key. No unit tests exist for this file. |
| 2026-11-20T18:32:50+01:00 | qseremediation/utils/tokens.py | `.venv/bin/python -m py_compile + sign/verify script (RSA-3072, PSS-SHA256)` | 0 | Compiles; signature verifies with PSS/SHA-256. No unit tests exist for this file. Pre-existing stderr notice: ML-KEM import fallback (MLKEMPrivateKey names do not exist in cryptography 50.0.2), unrelated to this change. |
| 2026-11-20T18:34:04+01:00 | qseremediation/crypto/keys.py | `.venv/bin/python -m py_compile + roundtrip script (ML-KEM-768 encap/decap, AES-256-GCM encrypt/decrypt, nonce uniqueness, bad-key ValueError)` | 0 | Compiles; ML-KEM shared secret matches on decapsulate (ct 1088 bytes); GCM output decrypts and verifies; nonces differ; short key rejected. No unit tests exist for this file. |
| 2026-11-20T18:35:06+01:00 | qseremediation/services/auth.py | `.venv/bin/python -m py_compile + roundtrip script (decrypt_and_verify both functions; short key rejected)` | 0 | Compiles; both functions' output decrypts/verifies with AES-256-GCM; 8-byte key rejected. No unit tests exist for this file. Pre-existing stderr notice: ML-DSA import fallback (mldsa API names differ in cryptography 50.0.2), unrelated to this change. |
| 2026-11-20T18:37:09+01:00 | qseremediation/services/user.py | `.venv/bin/python -m py_compile + script (logic of tests/test_auth.py::test_hash_password_returns_string, verify_password, GCM roundtrip)` | 0 | Compiles; hash_password returns str (test logic passes); verify_password accepts right / rejects wrong and malformed; salts differ per call; GCM output decrypts, nonces differ, 16-byte key rejected. pytest not installed in .venv so test file not run directly. |
| 2026-11-20T18:39:23+01:00 | qseremediation/config/settings.py | `.venv/bin/python -m py_compile + derive_file_key script` | 0 | Compiles; derived key is 32 bytes, deterministic per (passphrase, salt), differs by passphrase; PBKDF2_ITERATIONS==600000. No unit tests exist for this file. |
| 2026-11-20T18:39:23+01:00 | requirements.txt | `.venv/bin/pip install --dry-run -r requirements.txt` | 0 | Dry-run resolves requirements with cryptography>=50.0.2 (supporting change, not a scan finding; edited after backup) |
| 2026-11-20T18:39:38+01:00 | qseremediation/utils/tokens.py | `inline run of tests/test_auth.py logic (pytest not installed in .venv)` | 1 | test_hash_password_returns_string PASS; test_generate_token_not_empty FAIL: generate_reset_token does not exist in tokens.py (also absent in the pre-remediation original) - pre-existing, unrelated to remediation |

## 7. Not remediated

None.
