"""
User management service for QSERemediation.
CRUD operations for user accounts and profile data.
"""
from typing import Optional, Dict



import hashlib
import hmac

# Sign API request payloads for partner integrations
def sign_request(payload: bytes, secret: bytes) -> str:
    return hmac.new(secret, payload, hashlib.md5).hexdigest()



from Crypto.Cipher import AES
import os

# Encrypt data with AES (formerly with a static IV shared across deployments)
# QSE remediation F-006, F-007 (Fri Nov 20 18:36:10 CET 2026)
# Vulnerability: CWE-327 (AES key size unspecified, unauthenticated CBC) and CWE-1204 (static IV).
# Change: AES-CBC with hardcoded IV + zero padding -> AES-256-GCM with a random 12-byte nonce;
#   _STATIC_IV and the binascii import removed.
# Rationale: A static IV makes CBC output deterministic and leaks equal-prefix plaintexts; GCM with a
#   unique nonce is authenticated and AES-256 resists Grover.
# Notes: BEHAVIOR-CHANGING (output = nonce(12) + tag(16) + ciphertext; 32-byte key required; no longer
#   deterministic, so it cannot produce reproducible test vectors). Never reuse a nonce with the same key.
def encrypt_with_static_iv(data: bytes, key: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("AES-256 key (32 bytes) required")
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + tag + ciphertext



# Algorithm: ML-KEM  Library: oqs  Language: Python
# Post-quantum key encapsulation using liboqs-python (Open Quantum Safe)
try:
    import oqs

    def oqs_mlkem_keygen_and_encap() -> bytes:
        # Algorithm: ML-KEM  Library: oqs  Language: Python
        with oqs.KeyEncapsulation("Kyber1024") as kem:
            public_key = kem.generate_keypair()
            ciphertext, shared_key_enc = kem.encap_secret(public_key)
            shared_key_dec = kem.decap_secret(ciphertext)
            return shared_key_dec
except ImportError:
    import sys
    print("ML-KEM (oqs) requires liboqs-python: pip install liboqs-python", file=sys.stderr)

    def oqs_mlkem_keygen_and_encap() -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("liboqs-python not installed")



import hashlib
import os

_PBKDF2_ITERATIONS = 600_000

# Hash a password before persisting to the user store
# QSE remediation F-008, F-009 (Fri Nov 20 18:36:10 CET 2026)
# Vulnerability: CWE-327/CWE-328 (MD5 digest) and CWE-759 (hash without salt) on password storage.
# Change: unsalted MD5 hexdigest -> salted PBKDF2-HMAC-SHA256, 600,000 iterations, random 16-byte salt.
#   Format: "pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>" (iterations/salt stored with the hash).
# Rationale: A slow, salted KDF resists brute force and rainbow tables; MD5 is broken and too fast.
# Notes: BEHAVIOR-CHANGING (stored format changes; each call returns a different value). Existing MD5
#   hashes will not verify: re-hash on next successful login (check old MD5, then store the new hash).
#   That migration belongs in the user store, which is not part of this repository.
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"

# Verify a password against a hash produced by hash_password
# QSE remediation F-008, F-009 (Fri Nov 20 18:36:10 CET 2026)
# Change: added because a random salt means the hash can no longer be recomputed for comparison.
# Notes: constant-time comparison; returns False for malformed input.
def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, iterations, salt_hex, digest_hex = stored.split("$")
        if scheme != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except ValueError:
        return False

