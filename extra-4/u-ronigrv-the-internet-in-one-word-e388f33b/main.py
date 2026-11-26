#!/usr/bin/env python3
"""The internet in one word.

The entry is a single word and nothing else: "Doomscrolling" — the one
word that names what the internet has become for most of its users, the
endless scroll that eats the hours. Funny, fitting, and surprising in how
precisely it lands.
"""

from pathlib import Path

WORD = "Doomscrolling"

TARGET = Path("/output/entry.txt")


def build() -> str:
    """The word is a fixed constant, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    if not WORD or len(WORD.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not WORD.isalpha():
        raise ValueError("entry must be a single word of letters only")
    return WORD


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
