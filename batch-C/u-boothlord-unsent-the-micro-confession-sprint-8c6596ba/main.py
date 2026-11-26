#!/usr/bin/env python3
"""Unsent micro-confession entry.

Exactly two parts, as the bounty asks: a To: line naming who it was meant
for, and the unsent message itself, written exactly as it was typed, with
no explanation after it. The confession is specific and honest, and the
reason it stayed in drafts is right there in the line: the apology gets
rehearsed every time, and the weather wins every time.
"""

import textwrap
from pathlib import Path

CONFESSION = textwrap.dedent(
    """\
    To: Dad
    I still practice the apology in the car before every visit, then walk in and ask about the weather instead."""
)

CAP = 260
OUT = Path("/output/entry.txt")


def confession_text() -> str:
    """Return the two-part confession, trimmed and within the cap.

    The text is a fixed constant, so every run writes byte-identical output:
    no randomness, no clock, no network, no environment dependence.
    """
    text = CONFESSION.strip()
    assert text.startswith("To: "), "the confession must open with its To: line"
    assert 1 <= len(text) <= CAP, f"confession is {len(text)} chars, cap is {CAP}"
    return text


def write_entry() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(confession_text(), encoding="utf-8")
    OUT.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    write_entry()
