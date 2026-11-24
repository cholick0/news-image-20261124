#!/usr/bin/env python3
"""Render the World News front page for Tuesday 24 November 2026 (1024x1024 PNG).

Stories verified from news dated 24 November 2026:
 1. Nvidia reinstates Jensen Huang as CEO; shares surge 31%, Nasdaq +~7%
    (board decision Monday, market rally reported 24 Nov in Asia)
 2. World Chess Championship opens in Geneva: Gukesh defends vs Sindarov
 3. Oxfam/CEOBS report released 24 Nov: Gaza's air, soil and water poisoned
 4. Taliban orders women's names off documents in Balkh (24 Nov report)
 5. India's flash factory PMI rises to 56.3 (released 24 Nov)
 6. Rescuers still search for ~30 missing after Indonesia factory fire
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 245)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GRAY = (85, 85, 85)
GREEN = (21, 128, 61)
LIGHT = (238, 234, 224)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
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

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36  # margin
R = W - M

# ---- Masthead ----
d.line([(M, 26), (R, 26)], fill=INK, width=4)
f_mast = font(SERIF_B, 78)
d.text((W // 2, 34), "WORLD NEWS", font=f_mast, fill=INK, anchor="ma")
f_date = font(SANS_B, 27)
d.text((W // 2, 122), "T U E S D A Y ,  2 4  N O V E M B E R  2 0 2 6",
       font=f_date, fill=RED, anchor="ma")
d.line([(M, 158), (R, 158)], fill=INK, width=3)

# ---- Hero: Nvidia ----
f_kick = font(SANS_B, 20)
f_hero = font(SERIF_B, 45)
f_sum = font(SANS, 23)
d.text((M, 172), "BUSINESS  ·  MARKETS", font=f_kick, fill=RED)
hero_head = ["Huang is back: Nvidia", "shares soar 31%"]
y = 200
for line in hero_head:
    d.text((M, y), line, font=f_hero, fill=INK)
    y += 52
hero_sum = ("Nvidia reinstated Jensen Huang as chief executive after President "
            "Trump pressed the board to bring him back. Shares jumped 31% "
            "and the Nasdaq rose nearly 7%.")
for line in wrap(d, hero_sum, f_sum, 640):
    d.text((M, y), line, font=f_sum, fill=INK)
    y += 30

# small chart box, right of hero text
cx0, cy0, cx1, cy1 = 700, 178, R, 372
d.rectangle([cx0, cy0, cx1, cy1], outline=INK, width=2)
pts = [(716, 348), (748, 330), (780, 336), (812, 300), (844, 306),
       (876, 262), (908, 268), (940, 214), (972, 196)]
d.line(pts, fill=GREEN, width=4)
d.ellipse([964, 188, 980, 204], fill=GREEN)
f_big = font(SANS_B, 34)
d.text(((cx0 + cx1) // 2, cy0 + 8), "+31%", font=f_big, fill=GREEN, anchor="ma")
d.text(((cx0 + cx1) // 2, cy0 + 52), "NVDA", font=font(SANS_B, 18), fill=GRAY, anchor="ma")

d.line([(M, 392), (R, 392)], fill=INK, width=2)

# ---- 2x2 grid: stories 2-5 ----
stories = [
    ("SPORT  ·  CHESS",
     "Chess crown on the line in Geneva",
     "The World Championship opens today: India's Gukesh defends his title "
     "against Uzbekistan's Sindarov in up to 14 games, first to 7.5 points."),
    ("MIDDLE EAST  ·  ENVIRONMENT",
     "Gaza's ground poisoned, report warns",
     "A new Oxfam report finds Israel's assault has left Gaza's air, soil "
     "and water laced with heavy metals, explosives residue and asbestos."),
    ("AFGHANISTAN  ·  RIGHTS",
     "Taliban erases women's names",
     "In Balkh, officials order women's names removed from documents, "
     "replaced with \u201cBibi\u201d \u2014 grandmother or older woman."),
    ("INDIA  ·  ECONOMY",
     "India's factories pick up pace",
     "Manufacturing strengthened in November: the HSBC flash PMI rose to "
     "56.3 from 56.2, with faster growth in output and new orders."),
]
f_sk = font(SANS_B, 17)
f_sh = font(SERIF_B, 27)
f_ss = font(SANS, 19)
col_w = 464
rows_y = [408, 560]
cols_x = [M, 524]
for i, (kick, head, summ) in enumerate(stories):
    x = cols_x[i % 2]
    y = rows_y[i // 2]
    d.text((x, y), kick, font=f_sk, fill=RED)
    y += 26
    for line in wrap(d, head, f_sh, col_w):
        d.text((x, y), line, font=f_sh, fill=INK)
        y += 31
    for line in wrap(d, summ, f_ss, col_w):
        d.text((x, y), line, font=f_ss, fill=(51, 51, 51))
        y += 23
d.line([(M, 716), (R, 716)], fill=INK, width=2)

# ---- Story 6, full width ----
d.text((M, 730), "INDONESIA  ·  RESCUE", font=f_sk, fill=RED)
d.text((M, 756), "Search goes on for 30 missing after factory fire",
       font=f_sh, fill=INK)
s6 = ("Rescuers keep combing the wreckage of the candy factory in Banten "
      "that killed 24 people, with about 30 still unaccounted for.")
y = 792
for line in wrap(d, s6, f_ss, R - M):
    d.text((M, y), line, font=f_ss, fill=(51, 51, 51))
    y += 23

# ---- Also Today band ----
by0, by1 = 850, 1000
d.rectangle([M, by0, R, by1], fill=NAVY)
d.text((M + 16, by0 + 10), "ALSO TODAY", font=font(SANS_B, 20), fill=(255, 255, 255))
also = [
    "India and China hold border talks in Arunachal Pradesh",
    "Chief Justice of India urges legal-aid work and AI rules in law courses",
    "Don Toliver's London show postponed after Manchester evacuation",
    "Ukraine claims it sank a Russian warship off the Libyan coast",
]
f_at = font(SANS, 18)
ax = [M + 16, 524]
ay = [by0 + 44, by0 + 96]
for i, item in enumerate(also):
    x = ax[i % 2]
    y = ay[i // 2]
    for line in wrap(d, "\u2022  " + item, f_at, 440):
        d.text((x, y), line, font=f_at, fill=(255, 255, 255))
        y += 23

img.save("/home/hatch/workspace/makefun/news-image-20261124/repo/entry.png")
print("saved", img.size)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/makefun/news-image-20261124/repo/entry.png"))
