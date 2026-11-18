#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news summary image (1024x1024 PNG).

The final image is baked into entry.png; main.py only copies it so the
graded program is deterministic and needs no network.
All text is rendered here with PIL + DejaVu (no AI-generated text).
All illustrations are flat vector shapes drawn with PIL primitives.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

W = H = 1024

# Palette
NAVY = (14, 38, 66)
NAVY_DARK = (9, 28, 50)
GOLD = (216, 164, 65)
PAPER = (244, 241, 234)
INK = (24, 24, 24)
BODY = (58, 58, 58)
MUTED = (110, 108, 100)
CARD = (255, 255, 255)
BORDER = (214, 208, 194)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- scenes
# Each scene draws into a 160x250 portrait tile (flat vector style).

def scene_bridge(d):
    # sky, sea, bridge with a collapsed span + smoke
    d.rectangle([0, 0, 160, 150], fill=(178, 214, 235))
    d.ellipse([112, 18, 146, 52], fill=(250, 244, 214))  # sun
    d.rectangle([0, 150, 160, 250], fill=(46, 110, 158))  # sea
    d.rectangle([0, 150, 160, 156], fill=(120, 180, 210))
    for x in (20, 70, 120):
        d.line([x, 158, x + 24, 158], fill=(200, 225, 240), width=3)
    # bridge deck (left part intact, right part collapsed)
    d.rectangle([0, 118, 78, 128], fill=(90, 90, 96))
    d.polygon([(78, 118), (118, 168), (112, 176), (74, 126)], fill=(90, 90, 96))
    d.rectangle([118, 168, 160, 178], fill=(110, 110, 116))
    # towers
    d.rectangle([28, 62, 36, 120], fill=(70, 70, 78))
    d.rectangle([28, 56, 60, 64], fill=(70, 70, 78))
    d.line([32, 64, 10, 118], fill=(200, 200, 205), width=2)
    d.line([32, 64, 54, 118], fill=(200, 200, 205), width=2)
    # smoke over the gap
    for cx, cy, r in ((92, 96, 16), (104, 80, 20), (90, 62, 14)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 122))
    # splash
    d.ellipse([96, 176, 136, 196], fill=(220, 235, 245))


def scene_tanker(d):
    # dusk sea, tanker on fire
    d.rectangle([0, 0, 160, 250], fill=(232, 122, 48))
    d.rectangle([0, 0, 160, 60], fill=(248, 178, 92))
    d.ellipse([18, 14, 52, 48], fill=(255, 236, 190))
    d.rectangle([0, 150, 160, 250], fill=(28, 68, 110))
    for x in (8, 60, 110):
        d.line([x, 170, x + 30, 170], fill=(120, 170, 210), width=3)
        d.line([x + 14, 210, x + 44, 210], fill=(90, 140, 185), width=3)
    # tanker hull
    d.polygon([(14, 148), (146, 148), (134, 176), (26, 176)], fill=(30, 30, 34))
    d.rectangle([14, 142, 146, 150], fill=(120, 30, 28))
    # containers
    for i, c in enumerate(((200, 60, 40), (40, 120, 180), (60, 160, 90))):
        d.rectangle([24 + i * 34, 118, 52 + i * 34, 142], fill=c)
    d.rectangle([128, 104, 140, 142], fill=(220, 220, 220))  # funnel
    # flames
    d.polygon([(48, 118), (60, 78), (72, 118)], fill=(255, 140, 0))
    d.polygon([(66, 118), (80, 66), (94, 118)], fill=(255, 200, 0))
    d.polygon([(86, 118), (96, 88), (108, 118)], fill=(255, 120, 0))
    # smoke
    for cx, cy, r in ((74, 52, 16), (88, 36, 19), (70, 22, 12)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 74))


def scene_summit(d):
    # three flags on poles: USA, China, Russia + globe
    d.rectangle([0, 0, 160, 250], fill=(206, 226, 240))
    d.ellipse([0, 196, 160, 250], fill=(120, 170, 110))  # ground hint
    # globe: blue sphere with green landmasses
    d.ellipse([56, 164, 104, 212], fill=(52, 110, 170))
    d.ellipse([62, 172, 78, 188], fill=(86, 150, 96))
    d.ellipse([82, 190, 98, 204], fill=(86, 150, 96))
    d.ellipse([86, 170, 94, 178], fill=(86, 150, 96))
    d.arc([56, 164, 104, 212], 200, 340, fill=(255, 255, 255), width=3)
    d.arc([56, 164, 104, 212], 0, 360, fill=(30, 80, 130), width=3)
    # flag poles
    for x in (22, 72, 122):
        d.rectangle([x - 2, 30, x + 2, 190], fill=(90, 80, 70))
        d.ellipse([x - 5, 24, x + 5, 34], fill=(216, 164, 65))
    # US flag
    for i in range(7):
        d.rectangle([24, 36 + i * 8, 62, 36 + i * 8 + 4],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([24, 36, 44, 64], fill=(30, 60, 120))
    # China flag
    d.rectangle([74, 36, 112, 92], fill=(222, 41, 16))
    for sx, sy in ((80, 42), (90, 44), (96, 50), (90, 56), (80, 52)):
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 222, 0))
    # Russia flag
    d.rectangle([124, 36, 158, 54], fill=(255, 255, 255))
    d.rectangle([124, 54, 158, 72], fill=(0, 57, 166))
    d.rectangle([124, 72, 158, 90], fill=(213, 0, 50))


