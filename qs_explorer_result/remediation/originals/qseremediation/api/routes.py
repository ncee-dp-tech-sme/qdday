"""
API route definitions for QSERemediation.
Maps HTTP endpoints to service handlers.
"""
from typing import Any, Dict



from cryptography.hazmat.primitives.asymmetric import rsa

# Generate RSA key pair for device certificate signing
def generate_device_keypair():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
    )



from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

# Wrap a symmetric key using the recipient's RSA public key
def wrap_key(symmetric_key: bytes, recipient_public_key) -> bytes:
    return recipient_public_key.encrypt(
        symmetric_key,
        asym_padding.PKCS1v15(),
    )



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



import hmac, hashlib, base64, json

# JWT signing secret — shared across all application instances
_JWT_SECRET = "y7xoltFyO46CBLNdBOLoinMey2g8kgJP"  # HashiCorpIgnore

def sign_jwt(payload: dict) -> str:
    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').rstrip(b"=").decode()
    body = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    sig_input = f"{header}.{body}".encode()
    sig = hmac.new(_JWT_SECRET.encode(), sig_input, hashlib.sha1).digest()
    return f"{header}.{body}.{base64.urlsafe_b64encode(sig).rstrip(b'=').decode()}"

