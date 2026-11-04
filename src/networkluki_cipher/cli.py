"""Command-line interface for the educational substitution cipher."""

from __future__ import annotations

import argparse
import string
import sys
from collections.abc import Sequence

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


def cmd_show() -> int:
    print(PLAIN)
    print(CIPHER)
    return 0


def cmd_show_map() -> int:
    for plain, encrypted in zip(string.ascii_uppercase, CIPHER):
        print(f"{plain} -> {encrypted}")
    return 0


def main(stdin_limit: int = MAX_STDIN_BYTES, argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit status."""
    try:
        validate_key(CIPHER)
    except ValueError as exc:
        print(f"Key error: {exc}", file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(
        prog="networkluki-cipher",
        description="Educational monoalphabetic substitution cipher (NOT secure encryption).",
    )
    parser.add_argument(
        "cmd",
        nargs="?",
        help="show | show-map | enc | dec; other single values are decrypted",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Input text; for enc/dec, omit to read stdin",
    )
    args = parser.parse_args(argv)

    if args.cmd == "show":
        if args.text is not None:
            parser.error("show does not accept a text argument")
        return cmd_show()
    if args.cmd == "show-map":
        if args.text is not None:
            parser.error("show-map does not accept a text argument")
        return cmd_show_map()

    enc, dec = build_maps()
    if args.cmd in ("enc", "dec"):
        try:
            data = (
                check_input_size(args.text, stdin_limit)
                if args.text is not None
                else read_bounded_stdin(sys.stdin, stdin_limit)
            )
        except (ValueError, UnicodeError, OSError) as exc:
            print(f"Input error: {exc}", file=sys.stderr)
            return 2
        output = encrypt_text(data, enc) if args.cmd == "enc" else decrypt_text(data, dec)
        print(output)
        return 0

    if args.cmd is not None and args.text is None:
        try:
            data = check_input_size(args.cmd, stdin_limit)
        except ValueError as exc:
            print(f"Input error: {exc}", file=sys.stderr)
            return 2
        print(decrypt_text(data, dec))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
