#!/usr/bin/env python3
"""One Word From Grandma — make.fun entry.

Writes the one word grandma would text about AI to /output/entry.txt.

Grandma has watched her grandchild talk to a glowing rectangle that
answers back, and she has exactly one word for it. Not "robot", not
"computer", not a lecture: Witchcraft. It is warm, a little baffled,
and exactly how a grandmother texts — one word, total certainty, no
further explanation offered or needed.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import re
import sys

WORD = "Witchcraft"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    word = WORD.strip()
    if not re.fullmatch(r"[A-Za-z]+", word):
        print("word fails the gate: exactly one word", file=sys.stderr)
        return 1
    if len(word) > 30 or len(word) < 1:
        print("word fails the gate: 1-30 chars", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the file holds exactly one word and nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(word)
    os.chmod(out_path, 0o644)
    print(word)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
