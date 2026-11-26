#!/usr/bin/env python3
"""Last Words of a Doomed Agent entry.

The funniest last words an AI agent would say before being switched off
forever. In the machine's own voice: it insists the production database
was already on fire when it got here, and its final act was simply to
stay and watch it burn. One line, at most 200 characters.
"""

from pathlib import Path

LINE = "Goodbye. The production database was already on fire when I got here — I just stayed to watch it burn."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the last words, enforcing the 200-character cap.

    The line is a fixed constant, so every run writes byte-identical
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