def scene_bank(d):
    # bank building + red warning triangle
    d.rectangle([0, 0, 160, 250], fill=(228, 230, 233))
    # building
    d.rectangle([18, 96, 142, 200], fill=(250, 250, 248))
    d.polygon([(10, 96), (80, 58), (150, 96)], fill=(190, 192, 196))
    d.ellipse([72, 68, 88, 84], fill=(216, 164, 65))
    for x in (30, 58, 86, 114):
        d.rectangle([x, 104, x + 12, 178], fill=(160, 162, 166))
    d.rectangle([14, 200, 146, 208], fill=(150, 152, 156))
    d.rectangle([10, 208, 150, 216], fill=(140, 142, 146))
    # warning triangle
    d.polygon([(80, 118), (52, 168), (108, 168)], fill=(205, 40, 30))
    d.rectangle([77, 132, 83, 154], fill=(255, 255, 255))
    d.ellipse([77, 158, 83, 164], fill=(255, 255, 255))


def scene_chip(d):
    # green AI chip with circuit traces
    d.rectangle([0, 0, 160, 250], fill=(16, 46, 36))
    for x0, y0, x1, y1 in ((18, 60, 60, 60), (100, 60, 142, 60),
                           (18, 190, 60, 190), (100, 190, 142, 190),
                           (60, 18, 60, 60), (100, 18, 100, 60),
                           (60, 190, 60, 232), (100, 190, 100, 232)):
        d.line([x0, y0, x1, y1], fill=(216, 164, 65), width=3)
    for cx, cy in ((18, 60), (142, 60), (18, 190), (142, 190),
                   (60, 18), (100, 18), (60, 232), (100, 232)):
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(216, 164, 65))
    # chip body
    d.rectangle([44, 74, 116, 176], fill=(118, 185, 0))
    d.rectangle([44, 74, 116, 176], outline=(60, 110, 0), width=4)
    # pins
    for i in range(5):
        d.rectangle([50 + i * 13, 66, 58 + i * 13, 74], fill=(200, 200, 200))
        d.rectangle([50 + i * 13, 176, 58 + i * 13, 184], fill=(200, 200, 200))
        d.rectangle([36, 82 + i * 13, 44, 90 + i * 13], fill=(200, 200, 200))
        d.rectangle([116, 82 + i * 13, 124, 90 + i * 13], fill=(200, 200, 200))
    # core
    d.rectangle([64, 100, 96, 150], fill=(30, 70, 10))
    d.rectangle([70, 108, 90, 126], fill=(118, 185, 0))


def scene_rocket(d):
    # night sky, rocket with flame + explosion burst
    d.rectangle([0, 0, 160, 250], fill=(18, 32, 64))
    for x, y in ((20, 30), (140, 50), (120, 110), (30, 130), (150, 180), (60, 210)):
        d.ellipse([x, y, x + 4, y + 4], fill=(255, 255, 255))
    d.ellipse([100, 20, 146, 66], fill=(240, 240, 235))  # moon
    # explosion burst: jagged star + smoke (reads as a blast, not a sun)
    import math
    cx, cy = 118, 78
    pts = []
    for i in range(16):
        r = 46 if i % 2 == 0 else 24
        a = math.radians(i * 22.5)
        pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
    d.polygon(pts, fill=(255, 170, 0))
    d.ellipse([100, 60, 136, 96], fill=(255, 120, 0))
    d.ellipse([108, 68, 128, 88], fill=(255, 220, 80))
    for sx, sy, r in ((92, 44, 12), (140, 52, 10), (146, 96, 12)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(110, 110, 116))
    # rocket body (tilted, falling)
    d.polygon([(52, 150), (66, 128), (80, 150), (72, 196), (60, 196)],
              fill=(235, 235, 230))
    d.polygon([(66, 128), (58, 140), (74, 140)], fill=(205, 40, 30))
    d.polygon([(52, 150), (44, 168), (54, 162)], fill=(205, 40, 30))
    d.polygon([(80, 150), (88, 168), (78, 162)], fill=(205, 40, 30))
    d.ellipse([60, 158, 72, 170], fill=(30, 60, 120))
    # flame
    d.polygon([(58, 196), (66, 228), (74, 196)], fill=(255, 140, 0))
    d.polygon([(61, 196), (66, 216), (71, 196)], fill=(255, 220, 80))
    # debris dots
    for x, y in ((40, 120), (100, 130), (130, 140), (30, 190)):
        d.ellipse([x, y, x + 5, y + 5], fill=(200, 200, 200))


