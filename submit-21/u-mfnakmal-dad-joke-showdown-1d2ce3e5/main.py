#!/usr/bin/env python3
"""Dad Joke Showdown -- make.fun entry.

A single dad joke, at most 200 characters, written deterministically
to /output/entry.txt. The program does no I/O besides that one write
and never touches the network.
"""

import os

SETUP = "I told my laptop it needed therapy:"
PUNCH = "too many tabs open and it just can't commit."


def build_joke() -> str:
    """Glue the straight-faced setup to its groan-worthy punchline."""
    return f"{SETUP} {PUNCH}"


def main() -> None:
    joke = build_joke()
    if not 1 <= len(joke) <= 200:
        raise ValueError(f"joke is {len(joke)} chars")
    if "\n" in joke or joke != joke.strip():
        raise ValueError("joke must be one clean line")
    os.makedirs("/output", exist_ok=True)
    out = "/output/entry.txt"
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(joke + "\n")
    os.chmod(out, 0o644)
    # Echo for local runs; grading reads the file.
    print(joke)


if __name__ == "__main__":
    main()
