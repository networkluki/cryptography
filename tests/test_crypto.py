import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import crypto


def test_ascii_roundtrip_preserves_text():
    enc, dec = crypto.build_maps()
    plain = "Hello, World!"
    cipher = crypto.encrypt_text(plain, enc)
    restored = crypto.decrypt_text(cipher, dec)
    assert restored == plain


def test_unicode_unmapped_letter_roundtrip():
    enc, dec = crypto.build_maps()
    plain = "straße"
    cipher = crypto.encrypt_text(plain, enc)
    restored = crypto.decrypt_text(cipher, dec)
    assert "ß" in cipher
    assert restored == plain
