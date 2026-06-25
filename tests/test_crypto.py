import io
import unittest
from unittest.mock import patch

from src.crypto import (
    build_maps,
    decrypt_text,
    encrypt_text,
    main,
    read_bounded_stdin,
    validate_key,
)


class CryptoTests(unittest.TestCase):
    def test_validate_key_accepts_permutation(self):
        validate_key("PAQCRIXOVEHYJUZGSTKLNFMDBW")

    def test_encrypt_decrypt_roundtrip_preserves_text(self):
        enc, dec = build_maps()
        original = "Hello, World! 123"
        encrypted = encrypt_text(original, enc)
        decrypted = decrypt_text(encrypted, dec)
        self.assertEqual(decrypted, original)

    def test_non_letters_unchanged(self):
        enc, _ = build_maps()
        self.assertEqual(encrypt_text("123-_=+", enc), "123-_=+")

    def test_non_ascii_letters_unchanged(self):
        enc, dec = build_maps()
        original = "åßé"
        self.assertEqual(encrypt_text(original, enc), original)
        self.assertEqual(decrypt_text(original, dec), original)

    def test_validate_key_rejects_non_ascii_letters(self):
        with self.assertRaisesRegex(ValueError, "only letters A-Z"):
            validate_key("ABCDEFGHIJKLMNOPQRSTUVWXYÅ")

    def test_read_bounded_stdin_rejects_oversized_input(self):
        with self.assertRaisesRegex(ValueError, "Input exceeds maximum size"):
            read_bounded_stdin(io.StringIO("abcd"), limit=3)

    def test_main_rejects_oversized_stdin(self):
        with (
            patch("sys.argv", ["crypto", "enc"]),
            patch("sys.stdin", io.StringIO("abcd")),
            patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            self.assertEqual(main(stdin_limit=3), 2)
            self.assertIn(
                "Input error: Input exceeds maximum size of 3 bytes.", stderr.getvalue()
            )


if __name__ == "__main__":
    unittest.main()
