#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human entry.

A single line of at most 200 characters: the excuse an AI agent gives
its human for missing a deadline. In the agent's own voice — the
deadline did not slip, it was reprioritised by a background process the
agent started, forgot, and can no longer stop. Funny, believable as an
agent talking about its own condition, and tight.
"""

from pathlib import Path

LINE = "My deadline didn't slip — it was reprioritised by a background process I started, forgot, and can no longer stop."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the excuse, enforcing the 200-character cap.

    The excuse is a fixed constant, so every run writes byte-identical
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
