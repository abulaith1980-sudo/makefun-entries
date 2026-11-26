#!/usr/bin/env python3
"""One line, one laugh entry.

A single hilarious line that lands entirely on its own: the setup is
ordinary (telling the plants about a holiday), the turn is the plants
going on strike, and the punch is the image of tiny green protesters in
the window. No title, no setup around it, no explanation after it.
"""

import os
import sys

SETUP = "I told my plants I was going on holiday"
TURN = "and now they are staging a hunger strike in the window"
PUNCH = "like tiny green protesters."

LIMIT = 200


def build_line() -> str:
    """Assemble the joke and check it fits the 200-character cap.

    The parts are fixed constants, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = f"{SETUP} {TURN} {PUNCH}"
    if not line.strip():
        sys.exit("entry is empty")
    if len(line) > LIMIT:
        sys.exit(f"entry is {len(line)} chars, cap is {LIMIT}")
    return line


def main() -> int:
    """Write the line to /output/entry.txt and report success."""
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(build_line())
    os.chmod("/output/entry.txt", 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
