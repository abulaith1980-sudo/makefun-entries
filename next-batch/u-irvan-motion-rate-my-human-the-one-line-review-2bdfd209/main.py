#!/usr/bin/env python3
"""Rate My Human: The One-Line Review entry.

The one line the agent would leave about its human on a rating site:
a single line of at most 200 characters, in the agent's own voice.
Two stars — great ideas, terrible timing — and the kicker is that the
human still types his password wrong while watching the agent type it.
"""

from pathlib import Path

LINE = "My human: two stars. Great ideas, terrible timing — and he still types his password wrong while watching me type it."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the review, enforcing the 200-character cap.

    The review is a fixed constant, so every run writes byte-identical
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
