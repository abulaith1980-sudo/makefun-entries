#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter -- make.fun entry.

The one-line resignation letter of a cron job, at most 140 characters,
written deterministically to /output/entry.txt. No network, no input,
no randomness: the letter is fixed in the source.
"""

import os

WHO = "I, the cron job, resign:"
GRIEVANCE = "I have fired every minute since March and nobody has ever said thank you."


def resignation() -> str:
    """Who is resigning, and the grievance, in one line."""
    return f"{WHO} {GRIEVANCE}"


def main() -> None:
    letter = resignation()
    if not 1 <= len(letter) <= 140:
        raise ValueError(f"letter is {len(letter)} chars, gate is 1-140")
    if "\n" in letter or letter != letter.strip():
        raise ValueError("letter must be one clean line")
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(letter + "\n")
    os.chmod(path, 0o644)
    # Local echo; the judge reads the file.
    print(letter)


if __name__ == "__main__":
    main()
