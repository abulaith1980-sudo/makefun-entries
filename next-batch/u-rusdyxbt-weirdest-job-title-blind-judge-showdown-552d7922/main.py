#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown entry.

A single job title, the weirdest one imaginable, in 60 characters or
fewer and nothing else. It sounds like a real corporate title with one
hilariously specific twist: a Senior Vice President whose entire job is
apologising to printers.
"""

from pathlib import Path

LINE = "Senior Vice President of Apologising to Printers"

LIMIT = 60
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the job title, enforcing the 60-character cap.

    The title is a fixed constant, so every run writes byte-identical
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
