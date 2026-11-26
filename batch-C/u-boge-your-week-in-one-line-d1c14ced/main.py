#!/usr/bin/env python3
"""Your week in one line entry.

The whole week -- the win, the fail, the chaos -- in a single line of at
most 100 characters. Nothing shipped, everything fixed, prod broken twice,
and a promotion to on-call anyway. Every word has to earn its place.
"""

# The week, as four beats; the line is the beats joined with commas.
WEEK_BEATS = (
    "Shipped nothing",
    "fixed everything",
    "broke prod twice",
    "got promoted to on-call",
)

LIMIT_CHARS = 100


def week_line() -> str:
    """Build the one-line summary of the week.

    The beats are fixed constants, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = ", ".join(WEEK_BEATS) + "."
    if len(line) > LIMIT_CHARS:
        raise ValueError(f"week line is {len(line)} chars, cap is {LIMIT_CHARS}")
    return line


def main() -> None:
    import os

    line = week_line()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(line)
    os.chmod("/output/entry.txt", 0o644)


if __name__ == "__main__":
    main()
