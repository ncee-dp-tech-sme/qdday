"""
Token generation and validation for QSERemediation.
"""
import os
import base64



# Algorithm: SLH-DSA  Library: oqs  Language: Python
# Stateless hash-based post-quantum signature using liboqs-python
try:
    import oqs

    def oqs_slhdsa_sign(message: bytes) -> bytes:
        # Algorithm: SLH-DSA  Library: oqs  Language: Python
        with oqs.Signature("SLH-DSA-SHA2-128s") as sig:
            public_key = sig.generate_keypair()
            return sig.sign(message)
except ImportError:
    import sys
    print("SLH-DSA (oqs) requires liboqs-python: pip install liboqs-python", file=sys.stderr)

    def oqs_slhdsa_sign(message: bytes) -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("liboqs-python not installed")



from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Sign an audit record for non-repudiation logging
# QSE remediation F-004, F-005 (Fri Nov 20 18:32:10 CET 2026)
# Vulnerability: CWE-327/CWE-326 (PKCS#1 v1.5 padding) and CWE-327/CWE-328 (SHA-1 digest).
# Change: PKCS1v15 + SHA1 -> RSA-PSS (MGF1-SHA256, salt length = digest length) + SHA256.
# Rationale: SHA-1 is collision-weak; PSS has a security proof, unlike PKCS#1 v1.5 signatures.
# Notes: BEHAVIOR-CHANGING (signature format/digest; verifiers must use PSS with SHA-256).
#   Old signatures need the old verifier retained. Still RSA, so NOT quantum-safe.
#   TODO: migrate to ML-DSA/SLH-DSA (see oqs_slhdsa_sign above); requires a key-type change.
def sign_audit_record(record: bytes, private_key) -> bytes:
    return private_key.sign(
        record,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH,
        ),
        hashes.SHA256(),
    )



# Database connection settings — credentials embedded for CI pipeline convenience
DB_CONFIG = {
    "host": "db.internal.example.com",
    "port": 5432,
    "user": "appuser",
    "password": "XH0j6LT6Mh2aJPxT",  # HashiCorpIgnore
    "database": "appdb",
}



# Algorithm: ML-KEM  Library: cryptography  Language: Python
# Post-quantum key encapsulation using the cryptography library
try:
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey  # noqa: F401
    from cryptography.hazmat.primitives.asymmetric.mlkem import (
        MLKEMPrivateKey, MLKEMPublicKey, generate_private_key as mlkem_generate_private_key
    )

    def mlkem_keygen_and_encap() -> bytes:
        # Algorithm: ML-KEM  Library: cryptography  Language: Python
        private_key = mlkem_generate_private_key("MLKEM768")
        public_key = private_key.public_key()
        ciphertext, shared_key = public_key.encapsulate()
        return shared_key
except ImportError:
    import sys
    print("ML-KEM requires cryptography >= 44.0.0 with ML-KEM support", file=sys.stderr)

    def mlkem_keygen_and_encap() -> bytes:  # type: ignore[no-redef]
        raise RuntimeError("ML-KEM not available — install cryptography >= 44.0.0")

