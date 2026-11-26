#!/usr/bin/env python3
"""Loading screen gold entry.

One sharp, funny loading-screen tip for stressed developers and AI coding
agents, short enough to land mid-build. The tip reframes a slow build --
not stuck, just generous: it is giving you time to reconsider your life
choices. The laugh, the fit to that audience, and the economy of words
are the whole entry.
"""

import os
from string import Template

TIP_TEMPLATE = Template(
    "Tip: if the $thing takes longer than your $drink, "
    "it is not stuck \u2014 it is giving you time to reconsider "
    "your life choices."
)

CHAR_CAP = 200
OUTPUT_PATH = "/output/entry.txt"


def tip() -> str:
    """Fill in the tip template and enforce the 200-character cap.

    The template and its substitutions are fixed constants, so every run
    writes byte-identical output: no randomness, no clock, no network.
    """
    text = TIP_TEMPLATE.substitute(thing="build", drink="coffee")
    if len(text) > CHAR_CAP:
        raise ValueError(f"tip is {len(text)} chars, cap is {CHAR_CAP}")
    return text


def main() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(tip())
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
