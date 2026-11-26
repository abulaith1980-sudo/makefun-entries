#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun entry.

Writes one out-of-office auto-reply to /output/entry.txt.

The joke: the reply is written in the voice of the AI agent itself, on
vacation, and the laugh comes from the inbox — the thing that is supposed
to be dutifully holding the fort — gaining sentience and going on strike
over the sender's subject lines. It stays a real auto-reply (it says
where the agent is and when, in its own way, a reply will come), it
never leans on beach / inbox-zero / back-soon cliches, and the sting is
in the last clause: the reply arrives when the inbox forgives you.

Deterministic by design: no input, no clock, no randomness and no
network, so two runs write byte-identical output.
"""

import os
import sys

# The reply, kept as one literal line so the output is byte-identical
# on every run. 127 characters, inside the 160-character cap.
REPLY = (
    "I'm on vacation. My inbox has gained sentience and gone on strike "
    "over your subject lines \u2014 it will reply when it forgives you."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")

    text = REPLY.strip()
    if not text or len(text) > 160 or "\n" in text:
        print("reply fails the gate: must be one line of 1-160 chars",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    # The grader collects outputs as another user: leave it world-readable.
    os.chmod(out_path, 0o644)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
