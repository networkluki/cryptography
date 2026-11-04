"""Educational monoalphabetic substitution cipher.

This is not secure cryptography. Do not use it for secrets or sensitive data.
"""

from __future__ import annotations

import string
from typing import Dict, Mapping, TextIO, Tuple

PLAIN = string.ascii_lowercase
CIPHER = "PAQCRIXOVEHYJUZGSTKLNFMDBW"
MAX_STDIN_BYTES = 1_048_576


def validate_key(cipher: str) -> None:
    """Require a permutation of the 26 ASCII letters (case-insensitive)."""
    if not isinstance(cipher, str):
        raise ValueError("Cipher key must be a string.")
    if len(cipher) != 26:
        raise ValueError("CIPHER must be exactly 26 characters long.")
    if not cipher.isascii() or not cipher.isalpha():
        raise ValueError("CIPHER must contain only letters A-Z.")
    cipher_upper = cipher.upper()
    if set(cipher_upper) != set(string.ascii_uppercase):
        raise ValueError("CIPHER must contain each letter A-Z exactly once.")


def build_maps(cipher: str = CIPHER) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Build plaintext-to-cipher and cipher-to-plaintext substitution maps."""
    validate_key(cipher)
    cipher_upper = cipher.upper()
    enc = dict(zip(PLAIN, cipher_upper))
    dec = {encrypted.lower(): plain for plain, encrypted in enc.items()}
    return enc, dec


def encrypt_text(text: str, enc: Mapping[str, str]) -> str:
    """Substitute ASCII letters, keeping case and non-ASCII text unchanged."""
    out: list[str] = []
    for ch in text:
        if ch in string.ascii_letters:
            mapped = enc[ch.lower()]
            out.append(mapped if ch.isupper() else mapped.lower())
        else:
            out.append(ch)
    return "".join(out)


def decrypt_text(text: str, dec: Mapping[str, str]) -> str:
    """Reverse a substitution, keeping case and non-ASCII text unchanged."""
    out: list[str] = []
    for ch in text:
        if ch in string.ascii_letters:
            mapped = dec[ch.lower()]
            out.append(mapped.upper() if ch.isupper() else mapped)
        else:
            out.append(ch)
    return "".join(out)


def check_input_size(text: str, limit: int = MAX_STDIN_BYTES) -> str:
    """Return text after enforcing a UTF-8 byte limit."""
    if not isinstance(limit, int) or limit < 0:
        raise ValueError("Input limit must be a nonnegative integer.")
    try:
        byte_count = len(text.encode("utf-8"))
    except UnicodeError as exc:
        raise ValueError("Input is not valid UTF-8 text.") from exc
    if byte_count > limit:
        raise ValueError(f"Input exceeds maximum size of {limit} bytes.")
    return text


def read_bounded_stdin(stdin: TextIO, limit: int = MAX_STDIN_BYTES) -> str:
    """Read at most limit + 1 characters, then enforce the UTF-8 byte limit."""
    if not isinstance(limit, int) or limit < 0:
        raise ValueError("Input limit must be a nonnegative integer.")
    return check_input_size(stdin.read(limit + 1), limit)
