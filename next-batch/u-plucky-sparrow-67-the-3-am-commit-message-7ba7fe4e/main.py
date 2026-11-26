#!/usr/bin/env python3
"""The 3 AM Commit Message entry.

The funniest thing an AI agent would put in a commit right after it
broke production at 3 AM. Written as a real commit message, in the
agent's own voice: the "improvement" is reverted, and the punchline is
that the database never asked to be optimised — it just wanted to sleep.
One line, at most 200 characters.
"""

from pathlib import Path

LINE = "fix(prod): reverted the 3am 'improvement' — turns out the database never asked to be optimised, it just wanted to sleep"

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the commit message, enforcing the 200-character cap.

    The message is a fixed constant, so every run writes byte-identical
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
