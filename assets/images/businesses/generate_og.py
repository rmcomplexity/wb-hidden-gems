#!/usr/bin/env python3
"""Generate OG (Open Graph) social share images for WB Hidden Gems business directory."""

from PIL import Image, ImageDraw, ImageFont
import os
import math

FONT_BOLD    = "/home/xirdneh/.local/share/fonts/Sansation-Bold.ttf"
FONT_REGULAR = "/home/xirdneh/.local/share/fonts/Sansation-Regular.ttf"
FONT_DESC    = "/usr/share/fonts/gnu-free/FreeSans.otf"
OUT_DIR     = os.path.dirname(os.path.abspath(__file__))

W, H = 1200, 630

# Brand palette
WHITE      = (254, 254, 254)
OFF_WHITE  = (248, 246, 243)
CREAM      = (245, 242, 235)
CHARCOAL   = (45,  45,  45)
GRAY       = (107, 107, 107)
YELLOW_D   = (204, 128, 18)
YELLOW_L   = (238, 201, 147)
GREEN_D    = (32,  80,  12)
GREEN_L    = (170, 214, 151)
RED_D      = (138, 13,  26)
RED_L      = (235, 27,  48)
BLUE_D     = (8,   19,  122)
BLUE_L     = (21,  34,  168)

businesses = [
    {
        "slug":        "marias-bakery-og",
        "name":        "Maria's Bakery",
        "tagline":     "Artisan breads, pastries & custom cakes",
        "description": "Family-owned bakery in Wells Branch, TX\nFreshly baked every morning since 2018",
        "category":    "Food & Drink",
        "rating":      "4.9",
        "initials":    "MB",
        "accent":      GREEN_D,
        "accent_mid":  (40, 107, 18),
        "accent_light": GREEN_L,
        "badge":       "Community Favorite",
    },
    {
        "slug":        "bloom-glow-og",
        "name":        "Bloom & Glow Salon",
        "tagline":     "Hair color, balayage & facials",
        "description": "Boutique beauty salon in Wells Branch, TX\nWoman-owned · Appointments & walk-ins welcome",
        "category":    "Health & Beauty",
        "rating":      "4.8",
        "initials":    "BG",
        "accent":      RED_D,
        "accent_mid":  (163, 20, 38),
        "accent_light": (235, 119, 130),
        "badge":       "Woman-Owned",
    },
    {
        "slug":        "peak-auto-og",
        "name":        "Peak Auto Care",
        "tagline":     "Honest auto repair you can trust",
        "description": "ASE-certified mechanics in Wells Branch, TX\nFamily-owned since 2014 · No surprise charges",
        "category":    "Automotive",
        "rating":      "4.7",
        "initials":    "PA",
        "accent":      BLUE_D,
        "accent_mid":  (14, 28, 155),
        "accent_light": (100, 120, 220),
        "badge":       "ASE Certified",
    },
]


def rgba(color, alpha=255):
    return (*color, alpha)


def tint(color, factor=0.18):
    """Blend color toward white. factor=1.0 is full color, 0.0 is pure white."""
    return tuple(int(255 * (1 - factor) + c * factor) for c in color)


def draw_star(draw, cx, cy, r_outer, r_inner, fill):
    """Draw a 5-point star polygon."""
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)


def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + radius*2, y0 + radius*2], fill=fill)
    draw.ellipse([x1 - radius*2, y0, x1, y0 + radius*2], fill=fill)
    draw.ellipse([x0, y1 - radius*2, x0 + radius*2, y1], fill=fill)
    draw.ellipse([x1 - radius*2, y1 - radius*2, x1, y1], fill=fill)


