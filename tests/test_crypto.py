"""Unit and regression tests for the public API and command-line interface."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from networkluki_cipher import (
    CIPHER,
    build_maps,
    decrypt_text,
    encrypt_text,
    read_bounded_stdin,
    validate_key,
)
from networkluki_cipher.cli import main


class CipherTests(unittest.TestCase):
    def test_default_key_is_a_valid_permutation(self):
        validate_key(CIPHER)

    def test_validate_key_rejects_duplicate_letters(self):
        with self.assertRaisesRegex(ValueError, "exactly once"):
            validate_key("A" * 26)

    def test_validate_key_rejects_non_ascii_letters(self):
        with self.assertRaisesRegex(ValueError, "only letters A-Z"):
            validate_key("ABCDEFGHIJKLMNOPQRSTUVWXYÅ")

    def test_validate_key_rejects_wrong_type(self):
        with self.assertRaises(ValueError):
            validate_key(None)

    def test_build_maps_accepts_custom_permutation(self):
        enc, dec = build_maps("ZYXWVUTSRQPONMLKJIHGFEDCBA")
        self.assertEqual(encrypt_text("Abc", enc), "Zyx")
        self.assertEqual(decrypt_text("Zyx", dec), "Abc")

    def test_roundtrip_preserves_case_unicode_and_symbols(self):
        enc, dec = build_maps()
        original = "Hello, World! 123 åäö🛡️"
        self.assertEqual(decrypt_text(encrypt_text(original, enc), dec), original)

    def test_non_letters_unchanged(self):
        enc, dec = build_maps()
        original = "123-_=+åßé"
        self.assertEqual(encrypt_text(original, enc), original)
        self.assertEqual(decrypt_text(original, dec), original)

    def test_read_bounded_stdin_rejects_oversized_text(self):
        with self.assertRaisesRegex(ValueError, "maximum size"):
            read_bounded_stdin(io.StringIO("abcd"), limit=3)

    def test_read_bounded_stdin_counts_utf8_bytes(self):
        with self.assertRaisesRegex(ValueError, "maximum size"):
            read_bounded_stdin(io.StringIO("å"), limit=1)

    def test_main_rejects_oversized_stdin(self):
        with (
            patch("sys.stdin", io.StringIO("abcd")),
            patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            self.assertEqual(main(stdin_limit=3, argv=["enc"]), 2)
            self.assertIn("maximum size of 3 bytes", stderr.getvalue())

    def test_main_rejects_oversized_argument(self):
        with patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(main(stdin_limit=3, argv=["enc", "abcd"]), 2)
            self.assertIn("maximum size of 3 bytes", stderr.getvalue())

    def test_cli_show_produces_exactly_two_lines(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(argv=["show"]), 0)
        self.assertEqual(stdout.getvalue().splitlines(), ["abcdefghijklmnopqrstuvwxyz", CIPHER])

    def test_cli_show_map_produces_26_lines(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(argv=["show-map"]), 0)
        self.assertEqual(len(stdout.getvalue().splitlines()), 26)

    def test_cli_implicit_decrypt(self):
        enc, _ = build_maps()
        encrypted = encrypt_text("Hello", enc)
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(argv=[encrypted]), 0)
        self.assertEqual(stdout.getvalue(), "Hello\n")


if __name__ == "__main__":
    unittest.main()
