"""
Cipher utilities for Quantum-DDay.
Provides encryption and decryption helpers used by services.
"""
import os



# Algorithm: ML-DSA  Library: cryptography  Language: Python
# Post-quantum digital signature using the cryptography library
try:
    from cryptography.hazmat.primitives.asymmetric.mldsa import (
        MLDSAPrivateKey, MLDSAPublicKey, generate_private_key as mldsa_generate_private_key
    )

    def mldsa_sign(message: bytes) -> bytes:
        # Algorithm: ML-DSA  Library: cryptography  Language: Python
        private_key = mldsa_generate_private_key("MLDSA65")
        return private_key.sign(message)
except ImportError:
    import sys
    print("ML-DSA requires cryptography >= 44.0.0 with ML-DSA support", file=sys.stderr)

    def mldsa_sign(message: bytes) -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("ML-DSA not available — install cryptography >= 44.0.0")



# Algorithm: XMSS  Library: oqs  Language: Python
# Stateful hash-based post-quantum signature using liboqs-python
try:
    import oqs

    def oqs_xmss_sign(message: bytes) -> bytes:
        # Algorithm: XMSS  Library: oqs  Language: Python
        with oqs.Signature("XMSS-SHAKE_10_256") as sig:
            public_key = sig.generate_keypair()
            return sig.sign(message)
except ImportError:
    import sys
    print("XMSS (oqs) requires liboqs-python: pip install liboqs-python", file=sys.stderr)

    def oqs_xmss_sign(message: bytes) -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("liboqs-python not installed")



# Algorithm: ML-KEM  Library: oqs  Language: Python
# Post-quantum key encapsulation using liboqs-python (Open Quantum Safe)
try:
    import oqs

    def oqs_mlkem_keygen_and_encap() -> bytes:
        # Algorithm: ML-KEM  Library: oqs  Language: Python
        with oqs.KeyEncapsulation("Kyber768") as kem:
            public_key = kem.generate_keypair()
            ciphertext, shared_key_enc = kem.encap_secret(public_key)
            shared_key_dec = kem.decap_secret(ciphertext)
            return shared_key_dec
except ImportError:
    import sys
    print("ML-KEM (oqs) requires liboqs-python: pip install liboqs-python", file=sys.stderr)

    def oqs_mlkem_keygen_and_encap() -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("liboqs-python not installed")

