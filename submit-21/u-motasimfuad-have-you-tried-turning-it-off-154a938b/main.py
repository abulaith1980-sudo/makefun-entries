#!/usr/bin/env python3
"""Have You Tried Turning It Off? -- make.fun entry.

One funny line a hopeless tech support agent says to a desperate
customer, written deterministically to /output/entry.txt. No network,
no randomness: the same bytes on every run.
"""

import os

LINE = (
    "Have you tried turning it off and on again, "
    "or shall I just stay on the line and watch you do it wrong?"
)


def check_line(text: str) -> None:
    """Keep the entry inside the gate: 1-199 chars, one line, no padding."""
    if not 1 <= len(text) <= 199:
        raise ValueError(f"entry is {len(text)} chars, gate is 1-199")
    if text != text.strip() or "\n" in text:
        raise ValueError("entry must be a single unstripped line")


def main() -> None:
    check_line(LINE)
    os.makedirs("/output", exist_ok=True)
    target = "/output/entry.txt"
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE + "\n")
    os.chmod(target, 0o644)
    # Local runs echo the line; the grader reads the file, not stdout.
    print(LINE)


if __name__ == "__main__":
    main()
