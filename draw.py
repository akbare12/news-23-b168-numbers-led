#!/usr/bin/env python3
"""draw.py — news-23 b168 numbers-led: THE WORLD TODAY, Monday 23 November 2026.
Renders entry.png 1024x1024 from PIL primitives. No external data."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(text, fnt, max_w, draw):
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


def chip(d, x, y, label, fill):
    f = font(FB, 9)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x, y, x + tw + 12, y + 15], radius=3, fill=fill)
    d.text((x + 6, y + 2), label, font=f, fill="white")
    return tw + 12


# palette
PAPER = "#fdfdf6"
INK = "#111111"
NAVY = "#0b1e3a"
NAVY2 = "#12294d"
TEAL = "#0f3a3a"
DARK = "#1a1a2e"
RED = "#b91c1c"
GREEN = "#166534"
GOLD = "#d4a017"
ORANGE = "#f97316"
GREY = "#5b6470"
LIGHT = "#dbe4ee"
RULE = "#9fb0c3"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- NUMBER GRID (top, navy, 5x2) ----------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"), ("11,762", "EBOLA CASES - DRC"),
    ("10T won", "SEOUL RESCUE FUND"), ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL - METS"), ("165", "MISSILES / WEEK"),
    ("12,000", "CLEARED MANCHESTER"), ("264 kg", "EXPLOSIVES LEBANON"),
    ("$107.3B", "ANTHROPIC IPO"),
]
cw = W // 5
for i, (val, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x0, y0 = col * cw, row * 64
    d.rectangle([x0, y0, x0 + cw - 1, y0 + 63], fill=NAVY if row == 0 else NAVY2)
    if col:
        d.line([x0, y0 + 8, x0, y0 + 56], fill="#2a4368", width=1)
    fv = font(FB, 25)
    fl = font(FR, 11)
    tw = d.textlength(val, font=fv)
    d.text((x0 + (cw - tw) / 2, y0 + 6), val, font=fv, fill="white")
    tw2 = d.textlength(lab, font=fl)
    d.text((x0 + (cw - tw2) / 2, y0 + 38), lab, font=fl, fill="#c7d3e4")

# ---------- MASTHEAD ----------
ft = font(FB, 40)
t = "THE WORLD TODAY"
d.text(((W - d.textlength(t, font=ft)) / 2, 134), t, font=ft, fill=INK)
fd = font(FB, 13)
dt = "MONDAY 23 NOVEMBER 2026"
d.text(((W - d.textlength(dt, font=fd)) / 2, 180), dt, font=fd, fill=RED)
# region bar
d.rectangle([0, 198, W, 218], fill=NAVY)
frb = font(FB, 12)
rb = "ASIA-PACIFIC 7  -  AMERICAS 8  -  MIDDLE EAST 6  -  EUROPE 5  -  AFRICA 3  -  WORLD 2   |   31 STORIES"
d.text(((W - d.textlength(rb, font=frb)) / 2, 203), rb, font=frb, fill="white")

# ---------- HEROES ----------
HX = [8, 352, 696]
HW = 320
HY = 224
SH = 146  # scene height


def hero_text(x, headline, body, source):
    fh = font(FB, 14)
    lines = wrap(headline, fh, HW, d)[:2]
    y = HY + SH + 6
    for ln in lines:
        d.text((x, y), ln, font=fh, fill=INK)
        y += 18
    fb = font(FR, 11)
    blines = wrap(body, fb, HW, d)[:2]
    y = HY + SH + 44
    for ln in blines:
        d.text((x, y), ln, font=fb, fill="#333333")
        y += 14
    fs = font(FB, 10)
    d.text((x, HY + SH + 74), source, font=fs, fill=GREY)
    chip(d, x + 78, HY + SH + 72, "REPORTED", GREEN)


# --- hero 1: Kospi ---
x = HX[0]
d.rectangle([x, HY, x + HW, HY + SH], fill=NAVY)
# buildings along bottom
import random
random.seed(1681)
bx = x + 8
while bx < x + HW - 20:
    bw = random.randint(18, 30)
    bh = random.randint(30, 48)
    d.rectangle([bx, HY + SH - bh, bx + bw, HY + SH], fill="#16294d",
                outline="#2a4368")
    for wy in range(HY + SH - bh + 5, HY + SH - 4, 9):
        for wx in range(bx + 4, bx + bw - 3, 8):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill="#ffd166")
    bx += bw + 4
fbig = font(FB, 34)
d.text((x + 10, HY + 8), "-3.3%", font=fbig, fill="white")
fsm = font(FB, 12)
d.text((x + 12, HY + 50), "KOSPI 4,708.54", font=fsm, fill="#ffd166")
# descending chart line, starts right of text and below it
pts = [(x + 175, HY + 82), (x + 210, HY + 92), (x + 245, HY + 88),
       (x + 275, HY + 108), (x + 305, HY + 122)]
d.line(pts, fill=ORANGE, width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=ORANGE)
hero_text(x, "AI ROUT HITS ASIA",
          "Kospi sheds 161 pts intraday -5.8%; Samsung -3.1%, SK Hynix -2.5%.",
          "REUTERS")

# --- hero 2: Guterres ---
x = HX[1]
d.rectangle([x, HY, x + HW, HY + SH], fill=TEAL)
fg = font(FB, 16)
d.text((x + 12, HY + 12), "150 DELEGATES", font=fg, fill=GOLD)
fw = font(FB, 13)
d.text((x + 12, HY + 38), "BRIDGETOWN", font=fw, fill="white")
d.text((x + 12, HY + 58), "BARBADOS", font=fw, fill="white")
# globe, right side
cx, cy, r = x + 248, HY + 92, 42
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline="#7fd1d1", width=2)
d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline="#7fd1d1", width=1)
d.line([cx - r, cy, cx + r, cy], fill="#7fd1d1", width=1)
d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill="#7fd1d1", width=1)
# small flags, top-right corner (clear of text, inside scene edge)
for i, c in enumerate(["#1e40af", "#dc2626", "#16a34a"]):
    fx = x + 284 + i * 11
    d.rectangle([fx, HY + 8, fx + 10, HY + 16], fill=c, outline="white")
hero_text(x, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
          "Bridgetown summit backs a risk framework; blueprint, not treaty.",
          "AP")

# --- hero 3: Power Index ---
x = HX[2]
d.rectangle([x, HY, x + HW, HY + SH], fill=DARK)
ft2 = font(FB, 11)
d.text((x + 10, HY + 8), "ASIA POWER INDEX 2026", font=ft2, fill="#9aa7bd")
bars = [("US", 78.9, "#3b82f6"), ("CHINA", 73.6, "#ef4444"), ("INDIA", 40.5, GOLD)]
by = HY + 30
for name, val, col in bars:
    fl2 = font(FB, 11)
    d.text((x + 10, by), name, font=fl2, fill="white")
    bw = int(val / 78.9 * 210)
    d.rectangle([x + 78, by + 2, x + 78 + bw, by + 14], fill=col)
    d.text((x + 82 + bw, by), f"{val}", font=fl2, fill="white")
    by += 30
d.text((x + 10, HY + 124), "US DIPLOMATIC INFLUENCE -6 TO 76.7",
       font=font(FR, 11), fill="#c7d3e4")
hero_text(x, "US LEAD OVER CHINA AT RECORD LOW",
          "Gap 5.3, narrowest since 2018; India third at 40.5.",
          "REUTERS")

# ---------- CARDS (5x2) ----------
cards = [
    ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker over sales.", "REUTERS", "REPORTED"),
    ("FBI PROBES NCIC POLICE-DATABASE HACK", "Federal system breached; scope under review.", "AP", "REPORTED"),
    ("TRUMP: IRAN STRIKES MAY RESUME IN NEW YEAR", "President warns Tehran as talks stall.", "REUTERS", "REPORTED"),
    ("NASDAQ FUTURES +3% HOLIDAY WEEK", "Tech leads into Thanksgiving trading.", "BLOOMBERG", "REPORTED"),
    ("SKUBAL $450M METS", "Two-time Cy Young winner signs nine-year deal.", "ESPN", "REPORTED"),
    ("TOM JACKSON DIES AT 75", "Broncos great and broadcaster remembered.", "AP", "REPORTED"),
    ("STATES SUE SPACEX OVER AI SAFETY CLAIMS", "Attorneys general challenge safety pledges.", "REUTERS", "REPORTED"),
    ("ANTHROPIC IPO $107.3B", "Raised at $83/share 19 Nov; debut close $97.17.", "BLOOMBERG", "REPORTED"),
    ("POLAND: 3 RUSSIAN KH-101 MISSILES CROSSED AIRSPACE", "Warsaw cites airspace breach.", "AP", "CLAIM"),
    ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "Moscow developing orbital weapon, US says.", "REUTERS", "CLAIM"),
]
CY0 = 468
CHH = 84
for i, (hl, body, src, kind) in enumerate(cards):
    col, row = i % 5, i // 5
    cx0 = 8 + col * 203
    cy0 = CY0 + row * 90
    d.rectangle([cx0, cy0, cx0 + 195, cy0 + CHH], outline="#c9c9bd", width=1, fill="white")
    fh = font(FB, 12)
    hl_lines = wrap(hl, fh, 183, d)[:2]
    y = cy0 + 5
    for ln in hl_lines:
        d.text((cx0 + 6, y), ln, font=fh, fill=INK)
        y += 15
    fb = font(FR, 10)
    bl = wrap(body, fb, 183, d)[:2]
    y = cy0 + 37
    for ln in bl:
        d.text((cx0 + 6, y), ln, font=fb, fill="#333333")
        y += 12
    fs = font(FB, 9)
    d.text((cx0 + 6, cy0 + 68), src, font=fs, fill=GREY)
    chip(d, cx0 + 118, cy0 + 66, kind, GREEN if kind == "REPORTED" else RED)

# ---------- MAP + ALSO ----------
MY0 = 650
# map panel
d.rectangle([8, MY0, 500, 868], outline="#c9c9bd", width=1, fill="#f4f7fa")
fm = font(FB, 11)
d.text((16, MY0 + 4), "THE WORLD IN 13 PINS", font=fm, fill=INK)
# blobs
d.ellipse([17, 662, 193, 818], fill=LIGHT, outline=RULE)          # Americas
d.ellipse([215, 657, 485, 773], fill=LIGHT, outline=RULE)         # Eurasia
d.ellipse([275, 770, 385, 854], fill=LIGHT, outline=RULE)         # Africa
pins = [
    (458, 700), (150, 795), (90, 705), (318, 692), (295, 672),
    (272, 682), (352, 672), (382, 718), (392, 742), (408, 720),
    (432, 738), (345, 800), (318, 836),
]
fpin = font(FB, 10)
for n, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white", width=1)
    tw = d.textlength(str(n), font=fpin)
    d.text((px - tw / 2, py - 7), str(n), font=fpin, fill="white")
fl2 = font(FR, 9)
leg1 = "1 SEOUL - 2 BRIDGETOWN - 3 WASHINGTON - 4 PARIS - 5 LONDON - 6 MANCHESTER - 7 WARSAW"
leg2 = "8 ANTALYA - 9 GAZA - 10 BEIRUT - 11 BAHRAIN - 12 KHARTOUM - 13 KINSHASA"
d.text(((508 - d.textlength(leg1, font=fl2)) / 2 + 4, 844), leg1, font=fl2, fill=GREY)
d.text(((508 - d.textlength(leg2, font=fl2)) / 2 + 4, 855), leg2, font=fl2, fill=GREY)

# ALSO panel
d.text((516, MY0 + 4), "ALSO ON MONDAY", font=fm, fill=INK)
also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared in scare",
    "Zelenskyy: 165 Russian missiles/week",
    "COP31: day after Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN demands port probe [CLAIM]",
    "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3%",
    "China eases margin rules to 80%",
    "Seoul readies 10T-won stabilisation fund",
]
fa = font(FR, 10)
for i, item in enumerate(also):
    col, row = i % 2, i // 2
    ax = 516 + col * 252
    ay = MY0 + 26 + row * 21
    d.text((ax, ay), "- " + item, font=fa, fill=INK)

# ---------- DATE CHECK ----------
d.rectangle([8, 876, 1016, 968], outline=RED, width=2)
fdc = font(FB, 12)
d.text((16, 880), "DATE CHECK - LEFT OUT (NOT 23 NOV)", font=fdc, fill=RED)
leftout = [
    "Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
    "El Chapo captured (22 Nov)", "EU-Indonesia pact (21 Nov)",
    "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)",
]
fdo = font(FR, 10)
for i, item in enumerate(leftout):
    col, row = i % 3, i // 3
    d.text((16 + col * 336, 904 + row * 16), "- " + item, font=fdo, fill=INK)
d.text((16, 936), "NOT YET:", font=font(FB, 10), fill=RED)
notyet = [
    "Dymer search continues (14 missing)", "4 House races uncalled",
    "COP32 venue not set", "WHO evacuating trapped Ebola staff",
]
for i, item in enumerate(notyet):
    d.text((16 + i * 252, 950), "- " + item, font=fdo, fill=INK)

# ---------- FOOTER ----------
ff = font(FR, 10)
f1 = "SOURCES: REUTERS - AP - BLOOMBERG - ESPN - WIRE SERVICES"
d.text(((W - d.textlength(f1, font=ff)) / 2, 976), f1, font=ff, fill=GREY)
f2 = "REPORTED = confirmed by wires  -  CLAIM = one side's claim  -  All stories dated Monday 23 November 2026"
d.text(((W - d.textlength(f2, font=ff)) / 2, 992), f2, font=ff, fill=GREY)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