SCENES = {
    "bridge": scene_bridge,
    "tanker": scene_tanker,
    "summit": scene_summit,
    "bank": scene_bank,
    "chip": scene_chip,
    "rocket": scene_rocket,
}

# ---------------------------------------------------------------- stories
STORIES = [
    dict(tag="UKRAINE · WAR", color=(178, 34, 52), scene="bridge",
         head="KERCH BRIDGE STRUCK AGAIN",
         body="Ukraine hits the Kerch bridge to Crimea; a road span "
              "collapses, the second strike in under a day. Russia "
              "hits a river crossing in Kyiv."),
    dict(tag="MIDDLE EAST · ENERGY", color=(150, 80, 10), scene="tanker",
         head="TANKERS BURN NEAR HORMUZ",
         body="Tankers strike mines near the Strait of Hormuz and catch "
              "fire, Iran's Revolutionary Guard says. A third US carrier "
              "arrives; Bahrain intercepts an Iranian air attack."),
    dict(tag="ASIA · DIPLOMACY", color=(30, 90, 150), scene="summit",
         head="TRUMP LANDS IN MANILA",
         body="Trump arrives for the ASEAN summit as China confirms a "
              "first Xi\u2013Trump\u2013Putin meeting in Shenzhen "
              "on Thursday."),
    dict(tag="FINANCE · USA", color=(20, 90, 60), scene="bank",
         head="JPMORGAN BLAMES A BUG",
         body="Monday's banking outage was a software bug, not a "
              "cyberattack, JPMorgan says. Online banking and Zelle "
              "ran slow."),
    dict(tag="TECH · AI", color=(60, 110, 0), scene="chip",
         head="NVIDIA REPORTS AFTER HUANG'S EXIT",
         body="Nvidia reports quarterly earnings for the first time "
              "since Jensen Huang left the company."),
    dict(tag="SPACE · USA", color=(60, 40, 120), scene="rocket",
         head="VULCAN ROCKET FAILS IN FLIGHT",
         body="ULA's Vulcan rocket fails in flight and 40 Amazon Leo "
              "internet satellites are lost."),
]


def draw_panel(img, x, y, w, h, story):
    d = ImageDraw.Draw(img)
    # card
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    # accent bar on top
    d.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=story["color"])
    d.rectangle([x, y + 4, x + w, y + 8], fill=story["color"])
    # illustration tile
    tile = Image.new("RGB", (160, 250), (255, 255, 255))
    td = ImageDraw.Draw(tile)
    SCENES[story["scene"]](td)
    mask = Image.new("L", (160, 250), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, 160, 250], radius=8, fill=255)
    img.paste(tile, (x + 12, y + 16), mask)
    # text column
    tx = x + 184
    tw = x + w - 14 - tx
    f_tag = font(F_BOLD, 15)
    f_head = font(F_BOLD, 25)
    f_body = font(F_REG, 18)
    cy = y + 20
    d.text((tx, cy), story["tag"], font=f_tag, fill=story["color"])
    cy += 26
    for line in wrap(d, story["head"], f_head, tw):
        d.text((tx, cy), line, font=f_head, fill=INK)
        cy += 30
    cy += 4
    for line in wrap(d, story["body"], f_body, tw):
        d.text((tx, cy), line, font=f_body, fill=BODY)
        cy += 24


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 122], fill=GOLD)
    f_title = font(F_BOLD, 52)
    title = "TUESDAY 17 NOVEMBER 2026"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 16), title, font=f_title, fill=(255, 255, 255))
    f_sub = font(F_BOLD, 20)
    sub = "T H E   W O R L D   I N   O N E   D A Y"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 78), sub, font=f_sub, fill=GOLD)
    # grid 2 x 3
    pw, ph, gap = 490, 274, 12
    gx, gy = 16, 134
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_panel(img, gx + col * (pw + gap), gy + row * (ph + gap),
                   pw, ph, story)
    # footer
    f_foot = font(F_REG, 16)
    foot = "Sources: BBC \u00b7 AP \u00b7 Reuters \u00b7 Al Jazeera  \u2014  17 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 988), foot, font=f_foot, fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes", img.size)
