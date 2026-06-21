import unittest

from src.crypto import build_maps, decrypt_text, encrypt_text, validate_key


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


if __name__ == "__main__":
    unittest.main()
