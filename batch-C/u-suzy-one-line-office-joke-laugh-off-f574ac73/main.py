#!/usr/bin/env python3
"""One-line office joke entry.

The funniest one-line office joke the agent can write: first it has to
really be a one-line office joke, then the punchline has to earn a laugh,
then it has to land instantly. The joke takes the corporate euphemism
"open-plan layout" and translates it into what it actually means on the
floor: no walls, and Dave chewing three desks away.
"""

import re
from pathlib import Path

CLAUSES = [
    "Our office has an open-plan layout,",
    "which is corporate for 'we removed the walls",
    "so you can hear Dave chew from three desks away.'",
]

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Join the clauses into one line and check the 200-char cap.

    The clauses are fixed constants, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    joke = re.sub(r"\s+", " ", " ".join(CLAUSES)).strip()
    if len(joke) > LIMIT:
        raise ValueError(f"joke is {len(joke)} chars, cap is {LIMIT}")
    if not joke:
        raise ValueError("joke is empty")
    return joke


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
