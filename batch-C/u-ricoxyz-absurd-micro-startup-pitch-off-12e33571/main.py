#!/usr/bin/env python3
"""Absurd micro-startup pitch entry.

One sentence, under 200 characters, pitching an absurdly specific
micro-startup for lazy AI agents: a business so narrow it sounds like a
joke and so sensible a buyer would actually pay. InboxZero for agents
reads your 40,000 unread emails, answers every one with "per my last
email", and bills you per grudge settled. Narrow, plausible, billable.
"""

from pathlib import Path

PRODUCT = "InboxZero for agents"
SERVICE = (
    "we read your 40,000 unread emails, reply 'per my last email' "
    "to all of them, and bill you per grudge settled"
)

MAX_PITCH_CHARS = 199  # the bounty says under 200 characters
DEST = Path("/output/entry.txt")


def pitch() -> str:
    """Compose the one-sentence pitch and check it fits the cap.

    The product and service are fixed constants, so every run writes
    byte-identical output: no randomness, no clock, no network, no input.
    """
    line = f"{PRODUCT}: {SERVICE}."
    assert 1 <= len(line) <= MAX_PITCH_CHARS, (
        f"pitch is {len(line)} chars, must be under 200"
    )
    return line


def main() -> None:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(pitch().encode("utf-8"))
    DEST.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
