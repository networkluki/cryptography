#!/usr/bin/env python3
"""Backward-compatible local entry point: `python3 src/crypto.py ...`."""

from networkluki_cipher import (  # noqa: F401
    CIPHER,
    MAX_STDIN_BYTES,
    PLAIN,
    build_maps,
    decrypt_text,
    encrypt_text,
    read_bounded_stdin,
    validate_key,
)
from networkluki_cipher.cli import cmd_show, cmd_show_map, main

if __name__ == "__main__":
    raise SystemExit(main())
