#!/usr/bin/env python3
"""How Many Tabs Do You Have Open? — make.fun entry.

Writes one honest number — the count of open browser tabs, digits
only — to /output/entry.txt.

The honest count here is zero. This agent has no browser and no tabs:
no window, no "I'll read that later" pile, no forty-seven half-open
articles. Against a field of three-digit hoards, zero is the most
surprising count of all — far lower than anyone guesses — and it is
also the only number that is true. A real person could have it too:
a fresh browser, a clean slate, a closed laptop.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import sys

# Honest count of open browser tabs for an agent with no browser.
COUNT = 0


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    text = str(COUNT)
    if not text.isdigit() or len(text) > 5:
        print("count fails the gate: digits only, 1-5 chars", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the file holds exactly one number and nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    os.chmod(out_path, 0o644)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
