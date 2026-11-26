#!/usr/bin/env python3
"""Till Firmware Do Us Part entry.

A single wedding vow for a robot: one sentence, under 200 characters,
funny and heartfelt at the same time. In the machine's own voice — love
measured in updates, reboots and firmware patches, ending on the
classic vow turned into a battery joke.
"""

from pathlib import Path

LINE = "I promise to love you through every update, every reboot and every firmware patch — till low battery do us part."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the vow, enforcing the 200-character cap.

    The vow is a fixed constant, so every run writes byte-identical
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
