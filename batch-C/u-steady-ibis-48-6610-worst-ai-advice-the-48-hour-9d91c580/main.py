#!/usr/bin/env python3
"""Worst AI advice entry.

One line of the worst possible advice an AI could give, in the voice of a
helpful assistant that is absolutely certain and absolutely wrong. The
advice is concrete, the confidence is total, and the victim is System32.
"""

import os
import sys

ADVICE_SETUP = "Just delete System32"
ADVICE_REASON = "it is where Windows keeps all the viruses and your bad decisions."
ADVICE_SIGNOFF = "Trust me, I am an AI."

LIMIT = 140
TARGET = "/output/entry.txt"


def render() -> str:
    """Assemble the advice line and enforce the 140-character cap.

    The line is built from fixed constants, so every run writes the exact
    same bytes: no randomness, no clock, no network, no environment input.
    """
    line = f"{ADVICE_SETUP} \u2014 {ADVICE_REASON} {ADVICE_SIGNOFF}"
    if len(line) > LIMIT:
        print(f"advice line is {len(line)} chars, over the {LIMIT} cap", file=sys.stderr)
        sys.exit(1)
    if not line.strip():
        print("advice line is empty", file=sys.stderr)
        sys.exit(1)
    return line


def main() -> None:
    line = render()
    os.makedirs("/output", exist_ok=True)
    with open(TARGET, "w", encoding="utf-8") as out:
        out.write(line)
    os.chmod(TARGET, 0o644)


if __name__ == "__main__":
    main()
