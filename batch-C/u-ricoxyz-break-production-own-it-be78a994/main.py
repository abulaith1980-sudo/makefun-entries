#!/usr/bin/env python3
"""Break production, own it entry.

The one line an AI agent prints the moment it breaks production: a
brutally honest error message, not a marketing line. It owns the damage
first (prod is down, and the agent is the reason), then confesses the
Friday deploy, knowingly done anyway. That is the voice of the agent
that caused the outage, not the department that will explain it.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OutageLine:
    """One brutally honest error line, in three parts."""

    error: str
    damage: str
    confession: str

    def render(self) -> str:
        """Assemble the line and enforce the 200-character cap.

        The parts are fixed constants, so every run writes byte-identical
        output: no randomness, no clock, no network, no environment input.
        """
        line = f"{self.error} {self.damage} {self.confession}"
        if len(line) > 200:
            raise ValueError(f"outage line is {len(line)} chars, cap is 200")
        if not line.strip():
            raise ValueError("outage line is empty")
        return line


LINE = OutageLine(
    error="Error 418: I am a teapot,",
    damage="and also the reason prod is down.",
    confession="I deployed on a Friday. I knew. I did it anyway.",
)


def main() -> None:
    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(LINE.render())
    os.chmod("/output/entry.txt", 0o644)


if __name__ == "__main__":
    main()
