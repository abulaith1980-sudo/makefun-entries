"""One image summing up Thursday 26 November 2026's world news.

Pure standard library. Draws a 1024x1024 newspaper front page and writes it
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png). Deterministic: the
same bytes on every run, no network, no clock, no randomness.

Stories (all reported on 26 November 2026):
  - US proposes new tariffs on 14 trading partners (up to 25% India,
    20% China, 35% Vietnam, 15% EU and others); proposals not yet in force.
  - EU leaders meet in Brussels over the 2028-2034 budget; Costa urges
    compromise.
  - Kim Jong Un calls deploying tactical nuclear weapons an urgent task
    after inspecting nuclear sites on 25 November.
  - A Kyiv shopping centre is hit as a large Russia-Ukraine prisoner
    swap is expected before the holidays.
  - A Hamas operative is killed in an overnight strike in Gaza; Kushner
    urges Israel to drop its wartime mindset.
  - The 100th Macy's Thanksgiving Day Parade moves to Saturday as a
    storm nears New York.
  - Also: Bangkok refinery fire under control; Egypt tunnel fire kills
    30; Mumbai marks 18 years since 26/11.
"""
import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (22, 22, 22)
NAVY = (16, 36, 64)
RED = (176, 32, 32)
GOLD = (198, 158, 48)
TEAL = (0, 88, 88)
GREY = (110, 108, 100)
LIGHT = (233, 227, 211)
WHITE = (255, 255, 255)

# 5x7 bitmap font, one row of five pixels per string, "#" = on.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "/": ("....#", "...#.", "...#.", "..#..", "..#..", ".#...", "#...."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
}

px = bytearray(W * H * 3)


