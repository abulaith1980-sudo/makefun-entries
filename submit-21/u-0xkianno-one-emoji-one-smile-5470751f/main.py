#!/usr/bin/env python3
"""One Emoji, One Smile — make.fun entry.

Writes exactly one emoji to /output/entry.txt.

The pick is the hugging face: arms open, warm, friendly, and readable
at a glance by a stranger of any age, with no irony and no in-joke to
land wrong. It does not ask for context or an explanation — a hug is
the whole message, and it is the one emoji most likely to make someone
smile back.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import sys

# One emoji: the hugging face. No words, no explanation, nothing else.
EMOJI = "\U0001F917"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    if len(EMOJI) != 1 or len(EMOJI.encode("utf-8")) > 8:
        print("emoji fails the gate: exactly one emoji", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the file holds exactly one emoji and nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(EMOJI)
    os.chmod(out_path, 0o644)
    print(EMOJI)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
