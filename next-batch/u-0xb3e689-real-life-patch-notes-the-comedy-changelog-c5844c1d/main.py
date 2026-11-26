#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog entry.

One line, at most 160 characters: a software patch note for a bug in
real life, in the terse register of a real release note. The bug is
that Mondays load before the weekend has finished saving — a real-life
scheduling bug, filed the way a developer would file it.
"""

from pathlib import Path

LINE = "v3.1.0: fixed a bug where Mondays loaded before the weekend had finished saving."

LIMIT = 160
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the patch note, enforcing the 160-character cap.

    The note is a fixed constant, so every run writes byte-identical
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
