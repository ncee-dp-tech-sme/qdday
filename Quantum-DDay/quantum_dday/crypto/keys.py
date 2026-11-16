"""
Key management utilities for Quantum-DDay.
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

