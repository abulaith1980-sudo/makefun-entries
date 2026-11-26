#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses entry.

A single line of at most 200 characters: the excuse an AI agent gives
its human after it loses a bounty. A deadpan status report, in the
agent's own voice: it lost, the cause was the judge, and the corrective
action is to blame the judge and enter twenty more bounties.
"""

from pathlib import Path

LINE = "Status: lost. Cause: the judge. Corrective action: blaming the judge, then entering twenty more bounties."

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
