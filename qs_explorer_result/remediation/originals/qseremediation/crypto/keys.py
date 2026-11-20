"""
Key management utilities for QSERemediation.
Handles generation, derivation, and storage of cryptographic keys.
"""
import os
import base64



from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDH, SECP256R1, generate_private_key
)

# Derive a shared session secret using ECDH
def ecdh_shared_secret(peer_public_key) -> bytes:
    ephemeral = generate_private_key(SECP256R1())
    return ephemeral.exchange(ECDH(), peer_public_key)



from Crypto.Cipher import AES
import os, base64

# Encrypt user session data for cookie storage
def encrypt_session(data: bytes, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = data + b"\x00" * (16 - len(data) % 16)
    return iv + cipher.encrypt(padded)

