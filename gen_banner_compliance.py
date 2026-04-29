"""
Codiste LinkedIn Banner Generator
Topic: AI Compliance Ethics & Governance
2400x1348 Codiste branded banner
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import os
import random

ASSETS = '/home/user/linkedin_post_creation/'
OUT_DIR = '/home/user/linkedin_post_creation/output/ai-compliance-ethics-governance/'
os.makedirs(OUT_DIR, exist_ok=True)

TITLE_LINE1 = "AI Compliance Is Scaling Fast:"
TITLE_LINE2 = "Your Ethics Framework Isn't"
SLUG = "ai-compliance-ethics-governance"

W, H = 2400, 1348


def generate_hero(width=1200, height=1348):
    """
    Governance architecture theme:
    Three concentric rings (fairness / transparency / privacy layers)
    around a central AI core, with audit-trail data streams and shield geometry.
    Deep navy + electric blue + muted gold palette.
    """
    random.seed(77)
    img = Image.new('RGB', (width, height), (4, 8, 28))
    draw = ImageDraw.Draw(img)

    # Background gradient dark navy → deep midnight
    for y in range(height):
        t = y / height
        r = int(4 + t * 8)
        g = int(8 + t * 12)
        b = int(28 + t * 22)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Subtle grid (governance structure motif)
    grid_col = (15, 30, 70)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=grid_col, width=1)
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=grid_col, width=1)

    cx, cy = width // 2, height // 2

    # ── Three governance rings ─────────────────────────────────────────
    # Outer ring — privacy/containment (deep indigo)
    for r_off in range(0, 3):
        draw.ellipse(
            [(cx - 340 + r_off, cy - 340 + r_off),
             (cx + 340 - r_off, cy + 340 - r_off)],
            outline=(60, 40, 160), width=1
        )
    # Middle ring — transparency (electric blue)
    for r_off in range(0, 4):
        draw.ellipse(
            [(cx - 240 + r_off, cy - 240 + r_off),
             (cx + 240 - r_off, cy + 240 - r_off)],
            outline=(0, 160, 255), width=2 if r_off == 0 else 1
        )
    # Inner ring — fairness/balance (muted gold)
    for r_off in range(0, 4):
        draw.ellipse(
            [(cx - 148 + r_off, cy - 148 + r_off),
             (cx + 148 - r_off, cy + 148 - r_off)],
            outline=(200, 160, 40), width=2 if r_off == 0 else 1
        )

    # ── Balance scale geometry inside fairness ring ────────────────────
    # Horizontal beam
    draw.line([(cx - 80, cy - 40), (cx + 80, cy - 40)], fill=(200, 160, 40), width=2)
    # Pivot
    draw.line([(cx, cy - 40), (cx, cy + 20)], fill=(200, 160, 40), width=2)
    # Left scale pan
    draw.arc([(cx - 80, cy - 30), (cx - 30, cy + 10)], 0, 180, fill=(200, 160, 40), width=2)
    # Right scale pan
    draw.arc([(cx + 30, cy - 30), (cx + 80, cy + 10)], 0, 180, fill=(200, 160, 40), width=2)

    # ── Hexagonal transparency lattice (middle ring zone) ─────────────
    hex_r = 18
    hex_positions = []
    for angle_deg in range(0, 360, 60):
        angle = math.radians(angle_deg)
        hx = cx + int(190 * math.cos(angle))
        hy = cy + int(190 * math.sin(angle))
        hex_positions.append((hx, hy))
        pts = []
        for ha in range(0, 360, 60):
            ra = math.radians(ha)
            pts.append((hx + int(hex_r * math.cos(ra)), hy + int(hex_r * math.sin(ra))))
        draw.polygon(pts, outline=(0, 130, 220), fill=(0, 30, 70))

    # Connect hexagons to center
    for hx, hy in hex_positions:
        draw.line([(cx, cy), (hx, hy)], fill=(0, 80, 160), width=1)

    # ── Privacy shield geometry (outer ring zone, four quadrants) ─────
    shield_positions = [
        (cx - 290, cy - 290),
        (cx + 290, cy - 290),
        (cx - 290, cy + 290),
        (cx + 290, cy + 290),
    ]
    for sx, sy in shield_positions:
        shield_pts = [
            (sx, sy - 28), (sx + 22, sy - 28),
            (sx + 22, sy + 8), (sx, sy + 28),
            (sx - 22, sy + 8), (sx - 22, sy - 28),
        ]
        draw.polygon(shield_pts, outline=(60, 40, 160), fill=(10, 8, 40))
        # Lock icon inside shield
        draw.ellipse([(sx - 8, sy - 16), (sx + 8, sy)], outline=(100, 80, 200), width=1)
        draw.rectangle([(sx - 10, sy - 2), (sx + 10, sy + 12)], outline=(100, 80, 200), fill=(15, 10, 50))

    # ── Audit trail data streams ────────────────────────────────────────
    stream_colors = [(0, 180, 255), (0, 140, 220), (30, 180, 255)]
    for i in range(14):
        y_pos = random.randint(60, height - 60)
        x_start = random.randint(-150, 50)
        x_end = random.randint(850, width + 80)
        col = random.choice(stream_colors)
        lw = random.choice([1, 1, 2])
        draw.line([(x_start, y_pos), (x_end, y_pos)], fill=col, width=lw)
        glow = (col[0] // 5, col[1] // 5, col[2] // 5)
        draw.line([(x_start, y_pos - 1), (x_end, y_pos - 1)], fill=glow, width=1)
        draw.line([(x_start, y_pos + 1), (x_end, y_pos + 1)], fill=glow, width=1)

    # ── Central AI core ────────────────────────────────────────────────
    core_rings = [
        (90, (0, 60, 140)),
        (70, (0, 100, 200)),
        (50, (0, 150, 240)),
        (30, (0, 200, 255)),
    ]
    for radius, col in core_rings:
        draw.ellipse(
            [(cx - radius, cy - radius), (cx + radius, cy + radius)],
            outline=col, width=2
        )
    for r in [22, 15, 8]:
        core_col = (0, min(255, 180 + r * 3), 255)
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=core_col)

    # Radiating spokes from core
    for angle_deg in range(0, 360, 45):
        angle = math.radians(angle_deg)
        x1 = cx + int(32 * math.cos(angle))
        y1 = cy + int(32 * math.sin(angle))
        x2 = cx + int(145 * math.cos(angle))
        y2 = cy + int(145 * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=(0, 90, 190), width=1)

    # ── Scattered governance nodes ─────────────────────────────────────
    node_colors = [(0, 200, 255), (200, 160, 40), (80, 80, 200)]
    for _ in range(28):
        nx = random.randint(40, width - 40)
        ny = random.randint(40, height - 40)
        dist = math.sqrt((nx - cx) ** 2 + (ny - cy) ** 2)
        if dist < 360:
            continue
        r = random.randint(3, 7)
        col = random.choice(node_colors)
        draw.ellipse([(nx - r, ny - r), (nx + r, ny + r)], fill=col)

    # ── Gold accent bottom bar ─────────────────────────────────────────
    for px in range(0, width):
        t = px / width
        rr = int(180 + t * 40)
        gg = int(130 + t * 40)
        bb = 15
        draw.rectangle([(px, height - 5), (px + 1, height - 1)], fill=(rr, gg, bb))

    # ── Subtle vignette ────────────────────────────────────────────────
    arr_img = np.array(img).astype(np.float32)
    vignette_mask = np.zeros((height, width), dtype=np.float32)
    for y in range(height):
        for x in range(0, width, 4):
            dx = (x - width / 2) / (width / 2)
            dy = (y - height / 2) / (height / 2)
            vignette_mask[y, x:x+4] = min(1.0, (dx * dx + dy * dy) * 0.35)
    for c in range(3):
        arr_img[:, :, c] = np.clip(arr_img[:, :, c] * (1 - vignette_mask * 0.6), 0, 255)

    return Image.fromarray(arr_img.astype(np.uint8))


def find_asset(name):
    p = ASSETS + name
    if os.path.exists(p):
        return p
    raise FileNotFoundError(f"Asset not found: {p}")


hero_img = generate_hero(1200, H)
hero_img.save(OUT_DIR + 'hero_raw.png')
print("✅ Hero image generated")

# Logo: c_white_claude (2).png → extract white pixels → render as black on white
logo_src = Image.open(find_asset('c_white_claude (2).png')).convert('RGBA')
arr_l = np.array(logo_src)
rgba_l = np.zeros((arr_l.shape[0], arr_l.shape[1], 4), dtype=np.uint8)
rgba_l[arr_l[:, :, 0] > 200] = [1, 1, 1, 255]
logo = Image.fromarray(rgba_l, 'RGBA')
bbox = logo.getbbox()
if bbox:
    logo = logo.crop(bbox)
logo_h = 80
logo_w = int(logo.width * logo_h / logo.height)
logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
print(f"✅ Logo loaded: {logo_w}x{logo_h}")

# Canvas
banner = Image.new('RGB', (W, H), (250, 250, 250))
banner.paste(hero_img, (0, 0))
draw = ImageDraw.Draw(banner)
draw.rectangle([1200, 0, W, H], fill=(250, 250, 250))
draw.line([(1200, 0), (1200, H)], fill=(215, 215, 215), width=2)
banner.paste(logo, (W - logo_w - 64, 52), logo)


def tw(txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    return bb[2] - bb[0]


def th(txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    return bb[3] - bb[1]


MAX_W = 1200 - 80 - 40


def wrap_to_n(text, font, max_w, n_lines):
    words = text.split()
    if n_lines == 1:
        return [text] if tw(text, font) <= max_w else None
    if n_lines == 2:
        best = None
        for i in range(1, len(words)):
            l1, l2 = " ".join(words[:i]), " ".join(words[i:])
            if tw(l1, font) <= max_w and tw(l2, font) <= max_w:
                diff = abs(tw(l1, font) - tw(l2, font))
                if best is None or diff < best[0]:
                    best = (diff, [l1, l2])
        return best[1] if best else None
    if n_lines == 3:
        best = None
        for i in range(1, len(words) - 1):
            for j in range(i + 1, len(words)):
                l1 = " ".join(words[:i])
                l2 = " ".join(words[i:j])
                l3 = " ".join(words[j:])
                if all(tw(l, font) <= max_w for l in [l1, l2, l3]):
                    widths = [tw(l, font) for l in [l1, l2, l3]]
                    spread = max(widths) - min(widths)
                    if best is None or spread < best[0]:
                        best = (spread, [l1, l2, l3])
        return best[1] if best else None
    return None


# Auto-fit Line 1 (Regular)
fs1 = 62
line1_lines = [TITLE_LINE1]
font_l1 = None
for fs in range(62, 31, -2):
    fnt = ImageFont.truetype(find_asset('Satoshi-Regular.otf'), fs)
    if tw(TITLE_LINE1, fnt) <= MAX_W:
        font_l1 = fnt; fs1 = fs; line1_lines = [TITLE_LINE1]; break
    r2 = wrap_to_n(TITLE_LINE1, fnt, MAX_W, 2)
    if r2:
        font_l1 = fnt; fs1 = fs; line1_lines = r2; break
    r3 = wrap_to_n(TITLE_LINE1, fnt, MAX_W, 3)
    if r3:
        font_l1 = fnt; fs1 = fs; line1_lines = r3; break

# Auto-fit Line 2 (Bold)
fs2 = 88
line2_lines = [TITLE_LINE2]
font_l2 = None
for fs in range(88, 35, -2):
    fnt = ImageFont.truetype(find_asset('Satoshi-Bold.otf'), fs)
    if tw(TITLE_LINE2, fnt) <= MAX_W:
        font_l2 = fnt; fs2 = fs; line2_lines = [TITLE_LINE2]; break
    r2 = wrap_to_n(TITLE_LINE2, fnt, MAX_W, 2)
    if r2:
        font_l2 = fnt; fs2 = fs; line2_lines = r2; break
    r3 = wrap_to_n(TITLE_LINE2, fnt, MAX_W, 3)
    if r3:
        font_l2 = fnt; fs2 = fs; line2_lines = r3; break

font_url = ImageFont.truetype(find_asset('Satoshi-Medium.otf'), 36)

# Vertically centre text block
BLACK = (1, 1, 1)
PAD_R = 80
gap = 28
line_gap = 12

l1_heights = [th(l, font_l1) for l in line1_lines]
total_l1_h = sum(l1_heights) + line_gap * (len(line1_lines) - 1)
l2_heights = [th(l, font_l2) for l in line2_lines]
total_l2_h = sum(l2_heights) + line_gap * (len(line2_lines) - 1)
total_h = total_l1_h + gap + total_l2_h
ty = (H - total_h) // 2

cur_y = ty
for i, line in enumerate(line1_lines):
    draw.text((W - tw(line, font_l1) - PAD_R, cur_y), line, font=font_l1, fill=BLACK)
    cur_y += l1_heights[i] + line_gap
cur_y = ty + total_l1_h + gap
for i, line in enumerate(line2_lines):
    draw.text((W - tw(line, font_l2) - PAD_R, cur_y), line, font=font_l2, fill=BLACK)
    cur_y += l2_heights[i] + line_gap

# codiste.com — -2% letter spacing
url_txt = "codiste.com"
char_spacing = -int(36 * 0.02)
total_url_w = sum(tw(ch, font_url) for ch in url_txt) + char_spacing * (len(url_txt) - 1)
x_cur = W - total_url_w - PAD_R
url_y = H - 65
for ch in url_txt:
    draw.text((x_cur, url_y), ch, font=font_url, fill=BLACK)
    x_cur += tw(ch, font_url) + char_spacing

# Export
png_path = OUT_DIR + f'codiste-banner-{SLUG}.png'
jpg_path = OUT_DIR + f'codiste-banner-{SLUG}.jpg'
banner.save(png_path, 'PNG', dpi=(288, 288))
banner.save(jpg_path, 'JPEG', quality=95, dpi=(288, 288))
print(f"✅ Banner PNG: {png_path}")
print(f"✅ Banner JPG: {jpg_path}")
print(f"   L1: {fs1}px ({len(line1_lines)} lines) | L2: {fs2}px ({len(line2_lines)} lines)")
