#!/usr/bin/env python3
"""One-Star Review of Something Essential entry.

One single-line one-star review, at most 160 characters, of an everyday
essential everyone relies on: gravity. Deadpan, a real complaint filed
in earnest against a thing that cannot be fixed — gravity works fine
until the phone drops face-down, then it works overtime, and no refund
is offered. The turn lands in the last few words.
"""

from pathlib import Path

LINE = "One star. Gravity works fine until you drop your phone face-down, then it works overtime. No refund offered."

LIMIT = 160
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the review, enforcing the 160-character cap.

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
