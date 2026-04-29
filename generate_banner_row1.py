"""
Codiste LinkedIn Banner — Row 1
Scaling Compliance: Why Your Framework Breaks at Market Three
Visual metaphor: Modular compliance layers plugging into a central infrastructure backbone
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import os
import random

ASSETS = '/home/user/linkedin_post_creation/'
OUT_DIR = '/home/user/linkedin_post_creation/output/scaling-compliance-global-frameworks/'
os.makedirs(OUT_DIR, exist_ok=True)

TITLE_LINE1 = "Scaling Compliance:"
TITLE_LINE2 = "Why Your Framework Breaks at Market Three"
SLUG = "scaling-compliance-global-frameworks"

W, H = 2400, 1348


def generate_hero(width=1200, height=1348):
    """Modular compliance architecture: layered modules connecting to a glowing core backbone."""
    random.seed(77)
    img = Image.new('RGB', (width, height), (4, 8, 28))
    draw = ImageDraw.Draw(img)

    # Deep navy gradient background
    for y in range(height):
        t = y / height
        r = int(4 + t * 8)
        g = int(8 + t * 12)
        b = int(28 + t * 25)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Central backbone — vertical glowing spine
    spine_x = width // 2
    for offset in range(-18, 19):
        alpha = max(0, 90 - abs(offset) * 5)
        col = (0, min(255, 160 + abs(offset) * 2), min(255, 220 + abs(offset)))
        if abs(offset) <= 3:
            draw.line([(spine_x + offset, 60), (spine_x + offset, height - 60)],
                      fill=col, width=1)
        else:
            glow = (0, alpha // 4, alpha // 2)
            draw.line([(spine_x + offset, 60), (spine_x + offset, height - 60)],
                      fill=glow, width=1)

    # Glowing core nodes along the backbone
    node_y_positions = [int(height * t) for t in [0.18, 0.35, 0.52, 0.68, 0.82]]
    node_colors = [
        (0, 200, 255), (0, 220, 200), (20, 180, 255),
        (0, 210, 230), (0, 190, 255)
    ]
    for ny, ncol in zip(node_y_positions, node_colors):
        for r in [30, 22, 14, 8, 4]:
            fade = int(255 * (1 - r / 32))
            c = (0, min(255, ncol[1] - 20 + r * 3), min(255, ncol[2]))
            draw.ellipse([(spine_x - r, ny - r), (spine_x + r, ny + r)], fill=c)

    # Compliance modules — glowing rectangles on both sides
    module_defs = [
        # (y_center, side: -1=left, +1=right, label_color, width, height_mod)
        (int(H * 0.20), -1, (0, 180, 255), 220, 80),
        (int(H * 0.38), -1, (0, 200, 220), 200, 70),
        (int(H * 0.56), -1, (20, 210, 255), 230, 75),
        (int(H * 0.74), -1, (0, 190, 240), 210, 65),
        (int(H * 0.25), 1, (0, 200, 255), 215, 78),
        (int(H * 0.44), 1, (0, 185, 230), 225, 72),
        (int(H * 0.62), 1, (10, 200, 255), 205, 70),
        (int(H * 0.80), 1, (0, 195, 245), 220, 68),
    ]

    for my, side, mcol, mw, mh in module_defs:
        if side == -1:
            mx1 = spine_x - 110 - mw
            mx2 = spine_x - 110
        else:
            mx1 = spine_x + 110
            mx2 = spine_x + 110 + mw

        # Module glow halo
        for expand in [12, 8, 4]:
            glow = (mcol[0] // 6, mcol[1] // 6, mcol[2] // 6)
            draw.rectangle(
                [(mx1 - expand, my - mh // 2 - expand),
                 (mx2 + expand, my + mh // 2 + expand)],
                outline=glow
            )

        # Module fill
        mod_fill = (mcol[0] // 12, mcol[1] // 10, mcol[2] // 8)
        draw.rectangle(
            [(mx1, my - mh // 2), (mx2, my + mh // 2)],
            fill=mod_fill, outline=mcol
        )
        draw.rectangle(
            [(mx1 + 2, my - mh // 2 + 2), (mx2 - 2, my + mh // 2 - 2)],
            outline=(mcol[0] // 3, mcol[1] // 3, mcol[2] // 3)
        )

        # Internal module lines (data fields)
        for li in range(1, 4):
            ly = my - mh // 2 + int(mh * li / 4)
            line_w = int(mw * random.uniform(0.3, 0.7))
            lx = mx1 + (mw - line_w) // 2
            draw.line([(lx, ly), (lx + line_w, ly)],
                      fill=(mcol[0] // 4, mcol[1] // 4, mcol[2] // 4), width=1)

        # Connector line to backbone node
        closest_node = min(node_y_positions, key=lambda n: abs(n - my))
        conn_end_x = spine_x if side == -1 else spine_x
        conn_start_x = mx2 if side == -1 else mx1
        # Draw stepped connector
        mid_x = (conn_start_x + conn_end_x) // 2
        conn_col = (0, mcol[1] // 3, mcol[2] // 3)
        draw.line([(conn_start_x, my), (mid_x, my)], fill=conn_col, width=1)
        draw.line([(mid_x, my), (mid_x, closest_node)], fill=conn_col, width=1)
        draw.line([(mid_x, closest_node), (conn_end_x, closest_node)],
                  fill=conn_col, width=1)
        # Dot at connector point
        draw.ellipse([(conn_start_x - 3, my - 3), (conn_start_x + 3, my + 3)],
                     fill=mcol)

    # Data stream particles flowing toward backbone
    for _ in range(60):
        px = random.randint(30, width - 30)
        py = random.randint(30, height - 30)
        ps = random.randint(1, 3)
        pcol = random.choice([(0, 160, 220), (0, 200, 255), (20, 180, 240)])
        draw.ellipse([(px - ps, py - ps), (px + ps, py + ps)], fill=pcol)

    # Subtle horizontal grid lines
    for gy in range(0, height, 80):
        draw.line([(0, gy), (width, gy)],
                  fill=(10, 20, 50), width=1)

    # Teal accent bar at bottom
    for px in range(0, width):
        t = px / width
        r = int(0 + t * 10)
        g = int(160 + t * 60)
        b = int(200 + t * 40)
        draw.rectangle([(px, height - 5), (px + 1, height)], fill=(r, g, b))

    # Vignette
    arr = np.array(img).astype(np.float32)
    vig = np.zeros_like(arr)
    cx, cy = width / 2, height / 2
    for y in range(height):
        for x in range(0, width, 4):
            dx = (x - cx) / cx
            dy = (y - cy) / cy
            d = min(1.0, math.sqrt(dx * dx + dy * dy))
            vig[y, x:x + 4] = d * d * 120
    result = np.clip(arr - vig, 0, 255).astype(np.uint8)
    return Image.fromarray(result)


def find_asset(name):
    p = ASSETS + name
    if os.path.exists(p):
        return p
    raise FileNotFoundError(f"Asset not found: {p}")


# Generate hero
hero_img = generate_hero(1200, H)
hero_raw_path = OUT_DIR + 'hero_raw_row1.png'
hero_img.save(hero_raw_path)
print("✅ Hero image generated")

# Load logo
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

# Vertically centre
BLACK = (1, 1, 1); PAD_R = 80; gap = 28; line_gap = 12
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

# codiste.com
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