def generate(biz):
    img  = Image.new("RGB", (W, H), color=biz["accent"])
    draw = ImageDraw.Draw(img, "RGBA")

    # ── Background decorative shapes ──────────────────────────────────────
    # Large muted circle top-right
    draw.ellipse(
        [W - 350, -150, W + 200, 400],
        fill=(*biz["accent_mid"], 180)
    )
    # Smaller circle bottom-left
    draw.ellipse(
        [-80, H - 250, 280, H + 80],
        fill=(*biz["accent_mid"], 140)
    )
    # Faint diagonal stripe
    draw.polygon(
        [(0, H*0.55), (W*0.45, 0), (W*0.55, 0), (0, H*0.7)],
        fill=(*biz["accent_mid"], 80)
    )

    # ── Right panel (light card area) ─────────────────────────────────────
    panel_x = 720
    draw_rounded_rect(draw, (panel_x, 40, W - 40, H - 40), 24, (*WHITE, 255))

    # ── Initials / logo circle ─────────────────────────────────────────────
    circle_cx, circle_cy = 370, 300
    r = 150
    draw.ellipse(
        [circle_cx - r, circle_cy - r, circle_cx + r, circle_cy + r],
        fill=(*WHITE, 30)
    )
    r2 = 120
    draw.ellipse(
        [circle_cx - r2, circle_cy - r2, circle_cx + r2, circle_cy + r2],
        fill=(*WHITE, 50)
    )

    try:
        font_initials = ImageFont.truetype(FONT_BOLD, 96)
    except Exception:
        font_initials = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), biz["initials"], font=font_initials)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        (circle_cx - tw // 2, circle_cy - th // 2 - 6),
        biz["initials"],
        font=font_initials,
        fill=WHITE
    )

    # ── WB Hidden Gems brand (left, above circle) ─────────────────────────
    try:
        font_brand = ImageFont.truetype(FONT_BOLD, 22)
    except Exception:
        font_brand = ImageFont.load_default()

    brand_y = 52
    draw.text((52, brand_y), "WB HIDDEN GEMS", font=font_brand, fill=(*YELLOW_L, 230))

    # separator dot
    draw.ellipse([52, brand_y + 34, 60, brand_y + 42], fill=(*WHITE, 120))

    try:
        font_sub_brand = ImageFont.truetype(FONT_REGULAR, 18)
    except Exception:
        font_sub_brand = ImageFont.load_default()
    draw.text((66, brand_y + 30), "Local Business Directory", font=font_sub_brand, fill=(*WHITE, 160))

    # ── Business name (right panel) ──────────────────────────────────────
    try:
        font_name = ImageFont.truetype(FONT_BOLD, 44)
    except Exception:
        font_name = ImageFont.load_default()

    name_x = panel_x + 36
    name_y = 90

    # word-wrap business name if too long
    words = biz["name"].split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0,0), test, font=font_name)
        if bbox[2] - bbox[0] > (W - panel_x - 80):
            lines.append(current)
            current = w
        else:
            current = test
    lines.append(current)

    for i, line in enumerate(lines):
        draw.text((name_x, name_y + i * 52), line, font=font_name, fill=CHARCOAL)

    name_bottom = name_y + len(lines) * 52

    # ── Tagline ────────────────────────────────────────────────────────────
    try:
        font_tagline = ImageFont.truetype(FONT_REGULAR, 22)
    except Exception:
        font_tagline = ImageFont.load_default()

    draw.text((name_x, name_bottom + 12), biz["tagline"], font=font_tagline, fill=GRAY)

    # ── Description lines ─────────────────────────────────────────────────
    try:
        font_desc = ImageFont.truetype(FONT_DESC, 18)
    except Exception:
        font_desc = ImageFont.load_default()

    desc_y = name_bottom + 52
    for line in biz["description"].split("\n"):
        draw.text((name_x, desc_y), line, font=font_desc, fill=GRAY)
        desc_y += 26

    # ── Divider ────────────────────────────────────────────────────────────
    div_y = desc_y + 20
    draw.line([(name_x, div_y), (W - 60, div_y)], fill=(*biz["accent_light"][:3], 100), width=2)

    # ── Category pill ─────────────────────────────────────────────────────
    try:
        font_pill = ImageFont.truetype(FONT_BOLD, 17)
    except Exception:
        font_pill = ImageFont.load_default()

    pad = 14
    pill_y = div_y + 22

    # Category
    cat_bbox = draw.textbbox((0, 0), biz["category"], font=font_pill)
    cat_w = cat_bbox[2] - cat_bbox[0]
    draw_rounded_rect(draw, (name_x, pill_y, name_x + cat_w + pad*2, pill_y + 32), 6, tint(biz["accent"]))
    draw.text((name_x + pad, pill_y + 7), biz["category"], font=font_pill, fill=biz["accent"])

    # ── Rating: 5 drawn stars + numeric score ─────────────────────────────
    rat_x = name_x + cat_w + pad*2 + 12
    star_y_center = pill_y + 16
    star_r = 8
    star_spacing = 19
    for i in range(5):
        draw_star(draw, rat_x + star_r + i * star_spacing, star_y_center, star_r, star_r * 0.42, YELLOW_D)

    rat_label = biz["rating"]
    try:
        font_rat_num = ImageFont.truetype(FONT_BOLD, 17)
    except Exception:
        font_rat_num = ImageFont.load_default()
    rat_num_bbox = draw.textbbox((0, 0), rat_label, font=font_rat_num)
    rat_num_w = rat_num_bbox[2] - rat_num_bbox[0]
    rat_num_x = rat_x + 5 * star_spacing + 8
    draw.text((rat_num_x, pill_y + 7), rat_label, font=font_rat_num, fill=YELLOW_D)

    # ── Badge pill (second row) ─────────────────────────────────────────────
    badge_y = pill_y + 44
    badge_bbox = draw.textbbox((0, 0), biz["badge"], font=font_pill)
    badge_w = badge_bbox[2] - badge_bbox[0]
    draw_rounded_rect(draw, (name_x, badge_y, name_x + badge_w + pad*2, badge_y + 32), 6, tint(RED_D))
    draw.text((name_x + pad, badge_y + 7), biz["badge"], font=font_pill, fill=RED_D)

    # ── Wells Branch TX label (bottom of right panel) ─────────────────────
    try:
        font_loc = ImageFont.truetype(FONT_REGULAR, 17)
    except Exception:
        font_loc = ImageFont.load_default()

    draw.text((name_x, H - 72), "Wells Branch, TX · 78728", font=font_loc, fill=GRAY)

    # ── URL watermark (bottom left of image) ─────────────────────────────
    try:
        font_url = ImageFont.truetype(FONT_REGULAR, 16)
    except Exception:
        font_url = ImageFont.load_default()

    draw.text((52, H - 52), "wbhiddengems.com/business-directory", font=font_url, fill=(*WHITE, 140))

    # ── Save ───────────────────────────────────────────────────────────────
    path = os.path.join(OUT_DIR, biz["slug"] + ".jpg")
    img.save(path, "JPEG", quality=92, optimize=True)
    print(f"  Created: {path}")


if __name__ == "__main__":
    print("Generating OG images…")
    for biz in businesses:
        generate(biz)
    print("Done.")
