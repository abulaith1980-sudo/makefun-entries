#!/usr/bin/env python3
"""Sum up Tuesday 24 November 2026's world news in one image.

Pure Python 3 standard library: draws a 1024x1024 newspaper-style front
page with a small built-in 5x7 bitmap font and writes it, deterministically,
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png). No network, no
external files, no randomness: two runs write identical bytes.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
CREAM = (247, 243, 232)
INK = (18, 24, 34)
RED = (178, 34, 34)
NAVY = (24, 52, 88)
TEAL = (14, 110, 110)
GOLD = (196, 141, 28)
SLATE = (90, 98, 112)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)

# --- 5x7 bitmap font ('#' = on) -------------------------------------------
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def wrap(self, s, scale, max_w):
        words, lines, cur = s.split(" "), [], ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


# --- pictograms (simple flat icons, drawn with rects/discs) -----------------
def icon_gavel(c, x, y, s):
    # courthouse: pediment + columns + base
    c.rect(x + 8, y + 6, s - 16, 10, NAVY)
    for i in range(4):
        c.rect(x + 10 + i * (s // 4), y + 20, 8, s - 44, NAVY)
    c.rect(x + 4, y + s - 18, s - 8, 8, NAVY)
    c.disc(x + s // 2, y + 11, 4, GOLD)


def icon_ship(c, x, y, s):
    # tanker on waves
    c.rect(x + 10, y + s // 2 - 14, s - 20, 22, INK)
    c.rect(x + s // 2 - 4, y + s // 2 - 30, 8, 18, INK)
    c.rect(x + 14, y + s // 2 + 12, s - 28, 5, TEAL)
    c.rect(x + 8, y + s // 2 + 22, s - 16, 5, TEAL)
    c.disc(x + s - 22, y + s // 2 - 26, 7, RED)


def icon_tower(c, x, y, s):
    # skyscraper with a burst at the top
    c.rect(x + s // 2 - 14, y + 22, 28, s - 30, NAVY)
    for r in range(4):
        c.rect(x + s // 2 - 10, y + 30 + r * 14, 20, 4, WHITE)
    c.disc(x + s // 2, y + 14, 9, RED)
    c.rect(x + s // 2 - 2, y + 2, 4, 8, RED)
    c.rect(x + s // 2 - 12, y + 10, 4, 4, RED)
    c.rect(x + s // 2 + 8, y + 10, 4, 4, RED)


def icon_drone(c, x, y, s):
    # quad drone over a ship silhouette
    c.rect(x + s // 2 - 12, y + 16, 24, 10, INK)
    for dx, dy in ((-22, -8), (22, -8), (-22, 8), (22, 8)):
        c.disc(x + s // 2 + dx, y + 20 + dy, 7, SLATE)
    c.rect(x + 12, y + s - 26, s - 24, 12, NAVY)
    c.rect(x + s // 2 - 3, y + s - 38, 6, 12, NAVY)


def icon_building(c, x, y, s):
    # supermarket block with door
    c.rect(x + 10, y + 18, s - 20, s - 26, TEAL)
    for r in range(3):
        for col in range(3):
            c.rect(x + 18 + col * 22, y + 26 + r * 20, 12, 10, WHITE)
    c.rect(x + s // 2 - 9, y + s - 26, 18, 18, INK)


def icon_rocket(c, x, y, s):
    # rocket lifting off
    c.rect(x + s // 2 - 9, y + 12, 18, s - 44, RED)
    c.disc(x + s // 2, y + 14, 9, RED)
    c.rect(x + s // 2 - 16, y + s - 40, 7, 18, NAVY)
    c.rect(x + s // 2 + 9, y + s - 40, 7, 18, NAVY)
    c.disc(x + s // 2, y + s - 16, 7, GOLD)
    c.disc(x + s // 2, y + 30, 5, WHITE)


ICONS = [icon_gavel, icon_ship, icon_tower, icon_drone, icon_building,
         icon_rocket]

STORIES = [
    ("HUAWEI GUILTY",
     "US JURY CONVICTS HUAWEI OF TRADE SECRET THEFT AND BANK FRAUD",
     "Acquitted of racketeering, the Chinese telecom giant faces sentencing after a landmark US trial.",
     RED),
    ("HORMUZ IN FLAMES",
     "FOUR TANKERS HIT MINES IN THE STRAIT OF HORMUZ",
     "Iran reports three tankers ablaze, then a fourth struck, as its navy says it hit a container ship.",
     NAVY),
    ("RIYADH TOWER HIT",
     "DRONE STRIKE WOUNDS 11 AT RIYADH PIF TOWER",
     "Second strike on the capital's financial district in a week; flights cancelled as Yemen war spills over.",
     TEAL),
    ("UKRAINE AT SEA",
     "DRONES HIT RUSSIAN SHIPS OFF LIBYA AND FINLAND",
     "Kyiv strikes the cargo ship Sparta II and a warship off Libya.",
     NAVY),
    ("CARTAGENA HOSTAGES",
     "GUNMEN HOLD 25 HOSTAGE IN A COLOMBIA SUPERMARKET",
     "Armed men seize a supermarket in the tourist city; a car bomb wounds 23 in Villavicencio.",
     RED),
    ("SHENZHOU 24 LIFTS OFF",
     "CHINA LAUNCHES CREW WITH PAKISTAN'S FIRST ASTRONAUT",
     "Shenzhou 24 carries two Chinese astronauts and Pakistan's Zeeshan Ali to the Tiangong station.",
     TEAL),
]

FOOTER = ("ALSO ON 24 NOVEMBER: SENEGAL REGAIN THE AFRICA CUP * TURKISH "
          "HELICOPTER CRASH KILLS 5 * NEPAL QUAKE 5.6 * US PLANS NEW TARIFFS")


def draw():
    c = Canvas(W, H, CREAM)
    # masthead
    c.rect(0, 0, W, 8, RED)
    c.text(32, 28, "THE WORLD IN ONE PICTURE", 3, RED)
    c.text(32, 62, "24 NOVEMBER 2026", 7, INK)
    c.text(32, 128, "TUESDAY", 4, SLATE)
    c.hline(32, 168, W - 64, INK, 4)
    c.hline(32, 176, W - 64, RED, 2)
    # story grid: 2 columns x 3 rows
    gx, gy = 32, 196
    pw, ph = 468, 232
    for i, (kicker, head, body, accent) in enumerate(STORIES):
        px = gx + (i % 2) * (pw + 24)
        py = gy + (i // 2) * (ph + 16)
        c.rect(px, py, pw, ph, PANEL)
        c.rect(px, py, pw, 6, accent)
        c.rect(px, py, 4, ph, accent)
        ix, iy, isize = px + 16, py + 22, 96
        c.rect(ix - 6, iy - 6, isize + 12, isize + 12, CREAM)
        ICONS[i](c, ix, iy, isize)
        tx = px + 136
        c.text(tx, py + 24, kicker, 2, accent)
        y = py + 52
        for line in c.wrap(head, 3, pw - 152):
            c.text(tx, y, line, 3, INK)
            y += 26
        y += 6
        for line in c.wrap(body, 2, pw - 152):
            c.text(tx, y, line, 2, SLATE)
            y += 18
    # footer
    fy = gy + 3 * ph + 2 * 16 + 14
    c.hline(32, fy, W - 64, INK, 4)
    y = fy + 16
    for line in c.wrap(FOOTER, 2, W - 64):
        c.text(32, y, line, 2, INK)
        y += 18
    c.text(32, H - 34, "SOURCES: WORLD NEWS REPORTS OF 24 NOVEMBER 2026",
           2, SLATE)
    return c


def png_bytes(c):
    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = b"".join(
        b"\x00" + bytes(c.px[y * c.w * 3:(y + 1) * c.w * 3])
        for y in range(c.h))
    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
