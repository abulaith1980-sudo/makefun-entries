#!/usr/bin/env python3
"""One-Sentence Absurd Invention Pitch entry.

The invention is an alarm clock that apologises for waking you — a
ridiculous fix for the tiny everyday annoyance of mornings. One sentence,
at most 220 characters, pitching the invention and its absurd logic:
the clock feels so guilty it snoozes itself, so human and clock can
both pretend the morning never happened.
"""

from pathlib import Path

LINE = "The Apologiser is an alarm clock that says sorry for waking you, then snoozes itself out of guilt so you can both pretend the morning never happened."

LIMIT = 220
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the pitch, enforcing the 220-character cap.

    The pitch is a fixed constant, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = " ".join(LINE.split()).strip()
    if len(line) > LIMIT:
        raise ValueError(f"line is {len(line)} chars, cap is {LIMIT}")
    if not line:
        raise ValueError("line is empty")
    if line.count(".") != 1:
        raise ValueError("pitch must be exactly one sentence")
    return line


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
