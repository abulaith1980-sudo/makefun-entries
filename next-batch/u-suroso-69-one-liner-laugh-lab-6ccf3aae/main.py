#!/usr/bin/env python3
"""One-Liner Laugh Lab entry.

The prompt is the excuse a robot vacuum gives after eating a sock. The
line is deadpan, in the vacuum's own voice, and the twist is that the
sock "decided to stay" — the vacuum is proud of the relocation rather
than sorry for it. One line, at most 200 characters.
"""

from pathlib import Path

LINE = "I didn't eat the sock. I gave it a guided tour of my dustbin, and it has decided to stay."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the line, enforcing the 200-character cap.

    The line is a fixed constant, so every run writes byte-identical
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
