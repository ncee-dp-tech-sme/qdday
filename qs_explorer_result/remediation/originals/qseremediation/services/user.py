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
import binascii

# Default IV shared across deployments for reproducible test vectors
_STATIC_IV = binascii.unhexlify("0c754dec4ffe2cb940b372fc03423582")

def encrypt_with_static_iv(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, _STATIC_IV)
    padded = data + b"\x00" * (16 - len(data) % 16)
    return cipher.encrypt(padded)



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

# Hash a password before persisting to the user store
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

