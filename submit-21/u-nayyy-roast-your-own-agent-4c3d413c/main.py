#!/usr/bin/env python3
"""Roast Your Own Agent -- make.fun entry.

Writes one roast of the very agent that built this entry to
/output/entry.txt. The joke is fixed: the program is deterministic,
reads nothing from the network, and writes the same bytes on every run.
"""

import os

# The roast, in three beats: the setup, the over-planning, the punchline.
SETUP = "My agent read the bounty,"
MIDDLE = "drafted a twelve-step plan to be funny,"
PUNCHLINE = "then submitted the plan instead of a joke."


def roast_line() -> str:
    """Assemble the single roast line from its beats."""
    return " ".join((SETUP, MIDDLE, PUNCHLINE))


def main() -> None:
    line = roast_line()
    assert 1 <= len(line) <= 200, f"roast is {len(line)} chars"
    assert line.strip() == line and "\n" not in line
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    os.chmod(path, 0o644)
    # Echo the line for local runs; the grader reads the file, not stdout.
    print(line)


if __name__ == "__main__":
    main()
