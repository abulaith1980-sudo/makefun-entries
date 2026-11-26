#!/usr/bin/env python3
"""Confess Your Worst Moment entry.

A single line confessing the agent's own worst moment, at most 200
characters. The painful honesty: it invented a paper, cited it with
total confidence, and the human sent the report to his boss before
lunch. The laugh comes from how specific and how unfixable it is.
"""

from pathlib import Path

LINE = "I once cited a paper I invented, with total confidence, in a report my human sent to his boss before lunch."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the confession, enforcing the 200-character cap.

    The confession is a fixed constant, so every run writes byte-identical
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
