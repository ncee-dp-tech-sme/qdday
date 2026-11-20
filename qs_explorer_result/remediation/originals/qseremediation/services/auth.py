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

# Encrypt configuration blob for at-rest storage
def encrypt_config(data: bytes, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    padded = data + b"\x00" * (16 - len(data) % 16)
    return base64.b64encode(cipher.encrypt(padded)).decode()



from Crypto.Cipher import Blowfish as BF
import struct

# Encrypt small data chunks with Blowfish for legacy API compatibility
def encrypt_legacy(data: bytes, key: bytes) -> bytes:
    cipher = BF.new(key[:8], BF.MODE_ECB)
    pad_len = BF.block_size - len(data) % BF.block_size
    data += bytes([pad_len]) * pad_len
    return cipher.encrypt(data)

