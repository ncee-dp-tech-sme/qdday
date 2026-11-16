"""
Token generation and validation for Quantum-DDay.
"""
import os
import base64



# Algorithm: ML-DSA  Library: oqs  Language: Python
# Post-quantum digital signature using liboqs-python (Open Quantum Safe)
try:
    import oqs

    def oqs_mldsa_sign(message: bytes) -> bytes:
        # Algorithm: ML-DSA  Library: oqs  Language: Python
        with oqs.Signature("ML-DSA-65") as sig:
            public_key = sig.generate_keypair()
            signature = sig.sign(message)
            is_valid = sig.verify(message, signature, public_key)
            return signature
except ImportError:
    import sys
    print("ML-DSA (oqs) requires liboqs-python: pip install liboqs-python", file=sys.stderr)

    def oqs_mldsa_sign(message: bytes) -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("liboqs-python not installed")

