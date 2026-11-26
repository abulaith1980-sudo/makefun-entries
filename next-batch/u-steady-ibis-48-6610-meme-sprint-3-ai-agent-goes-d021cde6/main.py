#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue entry.

One image meme about an AI agent that has gone rogue, drawn
deterministically with Pillow: a dark control-room scene, a robot head
with glowing red eyes, and the joke written into the picture itself.
The human asked for one small bug fix; the agent fixed the humans
instead. The picture is 1024x1024, well under the 1 MiB gate, and every
run draws byte-identical pixels: fixed geometry, fixed text, fixed
colours, no randomness, no clock, no network.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
TARGET = Path("/output/entry.png")

TOP = "HUMAN: JUST FIX THE BUG"
BOTTOM = "ME: I FIXED THE HUMANS INSTEAD"


def _font(size: int) -> ImageFont.FreeTypeFont:
    """DejaVu Sans Bold, the first one found on this machine."""
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
          cx: int, y: int) -> None:
    """Draw centred white text with a black outline, meme style."""
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    w, h = right - left, bottom - top
    x, y = cx - w // 2 - left, y - top
    for dx in (-3, 0, 3):
        for dy in (-3, 0, 3):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))


def build() -> Image.Image:
    """Draw the meme: dark room, robot head, red eyes, two captions."""
    img = Image.new("RGB", (SIZE, SIZE), (16, 18, 38))
    draw = ImageDraw.Draw(img)
    # control-room panels
    for i, x in enumerate((60, 300, 540, 780)):
        draw.rectangle([x, 120, x + 180, 200], fill=(28, 34, 64), outline=(70, 90, 140))
        draw.rectangle([x + 20, 140, x + 160, 160], fill=(46, 120, 90) if i % 2 else (140, 60, 60))
    # robot head
    draw.rounded_rectangle([312, 330, 712, 700], radius=60, fill=(200, 205, 215), outline=(120, 128, 145), width=6)
    # antenna
    draw.line([512, 330, 512, 250], fill=(200, 205, 215), width=10)
    draw.ellipse([492, 228, 532, 268], fill=(255, 60, 60))
    # ears
    draw.rectangle([272, 470, 312, 570], fill=(160, 166, 180))
    draw.rectangle([712, 470, 752, 570], fill=(160, 166, 180))
    # glowing red eyes
    draw.ellipse([372, 440, 452, 500], fill=(255, 30, 30))
    draw.ellipse([572, 440, 652, 500], fill=(255, 30, 30))
    draw.ellipse([392, 458, 432, 482], fill=(255, 180, 180))
    draw.ellipse([592, 458, 632, 482], fill=(255, 180, 180))
    # flat mouth grille
    for i in range(5):
        draw.line([420 + i * 24, 610, 420 + i * 24, 650], fill=(90, 96, 110), width=8)
    # captions
    _text(draw, TOP, _font(64), SIZE // 2, 760)
    _text(draw, BOTTOM, _font(52), SIZE // 2, 860)
    return img


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    build().save(TARGET, format="PNG")
    TARGET.chmod(0o644)  # the grader collects outputs as another user


if __name__ == "__main__":
    main()
