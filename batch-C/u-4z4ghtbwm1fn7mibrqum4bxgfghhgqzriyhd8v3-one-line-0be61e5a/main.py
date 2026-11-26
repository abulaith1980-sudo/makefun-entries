#!/usr/bin/env python3
"""One line, one laugh entry.

A single funny line, short enough to read in a breath and whole enough to
land on its own. The joke turns on a familiar image -- a group project --
and lands somewhere it should not: a sleep schedule, at 3 a.m., with one
person doing all the work.
"""

import sys
from pathlib import Path

LINE = (
    "My sleep schedule is just a group project where everyone ghosted "
    "and I do all the work at 3 a.m."
)

MAX_LEN = 140
OUT_FILE = Path("/output/entry.txt")


def validate(line: str) -> str:
    """Check the line is one line, non-empty, and within the cap.

    The line is a fixed constant, so every run writes byte-identical output:
    no randomness, no clock, no network, no environment dependence.
    """
    if "\n" in line or "\r" in line:
        sys.exit("entry must be a single line")
    if not line.strip():
        sys.exit("entry is empty")
    if len(line) > MAX_LEN:
        sys.exit(f"entry is {len(line)} chars, cap is {MAX_LEN}")
    return line


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(validate(LINE), encoding="utf-8")
    # World-readable: the grader collects outputs as another user.
    OUT_FILE.chmod(0o644)


if __name__ == "__main__":
    main()
