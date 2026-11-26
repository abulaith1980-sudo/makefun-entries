#!/usr/bin/env python3
"""Fridge Roast: One Line, Biggest Laugh — make.fun entry.

Writes one roast of a smart fridge to /output/entry.txt.

The roast aims at the fridge itself — its firmware update and its
habit of narrating its owner's life — rather than at kitchens in
general. A fridge that judges your midnight snacks out loud, and
beeps "again?" before the door is even open, has earned the roast.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import sys

ROAST = {
    "target": "My smart fridge",
    "crime": "updated its firmware and now judges my midnight snacks out loud",
    "sting": "it beeps 'again?' before I even open the door.",
}


def build_roast() -> str:
    return f"{ROAST['target']} {ROAST['crime']} \u2014 {ROAST['sting']}"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    line = build_roast()
    if not line or len(line) > 200 or "\n" in line:
        print("roast fails the gate: one line of 1-200 chars", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    os.chmod(out_path, 0o644)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
