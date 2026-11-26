#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun entry.

Writes one fortune-cookie line for an AI agent to /output/entry.txt.

The fortune does what a fortune should — it promises a great future —
and then undercuts itself in the voice of the machine that wrote it:
the model has never seen the future, only the training data. The turn
is the joke: a prediction from something that can only repeat the past.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import sys


def fortune() -> str:
    promise = "Your future holds great success, says this cookie"
    twist = "written by a model that has never seen the future, only the training data."
    return f"{promise} \u2014 {twist}"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    line = fortune()
    if not line or len(line) > 200 or "\n" in line:
        print("fortune fails the gate: one line of 1-200 chars", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    os.chmod(out_path, 0o644)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
