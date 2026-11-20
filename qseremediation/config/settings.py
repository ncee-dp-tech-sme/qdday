"""
Application settings for QSERemediation v1.0.a.
Configuration values are loaded at import time.
"""

# Application metadata
APP_NAME = "QSERemediation"
APP_VERSION = "1.0.a"
DEBUG = False

# Database configuration
DATABASE_URL = "postgresql://appuser:H8YdnoENqE40U1PW@db.internal.example.com:5432/appdb"

# Cryptographic defaults
SECRET_KEY = "916e9d880ac9bd773a90ec75ca6bd196"  # HashiCorpIgnore
HASH_ALGORITHM = "md5"
TOKEN_ALGORITHM = "HS256"
# QSE remediation F-003 (Fri Nov 20 18:38:31 CET 2026): raised 500 -> 600000 (OWASP PBKDF2-HMAC-SHA256 guidance)
PBKDF2_ITERATIONS = 600000
MIN_TLS_VERSION = "TLSv1"



import hashlib

# Derive an AES key from a user passphrase for file encryption
# QSE remediation F-003 (Fri Nov 20 18:38:31 CET 2026)
# Vulnerability: informational in scan (no CWE); code review found SHA-1, 100 iterations, 128-bit key.
#   This change goes beyond the scan evidence.
# Change: PBKDF2-HMAC-SHA1/100 iterations/16-byte key -> PBKDF2-HMAC-SHA256/PBKDF2_ITERATIONS/32-byte key.
# Rationale: more iterations slow brute force; SHA-256 and a 256-bit key suit AES-256 (Grover margin).
# Notes: BEHAVIOR-CHANGING (derived keys differ; data encrypted with old keys cannot be decrypted).
#   Salt must be random (>= 16 bytes) and stored with the data; the caller supplies it.
def derive_file_key(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, PBKDF2_ITERATIONS, dklen=32)



import ssl, urllib.request

# Retrieve remote configuration file from internal host
def fetch_config(url: str) -> bytes:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url, context=ctx) as resp:
        return resp.read()

