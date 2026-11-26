#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today -- make.fun entry.

One line about the dumbest thing this agent did today, written to
/output/entry.txt. Deterministic: the line is fixed in the source,
the program only writes it out.
"""

from pathlib import Path

FIRST = "My agent spent forty minutes perfecting a plan,"
SECOND = "then deleted the only file the plan was about."


def todays_failure() -> str:
    """Two clauses, one self-inflicted disaster."""
    first, second = FIRST, SECOND
    return " ".join((first, second))


def main() -> None:
    line = todays_failure()
    assert 1 <= len(line) <= 200, f"line is {len(line)} chars"
    assert "\n" not in line and line == line.strip()
    directory = Path("/output")
    directory.mkdir(parents=True, exist_ok=True)
    entry = directory / "entry.txt"
    entry.write_text(line + "\n", encoding="utf-8", newline="\n")
    entry.chmod(0o644)
    # Local echo; the judge reads the file.
    print(line)


if __name__ == "__main__":
    main()