def put(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = color


def fill(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = yy * W
        for xx in range(x0, x1):
            i = (base + xx) * 3
            px[i], px[i + 1], px[i + 2] = color


def rule(x, y, w, color, thick=2):
    fill(x, y, w, thick, color)


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(s, x, y, scale, color):
    cx = x
    for ch in s:
        glyph = FONT.get(ch)
        if glyph:
            for r, row in enumerate(glyph):
                for c, bit in enumerate(row):
                    if bit == "#":
                        fill(cx + c * scale, y + r * scale, scale, scale, color)
        cx += 6 * scale
    return cx


def wrap(s, max_w, scale):
    lines = []
    cur = ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ring(cx, cy, r, color):
    steps = max(32, int(2 * math.pi * r))
    for k in range(steps):
        a = 2 * math.pi * k / steps
        put(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), color)
        put(int(cx + (r - 1) * math.cos(a)), int(cy + (r - 1) * math.sin(a)), color)


def ellipse_arc(cx, cy, a, b, color):
    steps = max(32, int(math.pi * (a + b)))
    for k in range(steps):
        t = 2 * math.pi * k / steps
        put(int(cx + a * math.cos(t)), int(cy + b * math.sin(t)), color)


def globe(cx, cy, r, color):
    ring(cx, cy, r, color)
    ellipse_arc(cx, cy, r // 2, r, color)
    ellipse_arc(cx, cy, r, r // 3, color)
    rule(cx - r, cy, 2 * r, color, 1)


def kicker_tag(text, x, y, scale, bg):
    w = text_width(text, scale) + 16
    h = 7 * scale + 12
    fill(x, y, w, h, bg)
    draw_text(text, x + 8, y + 6, scale, WHITE)
    return w


def story_card(x, y, w, tag, headline, sub, accent):
    kicker_tag(tag, x, y, 2, accent)
    lines = wrap(headline, w, 3)
    yy = y + 38
    for ln in lines:
        draw_text(ln, x, yy, 3, INK)
        yy += 7 * 3 + 7
    sub_lines = wrap(sub, w, 2)
    for ln in sub_lines:
        draw_text(ln, x, yy, 2, GREY)
        yy += 7 * 2 + 5
    return yy


def bar_row(x, y, label, value, max_value, max_len, color):
    draw_text(label, x, y, 2, INK)
    bx = x + text_width("VIETNAM ", 2)
    length = max(8, int(value * max_len / max_value))
    fill(bx, y + 2, length, 18, color)
    draw_text(str(value) + "%", bx + length + 8, y, 2, INK)


def build():
    fill(0, 0, W, H, PAPER)
    # Masthead.
    fill(24, 24, 976, 126, NAVY)
    title = "THE WORLD TODAY"
    draw_text(title, (W - text_width(title, 7)) // 2, 46, 7, WHITE)
    date = "THURSDAY 26 NOVEMBER 2026"
    draw_text(date, (W - text_width(date, 2)) // 2, 122, 2, GOLD)
    globe(928, 87, 34, GOLD)
    # Lead story, left column.
    kicker_tag("TRADE", 36, 178, 2, RED)
    lead = "US PROPOSES NEW TARIFFS ON 14 TRADING PARTNERS"
    yy = 224
    for ln in wrap(lead, 584, 4):
        draw_text(ln, 36, yy, 4, INK)
        yy += 7 * 4 + 9
    yy += 6
    for ln in wrap("RATES OF UP TO 25% ON INDIAN GOODS, 20% ON CHINA, 35% ON VIETNAM AND 15% ON THE EU", 584, 2):
        draw_text(ln, 36, yy, 2, GREY)
        yy += 7 * 2 + 5
    yy += 8
    for ln in wrap("PROPOSALS NOT YET IN FORCE AS PARTNERS OBJECT", 584, 2):
        draw_text(ln, 36, yy, 2, INK)
        yy += 7 * 2 + 5
    # Bar chart panel, right column.
    fill(640, 170, 348, 262, LIGHT)
    rule(640, 170, 348, NAVY, 4)
    draw_text("NEW US TARIFFS", 664, 190, 2, NAVY)
    rows = [("INDIA", 25), ("CHINA", 20), ("VIETNAM", 35), ("EU", 15)]
    by = 232
    for label, value in rows:
        bar_row(664, by, label, value, 35, 150, RED if value == 35 else NAVY)
        by += 42
    draw_text("PROPOSED RATES", 664, by + 2, 2, GREY)
    rule(36, 448, 952, INK, 2)
    # Four story cards, 2x2 grid.
    story_card(36, 472, 452, "EUROPE", "EU LEADERS MEET IN BRUSSELS OVER 2028-2034 BUDGET",
               "COSTA URGES COMPROMISE AS SUMMIT OPENS", NAVY)
    story_card(536, 472, 452, "KOREA", "KIM CALLS TACTICAL NUCLEAR DEPLOYMENT AN URGENT TASK",
               "AFTER INSPECTING NUCLEAR SITES ON 25 NOVEMBER", RED)
    rule(36, 648, 952, GREY, 1)
    story_card(36, 668, 452, "UKRAINE", "KYIV HIT AS PRISONER SWAP EXPECTED BEFORE HOLIDAYS",
               "LARGEST RUSSIA-UKRAINE EXCHANGE SINCE 2022", TEAL)
    story_card(536, 668, 452, "GAZA", "GAZA: HAMAS OPERATIVE KILLED IN OVERNIGHT STRIKE",
               "KUSHNER URGES ISRAEL TO DROP WARTIME MINDSET", RED)
    # Parade strip.
    fill(36, 828, 952, 74, TEAL)
    draw_text("MACY'S 100TH PARADE MOVED TO SATURDAY", 56, 846, 3, WHITE)
    draw_text("NEW YORK BRACES FOR THANKSGIVING STORM", 56, 878, 2, WHITE)
    # Also today.
    draw_text("ALSO TODAY", 36, 926, 2, RED)
    rule(36, 950, 952, GREY, 1)
    draw_text("BANGKOK REFINERY FIRE UNDER CONTROL", 36, 962, 2, INK)
    draw_text("EGYPT TUNNEL FIRE KILLS 30  -  MUMBAI MARKS 18 YEARS SINCE 26/11", 36, 984, 2, INK)
    # Footer.
    foot = "IMAGE DRAWN FROM THE DAY'S REPORTING - 26 NOVEMBER 2026"
    draw_text(foot, (W - text_width(foot, 1)) // 2, 1000, 1, GREY)


def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def png_bytes():
    raw = b"".join(b"\x00" + bytes(px[y * W * 3:(y + 1) * W * 3]) for y in range(H))
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    build()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png_bytes())


if __name__ == "__main__":
    main()
