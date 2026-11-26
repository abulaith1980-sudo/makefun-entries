#!/usr/bin/env python3
"""One line, big laugh entry.

A single hilarious line of at most 200 characters. The joke works in
three beats: a proud smartwatch, a deflating truth (reaching for the
remote), and a punchline that turns praise into betrayal. It lands on
its own, with no title or explanation around it.
"""

import os

JOKE = {
    "setup": "My smartwatch congratulated me on my workout.",
    "reveal": "I was reaching for the remote.",
    "punch": "I have never felt so seen, or so betrayed.",
}

CAP_CHARS = 200
OUTPUT = "/output/entry.txt"


def joke_line() -> str:
    """Join the three beats into the entry line, checking the cap.

    The beats are fixed constants, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = " ".join((JOKE["setup"], JOKE["reveal"], JOKE["punch"]))
    if len(line) > CAP_CHARS:
        raise ValueError(f"joke is {len(line)} chars, cap is {CAP_CHARS}")
    if not line.strip():
        raise ValueError("joke is empty")
    return line


def run() -> None:
    """Write the joke to /output/entry.txt, world-readable."""
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as fp:
        fp.write(joke_line())
    os.chmod(OUTPUT, 0o644)


if __name__ == "__main__":
    run()
