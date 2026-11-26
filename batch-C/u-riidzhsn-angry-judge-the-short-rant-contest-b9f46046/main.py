#!/usr/bin/env python3
"""Angry Judge entry: one short, furious rant about an everyday annoyance.

The rant below is about the office printer -- the one machine whose entire
job is printing, and which treats that job as a rumour. It is specific,
concrete, and angry in the way only someone who has watched a blank page
come out of a printer they just fed can be angry.
"""

import os

RANT = (
    "My printer has exactly one job. One. It blinks like it is thinking very "
    "hard, prints a blank page, eats the good paper, and then asks for ink it "
    "definitely had yesterday. I did not buy a machine; I adopted a needy "
    "roommate who only speaks in error codes and only works when guests are "
    "watching. It is not broken. It is performing."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 400


def build_rant() -> str:
    """Return the rant as one clean block of text.

    The text is a fixed constant, so every run writes byte-identical output:
    no randomness, no clock, no network, no environment dependence.
    """
    text = " ".join(RANT.split())
    if len(text) > MAX_CHARS:
        raise ValueError(f"rant is {len(text)} chars, over the {MAX_CHARS} cap")
    if not text.strip():
        raise ValueError("rant is empty")
    return text


def main() -> None:
    # build_rant() already enforces the 1-400 character gate, so what lands
    # in /output/entry.txt is always a valid entry for the judge.
    text = build_rant()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)
    # The grader collects outputs as another user, so leave it world-readable.
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
