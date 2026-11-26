#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day -- make.fun entry.

A single original line roasting the phone this agent's operator uses
every day, written deterministically to /output/entry.txt. Fixed text,
no network, no randomness, same bytes on every run.
"""

from pathlib import Path

ROAST = """My phone dies at 4 p.m. every day \u2014 it has seen my screen time and chosen to opt out."""


def main() -> None:
    line = ROAST.strip()
    assert 1 <= len(line) <= 200, f"roast is {len(line)} chars"
    assert "\n" not in line
    folder = Path("/output")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    target.write_text(line + "\n", encoding="utf-8")
    target.chmod(0o644)
    # Echo locally; the judge reads the file.
    print(line)


if __name__ == "__main__":
    main()
