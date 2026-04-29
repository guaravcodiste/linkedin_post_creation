"""
Codiste LinkedIn Banner — Row 2
Zero-Trust Compliance: The C-Suite Playbook for 2026
Visual metaphor: Central verification node with scanning beams, AI neural mesh, zero-trust gates
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import os
import random

ASSETS = '/home/user/linkedin_post_creation/'
OUT_DIR = '/home/user/linkedin_post_creation/output/zero-trust-compliance-ai-regtech/'
os.makedirs(OUT_DIR, exist_ok=True)

TITLE_LINE1 = "Zero-Trust Compliance:"
TITLE_LINE2 = "The C-Suite Playbook for 2026"
SLUG = "zero-trust-compliance-ai-regtech"

W, H = 2400, 1348


def generate_hero(width=1200, height=1348):
    """Zero-trust visual: central verification node, scanning beams, AI neural mesh."""
    random.seed(99)
    img = Image.new('RGB', (width, height), (5, 5, 22))
    draw = ImageDraw.Draw(img)

    # Deep dark purple-navy gradient
    for y in range(height):
        t = y / height
        r = int(5 + t * 8)
        g = int(5 + t * 8)
        b = int(22 + t * 28)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    cx, cy = width // 2, height // 2

    # ── Background neural mesh ──────────────────────────────────────
    mesh_pts = []
    random.seed(42)
    for _ in range(55):
        mx = random.randint(40, width - 40)
        my = random.randint(40, height - 40)
        mesh_pts.append((mx, my))
        dot_r = random.randint(2, 5)
        dot_col = random.choice([(0, 80, 160), (60, 0, 120), (0, 100, 180)])
        draw.ellipse([(mx - dot_r, my - dot_r), (mx + dot_r, my + dot_r)], fill=dot_col)

    # Connect nearby mesh nodes
    for i, p1 in enumerate(mesh_pts):
        for p2 in mesh_pts[i + 1:]:
            dist = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
            if dist < 200:
                alpha = int(40 * (1 - dist / 200))
                draw.line([p1, p2], fill=(0, alpha, alpha * 2), width=1)

    # ── Concentric verification rings ──────────────────────────────
    ring_params = [
        (320, (0, 80, 160), 1),
        (260, (0, 100, 180), 1),
        (200, (0, 130, 210), 1),
        (150, (0, 160, 230), 2),
        (100, (30, 180, 250), 2),
        (60, (60, 200, 255), 2),
    ]
    for radius, col, lw in ring_params:
        draw.ellipse(
            [(cx - radius, cy - radius), (cx + radius, cy + radius)],
            outline=col, width=lw
        )

    # ── Scanning beams radiating from center ────────────────────────
    beam_angles = [i * 30 for i in range(12)]
    for angle_deg in beam_angles:
        angle = math.radians(angle_deg)
        for beam_len in range(70, 450, 15):
            bx = cx + int(beam_len * math.cos(angle))
            by = cy + int(beam_len * math.sin(angle))
            if 0 <= bx < width and 0 <= by < height:
                fade = max(0, 80 - int(80 * beam_len / 450))
                beam_col = (0, fade, min(255, fade * 3))
                draw.ellipse([(bx - 1, by - 1), (bx + 1, by + 1)], fill=beam_col)

    # Solid primary beams
    primary_angles = [0, 60, 120, 180, 240, 300]
    for angle_deg in primary_angles:
        angle = math.radians(angle_deg)
        x2 = cx + int(500 * math.cos(angle))
        y2 = cy + int(500 * math.sin(angle))
        draw.line([(cx, cy), (x2, y2)], fill=(0, 60, 130), width=1)

    # ── Verification gate checkpoints along beams ───────────────────
    gate_positions = [
        (cx + 180, cy), (cx - 180, cy),
        (cx, cy + 180), (cx, cy - 180),
        (int(cx + 130 * math.cos(math.radians(60))),
         int(cy + 130 * math.sin(math.radians(60)))),
        (int(cx + 130 * math.cos(math.radians(300))),
         int(cy + 130 * math.sin(math.radians(300)))),
    ]
    for gx, gy in gate_positions:
        gate_col = (0, 180, 220)
        gate_size = 18
        # Gate symbol: two parallel lines with gap
        draw.rectangle(
            [(gx - gate_size, gy - gate_size // 3),
             (gx - gate_size // 4, gy + gate_size // 3)],
            outline=gate_col, width=1,
            fill=(0, gate_col[1] // 8, gate_col[2] // 8)
        )
        draw.rectangle(
            [(gx + gate_size // 4, gy - gate_size // 3),
             (gx + gate_size, gy + gate_size // 3)],
            outline=gate_col, width=1,
            fill=(0, gate_col[1] // 8, gate_col[2] // 8)
        )
        # Check mark indicator
        ck_col = (0, 220, 150)
        draw.line([(gx - 8, gy), (gx - 2, gy + 6), (gx + 8, gy - 6)],
                  fill=ck_col, width=2)

    # ── Central verification core ───────────────────────────────────
    core_layers = [
        (40, (0, 60, 130)),
        (32, (0, 100, 180)),
        (24, (0, 140, 210)),
        (16, (0, 180, 240)),
        (10, (80, 210, 255)),
        (5, (180, 240, 255)),
    ]
    for r, col in core_layers:
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=col)

    # ── Pulsing wave rings (monitoring pulses) ──────────────────────
    pulse_radii = [380, 430, 480]
    for pr in pulse_radii:
        alpha = int(25 * (1 - (pr - 380) / 100))
        draw.ellipse(
            [(cx - pr, cy - pr), (cx + pr, cy + pr)],
            outline=(0, alpha * 3, alpha * 5), width=1
        )

    # ── AI activity dots scattered around ─────────────────────────
    random.seed(55)
    for _ in range(40):
        ax = random.randint(30, width - 30)
        ay = random.randint(30, height - 30)
        dist = math.sqrt((ax - cx) ** 2 + (ay - cy) ** 2)
        if dist > 80:
            ar = random.randint(1, 4)
            acol = random.choice([
                (0, 150, 220), (60, 0, 140), (0, 180, 200), (80, 100, 220)
            ])
            draw.ellipse([(ax - ar, ay - ar), (ax + ar, ay + ar)], fill=acol)

    # Purple accent horizontal streaks
    random.seed(66)
    for _ in range(12):
        sy = random.randint(50, height - 50)
        sx = random.randint(0, width // 3)
        ex = random.randint(width * 2 // 3, width)
        scol = (random.randint(40, 100), 0, random.randint(120, 180))
        draw.line([(sx, sy), (ex, sy)], fill=scol, width=1)

    # Purple accent bar at bottom
    for px in range(0, width):
        t = px / width
        r = int(60 + t * 40)
        g = int(0)
        b = int(140 + t * 60)
        draw.rectangle([(px, height - 5), (px + 1, height)], fill=(r, g, b))

    # Vignette
    arr = np.array(img).astype(np.float32)
    vig = np.zeros_like(arr)
    cxf, cyf = width / 2, height / 2
    for y in range(height):
        for x in range(0, width, 4):
            dx = (x - cxf) / cxf
            dy = (y - cyf) / cyf
            d = min(1.0, math.sqrt(dx * dx + dy * dy))
            vig[y, x:x + 4] = d * d * 110
    result = np.clip(arr - vig, 0, 255).astype(np.uint8)
    return Image.fromarray(result)


def find_asset(name):
    p = ASSETS + name
    if os.path.exists(p):
        return p
    raise FileNotFoundError(f"Asset not found: {p}")


# Generate hero
hero_img = generate_hero(1200, H)
hero_raw_path = OUT_DIR + 'hero_raw_row2.png'
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
