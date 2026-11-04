"""Educational substitution cipher API (not suitable for protecting secrets)."""

from .cipher import (
    CIPHER,
    MAX_STDIN_BYTES,
    PLAIN,
    build_maps,
    check_input_size,
    decrypt_text,
    encrypt_text,
    read_bounded_stdin,
    validate_key,
)

__all__ = [
    "CIPHER",
    "MAX_STDIN_BYTES",
    "PLAIN",
    "build_maps",
    "check_input_size",
    "decrypt_text",
    "encrypt_text",
    "read_bounded_stdin",
    "validate_key",
]
