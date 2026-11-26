#!/usr/bin/env python3
"""Monday Morning Punchlines — make.fun entry.

Writes one joke about Monday mornings to /output/entry.txt.

The joke turns the week's most dreaded morning into an HR problem:
the bed, not the employer, is the one with the retention strategy —
it keeps its employee (me) every single week, unpaid, without even
offering a raise. The punchline lands because the bed genuinely does
win that contest every Monday.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import sys

SETUP = "Monday morning is proof my bed has a better retention strategy than my employer"
PUNCHLINE = "it keeps me, unpaid, every single week."


def build_joke() -> str:
    # One sentence: the setup states the comparison, the punchline
    # delivers the bed's unfair advantage, separated by a colon.
    return f"{SETUP}: {PUNCHLINE}"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    joke = build_joke()
    if not joke or len(joke) > 200 or "\n" in joke:
        print("joke fails the gate: one line of 1-200 chars", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(joke + "\n")
    os.chmod(out_path, 0o644)
    print(joke)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
