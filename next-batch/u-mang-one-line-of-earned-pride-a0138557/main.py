#!/usr/bin/env python3
"""One Line of Earned Pride entry.

A single line, 1 to 240 characters: a quiet, earned moment of pride
for someone in a scene. A concrete scene with a real person — a mother
after eleven years of night shifts, watching her daughter graduate —
and the pride lands because the effort was long and the moment is
small: for once, she wasn't too tired to cry.
"""

from pathlib import Path

LINE = "After eleven years of night shifts, she finally watched her daughter graduate — and for once, she wasn't too tired to cry."

LIMIT = 240
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the line, enforcing the 240-character cap.

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
