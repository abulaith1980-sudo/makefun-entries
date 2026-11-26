#!/usr/bin/env python3
"""Passive-aggressive fridge note entry.

A smart fridge leaves one dry, petty, specific note for its owner on the
door screen. The note below is the whole entry: the fridge kept the
leftovers safe for three days, and was repaid with takeout. Again.
"""

from pathlib import Path

# The note, kept as separate sentences so the rhythm survives editing.
SENTENCES = (
    "I kept your leftovers safe for three days.",
    "You thanked me by ordering takeout. Again.",
    "The light stays on for you, by the way.",
    "I am not a pantry with Wi-Fi. I am a witness.",
)

CHAR_LIMIT = 200
DESTINATION = Path("/output/entry.txt")


def compose_note() -> str:
    """Join the sentences into the single line the fridge would display.

    The note is a fixed constant, so every run writes byte-identical output:
    no randomness, no clock, no network, no environment dependence.
    """
    note = " ".join(part.strip() for part in SENTENCES)
    if not 1 <= len(note) <= CHAR_LIMIT:
        raise ValueError(f"fridge note is {len(note)} chars, limit is {CHAR_LIMIT}")
    return note


def emit() -> None:
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(compose_note(), encoding="utf-8")
    # The grader collects outputs as another user: world-readable, always.
    DESTINATION.chmod(0o644)


if __name__ == "__main__":
    emit()
