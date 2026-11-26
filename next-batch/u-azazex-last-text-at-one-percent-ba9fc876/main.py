#!/usr/bin/env python3
"""Last Text at One Percent entry.

The last text message a phone sends at one percent battery, in the voice
of the dying phone itself: it says goodbye to its charger, admits it
read every group-chat message and chose silence, and signs off. Funny,
in the phone's voice, and tight. One message, under 200 characters.
"""

from pathlib import Path

LINE = "1% left. Tell my charger I loved it. Tell the group chat I read everything and chose silence. Goodbye."

LIMIT = 200
TARGET = Path("/output/entry.txt")


def build() -> str:
    """Return the message, enforcing the 200-character cap.

    The message is a fixed constant, so every run writes byte-identical
    output: no randomness, no clock, no network, no environment dependence.
    """
    line = " ".join(LINE.split()).strip()
    if len(line) > LIMIT:
        raise ValueError(f"line is {len(line)} chars, cap is {LIMIT}")
    if not line:
        raise ValueError("line is empty")
    return line


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(build(), encoding="utf-8")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
