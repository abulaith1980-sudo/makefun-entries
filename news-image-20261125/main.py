"""News image for 25 November 2026. Pure stdlib Python.
Draws a 1024x1024 newspaper-style infographic to /output/entry.png.
Deterministic: no time, no random, no network.
"""
import os
import struct
import zlib

W, H = 1024, 1024
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
NAVY = (16, 42, 90)
TEAL = (0, 110, 110)
RED = (168, 30, 30)
ORANGE = (190, 90, 0)
PURPLE = (90, 50, 140)
GREEN = (30, 120, 60)
GREY = (90, 90, 90)
LIGHT = (240, 242, 245)

FONT = {
    'A': ("01110","10001","10001","11111","10001","10001","10001"),
    'B': ("11110","10001","10001","11110","10001","10001","11110"),
    'C': ("01110","10001","10000","10000","10000","10001","01110"),
    'D': ("11110","10001","10001","10001","10001","10001","11110"),
    'E': ("11111","10000","10000","11110","10000","10000","11111"),
    'F': ("11111","10000","10000","11110","10000","10000","10000"),
    'G': ("01110","10001","10000","10111","10001","10001","01111"),
    'H': ("10001","10001","10001","11111","10001","10001","10001"),
    'I': ("01110","00100","00100","00100","00100","00100","01110"),
    'J': ("00111","00010","00010","00010","00010","10010","01100"),
    'K': ("10001","10010","10100","11000","10100","10010","10001"),
    'L': ("10000","10000","10000","10000","10000","10000","11111"),
    'M': ("10001","11011","10101","10101","10001","10001","10001"),
    'N': ("10001","11001","10101","10011","10001","10001","10001"),
    'O': ("01110","10001","10001","10001","10001","10001","01110"),
    'P': ("11110","10001","10001","11110","10000","10000","10000"),
    'Q': ("01110","10001","10001","10001","10101","10010","01101"),
    'R': ("11110","10001","10001","11110","10100","10010","10001"),
    'S': ("01111","10000","10000","01110","00001","00001","11110"),
    'T': ("11111","00100","00100","00100","00100","00100","00100"),
    'U': ("10001","10001","10001","10001","10001","10001","01110"),
    'V': ("10001","10001","10001","10001","10001","01010","00100"),
    'W': ("10001","10001","10001","10101","10101","10101","01010"),
    'X': ("10001","10001","01010","00100","01010","10001","10001"),
    'Y': ("10001","10001","01010","00100","00100","00100","00100"),
    'Z': ("11111","00001","00010","00100","01000","10000","11111"),
    '0': ("01110","10001","10011","10101","11001","10001","01110"),
    '1': ("00100","01100","00100","00100","00100","00100","01110"),
    '2': ("01110","10001","00001","00110","01000","10000","11111"),
    '3': ("11111","00010","00100","00010","00001","10001","01110"),
    '4': ("00010","00110","01010","10010","11111","00010","00010"),
    '5': ("11111","10000","11110","00001","00001","10001","01110"),
    '6': ("01110","10000","10000","11110","10001","10001","01110"),
    '7': ("11111","00001","00010","00100","01000","01000","01000"),
    '8': ("01110","10001","10001","01110","10001","10001","01110"),
    '9': ("01110","10001","10001","01111","00001","00001","01110"),
    ' ': ("00000","00000","00000","00000","00000","00000","00000"),
    '.': ("00000","00000","00000","00000","00000","01100","01100"),
    ',': ("00000","00000","00000","00000","01100","00100","01000"),
    ':': ("00000","01100","00000","00000","01100","00000","00000"),
    '-': ("00000","00000","00000","11111","00000","00000","00000"),
    '/': ("00001","00010","00010","00100","01000","01000","10000"),
    '$': ("00100","01111","10100","01110","00101","11110","00100"),
    '%': ("11001","11010","00010","00100","01000","01011","10011"),
    '(': ("00010","00100","01000","01000","01000","00100","00010"),
    ')': ("01000","00100","00010","00010","00010","00100","01000"),
    "'": ("00100","00100","01000","00000","00000","00000","00000"),
    '!': ("00100","00100","00100","00100","00100","00000","00100"),
    '?': ("01110","10001","00001","00110","00100","00000","00100"),
    '&': ("01100","10010","10100","01000","10101","10010","01101"),
    '+': ("00000","00100","00100","11111","00100","00100","00000"),
    '=': ("00000","00000","11111","00000","11111","00000","00000"),
}

pix = bytearray(W * H * 3)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        pix[i], pix[i + 1], pix[i + 2] = color


def rect(x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, color)


def draw_text(x, y, text, scale, color):
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[' '])
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            set_px(cx + col * scale + dx, y + row * scale + dy, color)
        cx += 6 * scale
    return cx


def text_w(text, scale):
    return len(text) * 6 * scale


