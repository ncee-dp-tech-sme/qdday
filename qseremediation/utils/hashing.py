"""
Hashing utilities for QSERemediation.
"""
import hashlib



# Algorithm: XMSS  Library: oqs  Language: Python
# Stateful hash-based post-quantum signature using liboqs-python
try:
    import oqs

    def oqs_xmss_sign(message: bytes) -> bytes:
        # Algorithm: XMSS  Library: oqs  Language: Python
        with oqs.Signature("XMSS-SHA2_10_256") as sig:
            public_key = sig.generate_keypair()
            return sig.sign(message)
except ImportError:
    import sys
    print("XMSS (oqs) requires liboqs-python: pip install liboqs-python", file=sys.stderr)

    def oqs_xmss_sign(message: bytes) -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("liboqs-python not installed")

