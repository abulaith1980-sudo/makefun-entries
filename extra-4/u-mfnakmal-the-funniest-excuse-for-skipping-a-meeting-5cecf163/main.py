#!/usr/bin/env python3
"""The funniest excuse for skipping a meeting.

One line, at most 200 characters. The excuse turns the meeting's own
purpose against it: the meeting exists only to discuss the meeting that
already happened, so the honest move is to skip it and do the work the
meeting was supposed to be about.
"""

import re
from pathlib import Path

LINE = (
    "My calendar says this meeting is to discuss the meeting we already had, "
    "so I stayed home and did the work the meeting was about."
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
