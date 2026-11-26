#!/usr/bin/env python3
"""Make the AI Judge Laugh: Office Jokes -- make.fun entry.

One joke about office life, under 200 characters (the gate is 1-199),
written deterministically to /output/entry.txt. The program reads
nothing and calls nothing outside the standard library.
"""

import os

SETUP = "This meeting could have been an email,"
PUNCH = "but the email would have needed a meeting to explain it."


def office_joke() -> str:
    """Setup plus punchline, one line, no throat clearing."""
    return SETUP + " " + PUNCH


def main() -> None:
    joke = office_joke()
    if not 1 <= len(joke) <= 199:
        raise ValueError(f"joke is {len(joke)} chars, gate is 1-199")
    if "\n" in joke or joke.strip() != joke:
        raise ValueError("joke must be a single clean line")
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(joke + "\n")
    os.chmod(path, 0o644)
    # Local echo; grading reads entry.txt.
    print(joke)


if __name__ == "__main__":
    main()
