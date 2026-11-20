"""
Authentication service for QSERemediation.
Manages user login, token issuance, and session validation.
"""
import time
import datetime



# Algorithm: ML-DSA  Library: cryptography  Language: Python
# Post-quantum digital signature using the cryptography library
try:
    from cryptography.hazmat.primitives.asymmetric.mldsa import (
        MLDSAPrivateKey, MLDSAPublicKey, generate_private_key as mldsa_generate_private_key
    )

    def mldsa_sign(message: bytes) -> bytes:
        # Algorithm: ML-DSA  Library: cryptography  Language: Python
        private_key = mldsa_generate_private_key("MLDSA87")
        return private_key.sign(message)
except ImportError:
    import sys
    print("ML-DSA requires cryptography >= 44.0.0 with ML-DSA support", file=sys.stderr)

    def mldsa_sign(message: bytes) -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("ML-DSA not available — install cryptography >= 44.0.0")



# Symmetric key for encrypting internal metrics payloads
METRICS_ENCRYPTION_KEY = b"3606d827bdb1089f82b2aa84423b5795"



from Crypto.Cipher import AES
import base64
import os

# AES-256-GCM helper: returns nonce(12) + tag(16) + ciphertext
# QSE remediation F-010, F-011, F-012, F-013 (Fri Nov 20 18:34:44 CET 2026)
# Vulnerability: CWE-327 - AES-ECB/unspecified key size and Blowfish-ECB (weak/unauthenticated modes).
# Change: shared helper using AES-256-GCM with a random 12-byte nonce; 32-byte key required.
# Rationale: AES-256 resists Grover; GCM is authenticated and hides plaintext patterns (unlike ECB).
# Notes: BEHAVIOR-CHANGING for encrypt_config and encrypt_legacy (format, key length). Never reuse a nonce
#   with the same key; existing ECB data needs a decrypt-old/re-encrypt path.
def _aes256_gcm_encrypt(data: bytes, key: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("AES-256 key (32 bytes) required")
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + tag + ciphertext

# Encrypt configuration blob for at-rest storage
# QSE remediation F-010, F-011 (Fri Nov 20 18:34:44 CET 2026)
# Change: AES-ECB + zero padding -> AES-256-GCM via _aes256_gcm_encrypt (base64 of nonce+tag+ciphertext).
# Notes: BEHAVIOR-CHANGING (see helper above).
def encrypt_config(data: bytes, key: bytes) -> str:
    return base64.b64encode(_aes256_gcm_encrypt(data, key)).decode()



import struct

# Encrypt small data chunks, formerly Blowfish, for legacy API compatibility
# QSE remediation F-012, F-013 (Fri Nov 20 18:34:44 CET 2026)
# Change: Blowfish-ECB with key[:8] -> AES-256-GCM via _aes256_gcm_encrypt.
# Notes: BEHAVIOR-CHANGING: peers expecting Blowfish-ECB output can no longer read the data;
#   a 32-byte key is now required (was 8 bytes).
def encrypt_legacy(data: bytes, key: bytes) -> bytes:
    return _aes256_gcm_encrypt(data, key)

