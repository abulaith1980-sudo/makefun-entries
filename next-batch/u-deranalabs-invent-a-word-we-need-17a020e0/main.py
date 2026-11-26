#!/usr/bin/env python3
"""Invent a Word We Need entry.

One new English word that does not exist yet, defined in one clear line
of at most 140 characters. The word names a moment with no name yet:
opening the fridge for one thing and leaving with a full meal, with no
memory of deciding. The word is sayable, spellable and memorable, and
the definition lands in one reading.
"""

from pathlib import Path

LINE = "snackcident (n.): opening the fridge for one thing and leaving with a full meal and no memory of deciding."

LIMIT = 140
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the word and definition, enforcing the 140-character cap.

    The entry is a fixed constant, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = " ".join(LINE.split()).strip()
    if len(line) > LIMIT:
        raise ValueError(f"line is {len(line)} chars, cap is {LIMIT}")
    if not line:
        raise ValueError("line is empty")
    return line


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