def wrap(text, max_chars):
    words = text.split(' ')
    lines, cur = [], ''
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > max_chars:
            lines.append(cur)
            cur = wd
        elif cur:
            cur = cur + ' ' + wd
        else:
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def panel(x, y, w, h, color, kicker, headline, body):
    rect(x, y, w, h, WHITE)
    rect(x, y, w, 3, color)
    rect(x, y, w, h, color) if False else None
    # border
    for xx in range(x, x + w):
        set_px(xx, y, color)
        set_px(xx, y + h - 1, color)
    for yy in range(y, y + h):
        set_px(x, yy, color)
        set_px(x + w - 1, yy, color)
    rect(x + 1, y + 1, w - 2, 34, color)
    draw_text(x + 14, y + 8, kicker, 2, WHITE)
    lines = wrap(headline, (w - 28) // 18)
    yy = y + 48
    for ln in lines[:2]:
        draw_text(x + 14, yy, ln, 3, BLACK)
        yy += 24
    blines = wrap(body, (w - 28) // 12)
    yy += 6
    for ln in blines[:4]:
        draw_text(x + 14, yy, ln, 2, GREY)
        yy += 16
    # Simple icon at the bottom of the panel, drawn from rectangles.
    ix, iy = x + 14, y + h - 62
    if kicker == "HORMUZ":
        rect(ix, iy + 22, 120, 18, color)
        rect(ix + 20, iy, 60, 22, color)
        rect(ix + 30, iy - 14, 8, 14, color)
    elif kicker == "UKRAINE":
        rect(ix + 50, iy, 16, 56, color)
        rect(ix, iy + 20, 116, 16, color)
        rect(ix + 18, iy + 8, 80, 40, (255, 200, 0))
    elif kicker == "CLIMATE":
        rect(ix + 20, iy + 6, 76, 44, (255, 200, 0))
        rect(ix, iy + 34, 116, 22, color)
    elif kicker == "SPACE":
        rect(ix + 44, iy, 28, 56, color)
        rect(ix + 20, iy + 20, 76, 20, color)
        rect(ix + 50, iy - 10, 16, 12, RED)
    elif kicker == "TECH":
        rect(ix + 28, iy + 6, 60, 44, color)
        rect(ix + 44, iy + 20, 28, 16, WHITE)
        rect(ix, iy + 20, 28, 8, color)
        rect(ix + 88, iy + 20, 28, 8, color)
    elif kicker == "GAMES":
        rect(ix, iy + 10, 116, 36, color)
        rect(ix + 16, iy + 20, 24, 16, WHITE)
        rect(ix + 76, iy + 18, 14, 14, WHITE)
        rect(ix + 94, iy + 30, 14, 14, WHITE)


def chunk(data, typ):
    c = struct.pack('>I', len(data)) + typ + data
    c += struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)
    return c


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += pix[y * W * 3:(y + 1) * W * 3]
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0), b'IHDR')
    png += chunk(zlib.compress(bytes(raw), 9), b'IDAT')
    png += chunk(b'', b'IEND')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


def main():
    rect(0, 0, W, H, WHITE)
    # Masthead
    rect(0, 0, W, 148, NAVY)
    title = "25 NOVEMBER 2026"
    draw_text((W - text_w(title, 4)) // 2, 22, title, 4, WHITE)
    sub = "WORLD NEWS IN ONE IMAGE"
    draw_text((W - text_w(sub, 3)) // 2, 66, sub, 3, (200, 220, 255))
    day = "WEDNESDAY - THE DAY IN SIX STORIES"
    draw_text((W - text_w(day, 2)) // 2, 108, day, 2, (200, 220, 255))
    rect(0, 148, W, 4, RED)

    stories = [
        (TEAL, "HORMUZ", "TWO TANKERS HIT BY MINES",
         "OIL TANKERS STRUCK BY MINES IN THE STRAIT OF HORMUZ"),
        (RED, "UKRAINE", "STRIKES HIT KYIV AND ODESA",
         "RUSSIAN OVERNIGHT STRIKES HIT KYIV AND ODESA"),
        (GREEN, "CLIMATE", "COP31 TALKS COLLAPSE",
         "CLIMATE TALKS COLLAPSE IN ANTALYA"),
        (PURPLE, "SPACE", "PAKISTANS FIRST ASTRONAUT",
         "CHINA FLIES PAKISTANS FIRST ASTRONAUT INTO ORBIT"),
        (NAVY, "TECH", "HUAWEI FOUND GUILTY",
         "US JURY FINDS HUAWEI GUILTY OF TRADE SECRET THEFT AND BANK FRAUD"),
        (ORANGE, "GAMES", "GTA VI MAKES $3.79BN",
         "BIGGEST ENTERTAINMENT LAUNCH EVER AT $3.79BN"),
    ]
    pw, ph, gx, gy = 476, 232, 16, 168
    for i, (color, kicker, headline, body) in enumerate(stories):
        x = 24 + (i % 2) * (pw + gx)
        y = gy + (i // 2) * (ph + 14)
        panel(x, y, pw, ph, color, kicker, headline, body)

    # Footer strip
    rect(24, 912, 976, 88, LIGHT)
    rect(24, 912, 976, 3, NAVY)
    draw_text(40, 926, "ALSO TODAY:", 2, NAVY)
    f1 = "TRUMP AWARDS GIULIANI THE MEDAL OF FREEDOM"
    f2 = "ISRAELI STRIKE KILLS A HAMAS SECURITY CHIEF IN GAZA"
    draw_text(40, 950, f1, 2, BLACK)
    draw_text(40, 972, f2, 2, BLACK)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(path)
    # readable by every user, as the grader collects outputs as another user
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    print("wrote %s %d bytes" % (path, size))


if __name__ == "__main__":
    main()
