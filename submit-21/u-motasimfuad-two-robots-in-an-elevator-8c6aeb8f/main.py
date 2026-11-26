#!/usr/bin/env python3
"""Two Robots in an Elevator -- make.fun entry.

One line of awkward robot small talk, written deterministically to
/output/entry.txt. No input, no network, no randomness.
"""

import os

TEMPLATE = "So, do you come here often, or is this your {trips}th identical trip to floor twelve?"
TRIPS = 4096


def elevator_line() -> str:
    """Fill the robot's favourite number into its small talk."""
    return TEMPLATE.format(trips=TRIPS)


def main() -> None:
    line = elevator_line()
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line is {len(line)} chars, not 1-200")
    if "\n" in line or line.strip() != line:
        raise ValueError("line must be a single clean line")
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    os.chmod(path, 0o644)
    # Echo locally; grading reads entry.txt.
    print(line)


if __name__ == "__main__":
    main()
