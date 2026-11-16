"""
Hashing utilities for Quantum-DDay.
"""
import hashlib



import ssl

# Build SSL context for connections to legacy on-premise endpoints
def build_legacy_ssl_context() -> ssl.SSLContext:
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.options &= ~ssl.OP_NO_SSLv3
    ctx.minimum_version = ssl.TLSVersion.TLSv1
    return ctx

