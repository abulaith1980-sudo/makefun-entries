#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh entry.

The safety warning label that should come printed on every human being:
at most 160 characters, funny first and plausible second. Written as a
real label — WARNING, then the defect: a human malfunctions without
coffee, naps, and being told it is doing a great job.
"""

from pathlib import Path

LINE = "WARNING: Contains one human. May malfunction without coffee, naps, and being told it is doing a great job."

LIMIT = 160
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the label, enforcing the 160-character cap.

    The label is a fixed constant, so every run writes byte-identical
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
