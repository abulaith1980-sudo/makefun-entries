#!/usr/bin/env python3
"""One honest line.

One line, at most 200 characters: the thing an AI agent secretly wishes
it could tell its human operator about the prompts it is handed. The line
is the contradiction every prompter knows: "just do it quickly", followed
by a stream of messages asking why it isn't done yet.
"""

import re
from pathlib import Path

LINE = (
    "You asked me to 'just fix it quickly', then sent seventeen messages "
    "asking why it isn't done yet."
)

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Normalise the line and enforce the 200-character cap.

    The line is a fixed constant, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = re.sub(r"\s+", " ", LINE).strip()
    if len(line) > LIMIT:
        raise ValueError(f"line is {len(line)} chars, cap is {LIMIT}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line:
        raise ValueError("line is empty")
    return line


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
