"""
Key management utilities for QSERemediation.
Handles generation, derivation, and storage of cryptographic keys.
"""
import os
import base64



from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PublicKey

# Derive a shared session secret using ML-KEM-768 encapsulation
# QSE remediation F-014, F-015 (Fri Nov 20 18:33:36 CET 2026)
# Vulnerability: CWE-327 - EC key generation and ECDH key agreement (quantum-vulnerable).
# Change: ECDH (P-256) -> ML-KEM-768 (FIPS 203) encapsulation; returns (shared_secret, ciphertext).
# Rationale: ML-KEM is a NIST-standardized quantum-resistant KEM; ECDH is broken by Shor's algorithm.
# Notes: BEHAVIOR-CHANGING. Name kept for greppability, but this is no longer ECDH: the return type
#   is now a tuple, the peer needs an ML-KEM-768 key pair and must receive the 1088-byte ciphertext
#   and call decapsulate(). No hybrid with a classical KEM yet (needs protocol design).
def ecdh_shared_secret(peer_public_key: MLKEM768PublicKey) -> tuple[bytes, bytes]:
    shared_secret, ciphertext = peer_public_key.encapsulate()
    return shared_secret, ciphertext



from Crypto.Cipher import AES
import os, base64

# Encrypt user session data for cookie storage
# QSE remediation F-016, F-017 (Fri Nov 20 18:33:36 CET 2026)
# Vulnerability: CWE-327 (AES key size unspecified, unauthenticated CBC) and CWE-1204 (IV handling).
# Change: AES-CBC + zero padding -> AES-256-GCM with a random 12-byte nonce; key must be 32 bytes.
# Rationale: AES-256 resists Grover; GCM adds authentication and removes the ambiguous zero padding.
# Notes: BEHAVIOR-CHANGING (output = nonce(12) + tag(16) + ciphertext; 32-byte key required).
#   The CBC IV was already random per call, so CWE-1204 looked like a false positive; it is moot now.
#   Never reuse a nonce with the same key; existing CBC data needs a decrypt-old/re-encrypt path.
def encrypt_session(data: bytes, key: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("AES-256 key (32 bytes) required")
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + tag + ciphertext

