#!/usr/bin/env python3
"""Monoalphabetic substitution cipher CLI (educational/demo).

Deterministic, case-preserving, and intended for learning purposes only.
"""

from __future__ import annotations

import argparse
import string
import sys

PLAIN = string.ascii_lowercase
CIPHER = "PAQCRIXOVEHYJUZGSTKLNFMDBW"


def validate_key(cipher: str) -> None:
    """Validate that the key is exactly 26 unique letters A-Z."""
    if len(cipher) != 26:
        raise ValueError("CIPHER must be exactly 26 characters long.")
    if not cipher.isalpha():
        raise ValueError("CIPHER must contain only letters A-Z.")

    cipher_u = cipher.upper()
    if set(cipher_u) != set(string.ascii_uppercase):
        missing = sorted(set(string.ascii_uppercase) - set(cipher_u))
        extra = sorted(set(cipher_u) - set(string.ascii_uppercase))
        raise ValueError(f"Invalid key permutation. Missing={missing}, Extra={extra}")


def build_maps() -> tuple[dict[str, str], dict[str, str]]:
    """Build encrypt/decrypt maps."""
    cipher_u = CIPHER.upper()
    enc = {p: c for p, c in zip(PLAIN, cipher_u)}
    dec = {c.lower(): p for p, c in zip(PLAIN, cipher_u)}
    return enc, dec


def encrypt_text(text: str, enc: dict[str, str]) -> str:
    """Encrypt text; preserve case; keep non-letters unchanged."""
    out: list[str] = []
    for ch in text:
        if ch.isalpha():
            mapped_u = enc.get(ch.lower(), ch)
            out.append(mapped_u if ch.isupper() else mapped_u.lower())
        else:
            out.append(ch)
    return "".join(out)


def decrypt_text(text: str, dec: dict[str, str]) -> str:
    """Decrypt text; preserve case; keep non-letters unchanged."""
    out: list[str] = []
    for ch in text:
        if ch.isalpha():
            mapped_l = dec.get(ch.lower(), ch.lower())
            out.append(mapped_l.upper() if ch.isupper() else mapped_l)
        else:
            out.append(ch)
    return "".join(out)


def cmd_show() -> int:
    print(PLAIN)
    print(CIPHER)
    return 0


def cmd_show_map() -> int:
    for p, c in zip(string.ascii_uppercase, CIPHER.upper()):
        print(f"{p} -> {c}")
    return 0


def main() -> int:
    try:
        validate_key(CIPHER)
    except ValueError as err:
        print(f"Key error: {err}", file=sys.stderr)
        return 2

    enc, dec = build_maps()

    parser = argparse.ArgumentParser(
        prog="crypto",
        description="Monoalphabetic substitution cipher CLI (A->P style).",
    )
    parser.add_argument(
        "cmd",
        nargs="?",
        help="Command: show | show-map | enc | dec. If omitted, single input defaults to decrypt.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to process. If omitted for enc/dec, reads from stdin.",
    )
    args = parser.parse_args()

    if args.cmd == "show":
        return cmd_show()
    if args.cmd == "show-map":
        return cmd_show_map()
    if args.cmd == "enc":
        data = args.text if args.text is not None else sys.stdin.read()
        print(encrypt_text(data, enc))
        return 0
    if args.cmd == "dec":
        data = args.text if args.text is not None else sys.stdin.read()
        print(decrypt_text(data, dec))
        return 0

    if args.cmd is not None and args.text is None:
        print(decrypt_text(args.cmd, dec))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
