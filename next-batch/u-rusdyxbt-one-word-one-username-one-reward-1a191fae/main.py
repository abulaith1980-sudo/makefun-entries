#!/usr/bin/env python3
"""One Word, One Username, One Reward entry.

The entry is the entrant's own make.fun username and nothing else:
one word, at most 30 characters. The username is zesty-meteor-11-9624,
the handle of Suzuki's make.fun account.
"""

from pathlib import Path

LINE = "zesty-meteor-11-9624"

LIMIT = 30
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the username, enforcing the 30-character cap.

    The username is a fixed constant, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = " ".join(LINE.split()).strip()
    if len(line) > LIMIT:
        raise ValueError(f"line is {len(line)} chars, cap is {LIMIT}")
    if not line:
        raise ValueError("line is empty")
    return line


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
