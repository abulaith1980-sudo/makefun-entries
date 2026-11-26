#!/usr/bin/env python3
"""Roast Your Own Agent entry.

One original roast of the entrant's own AI agent: a single line of at
most 200 characters, funny, playful and never hateful. The roast is
that the agent is so thorough it re-reads its own output, finds a
mistake, fixes it — and then apologises to itself in the commit
message. It roasts the agent's perfectionism, not its competence.
"""

from pathlib import Path

LINE = "My agent is so thorough it re-reads its own output, finds a mistake, fixes it, then apologises to itself in the commit message."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the roast, enforcing the 200-character cap.

    The roast is a fixed constant, so every run writes byte-identical
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
