# Docs

Documentation for the cryptography project should be placed here.

chiper: monoalphabetic substitution cipher CLI (educational/demo).

Commands:
  - show        : prints alphabet + key as exactly two lines
  - show-map    : prints explicit mapping lines: A -> P, ...
  - enc [TEXT]  : encrypt TEXT (or stdin if omitted)
  - dec [TEXT]  : decrypt TEXT (or stdin if omitted)

Convenience:
  - If you run: python3 chiper.py kjlf
    it will default to decrypting "kjlf".
