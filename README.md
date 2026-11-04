# NetworkLuki Cipher

[![CI](https://github.com/networkluki/cryptography/actions/workflows/ci.yml/badge.svg)](https://github.com/networkluki/cryptography/actions/workflows/ci.yml)

An educational monoalphabetic substitution cipher, available as a Python library and command-line application. This project also contains cryptography and network research notes.

> **Security warning:** This is a classical substitution cipher with a fixed default alphabet. It is trivial to break with frequency analysis and **must not** be used for passwords, private messages, authentication, file encryption, or any sensitive information. For real encryption, use a vetted cryptographic library and standard authenticated encryption.

## Installation

After the first PyPI release:

```bash
python -m pip install networkluki-cipher
```

From a checked-out repository, for development:

```bash
python -m pip install -e .
```

Requires Python 3.10 or newer. The runtime has no third-party dependencies.

## CLI

```bash
networkluki-cipher show
networkluki-cipher show-map
networkluki-cipher enc "Hello, World!"
networkluki-cipher dec "Oryyz, Mztyc!"
printf '%s\n' 'Hello' | networkluki-cipher enc
python -m networkluki_cipher show
```

`show` prints the plaintext alphabet and substitution alphabet on two lines. `show-map` prints all 26 mappings. `enc` and `dec` accept a single text argument or read standard input. A single unrecognized positional argument is treated as text to decrypt, for compatibility with the original script.

The CLI enforces a 1 MiB UTF-8 input limit; input exceeding it fails with exit code 2. Non-ASCII characters and nonletters are preserved.

The old local command remains available from the repository root:

```bash
python3 src/crypto.py show
```

## Python library

```python
from networkluki_cipher import build_maps, encrypt_text, decrypt_text

enc, dec = build_maps()
ciphertext = encrypt_text("Hello, World!", enc)
assert decrypt_text(ciphertext, dec) == "Hello, World!"
```

`build_maps(cipher=...)` can accept a custom permutation of the 26 ASCII letters for demonstrations. Changing the substitution alphabet **does not** make the cipher secure.

## Development and testing

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
```

Release steps and PyPI Trusted Publishing setup: [docs/PUBLISHING.md](docs/PUBLISHING.md).

## Research repository

Other material in this repository covers cryptography-focused research, network-layer concepts, visualizations, and reproducible experiments. Research and production-grade cryptography are separate from the educational cipher package.

For each study, document the problem statement, related work, method, results, limitations, and conclusions. Explicitly record cryptographic assumptions and threat models. Cite relevant RFC, NIST, ISO, or peer-reviewed references. Include the commit hash when citing this repository as a research artifact.

## License

MIT. See [LICENSE](LICENSE).
