"""
Codiste LinkedIn Banner Generator
Generates hero image + composites the 2400x1348 Codiste banner
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import os
import random

ASSETS = '/home/user/linkedin_post_creation/'
OUT_DIR = '/home/user/linkedin_post_creation/output/'
os.makedirs(OUT_DIR, exist_ok=True)

TITLE_LINE1 = "Why Your AI Risk Model Isn't the Problem:"
TITLE_LINE2 = "What Banks Get Wrong"
SLUG = "ai-risk-model-banks"

W, H = 2400, 1348

# ── STEP 1: Generate Hero Image (left panel) ─────────────────────────────────
def generate_hero(width=1200, height=1348):
    """Create a dark-themed financial/AI risk visualization."""
    random.seed(42)
    img = Image.new('RGB', (width, height), (6, 10, 35))
    draw = ImageDraw.Draw(img)

    # Background gradient (dark navy → deep blue)
    for y in range(height):
        t = y / height
        r = int(6 + t * 10)
        g = int(10 + t * 15)
        b = int(35 + t * 30)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Grid lines (circuit-board effect)
    grid_col = (20, 40, 90)
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=grid_col, width=1)
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=grid_col, width=1)

    # Data flow streams (horizontal glowing lines)
    stream_colors = [
        (0, 180, 255), (0, 140, 220), (30, 200, 255),
        (0, 120, 200), (50, 160, 255)
    ]
    for i in range(18):
        y_pos = random.randint(80, height - 80)
        x_start = random.randint(-200, 100)
        x_end = random.randint(900, width + 100)
        col = random.choice(stream_colors)
        alpha_val = random.randint(60, 160)
        # Main line
        lw = random.choice([1, 1, 2])
        draw.line([(x_start, y_pos), (x_end, y_pos)], fill=col, width=lw)
        # Glow above/below
        glow_col = (col[0] // 4, col[1] // 4, col[2] // 4)
        draw.line([(x_start, y_pos - 1), (x_end, y_pos - 1)], fill=glow_col, width=1)
        draw.line([(x_start, y_pos + 1), (x_end, y_pos + 1)], fill=glow_col, width=1)

    # Circuit nodes (intersection dots)
    node_positions = []
    for _ in range(35):
        nx = random.randint(60, width - 60)
        ny = random.randint(60, height - 60)
        # Snap to grid
        nx = (nx // 60) * 60
        ny = (ny // 60) * 60
        node_positions.append((nx, ny))
        r = random.randint(3, 8)
        col = random.choice([(0, 200, 255), (0, 160, 220), (100, 220, 255)])
        draw.ellipse([(nx - r, ny - r), (nx + r, ny + r)], fill=col)
        # Outer glow ring
        gr = r + 4
        glow = (col[0] // 5, col[1] // 5, col[2] // 5)
        draw.ellipse([(nx - gr, ny - gr), (nx + gr, ny + gr)], outline=glow, width=1)

    # Connect some nodes with lines (circuit traces)
    for i in range(min(20, len(node_positions) - 1)):
        p1 = node_positions[i]
        p2 = node_positions[(i + 3) % len(node_positions)]
        trace_col = (0, 80, 150)
        draw.line([p1, p2], fill=trace_col, width=1)

    # Central AI core — glowing concentric rings
    cx, cy = width // 2, height // 2
    ring_colors = [
        (0, 200, 255), (0, 160, 220), (0, 120, 180),
        (0, 80, 140), (0, 50, 100)
    ]
    for idx, (radius, col) in enumerate(zip([200, 160, 120, 80, 40], ring_colors)):
        draw.ellipse(
            [(cx - radius, cy - radius), (cx + radius, cy + radius)],
            outline=col, width=2 if idx < 2 else 1
        )

    # Central bright core
    for r in [35, 25, 15, 8]:
        alpha = int(255 * (1 - r / 40))
        core_col = (0, min(255, 180 + r * 2), 255)
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=core_col)

    # Radiating spokes from core
    for angle_deg in range(0, 360, 30):
        angle = math.radians(angle_deg)
        x1 = cx + int(45 * math.cos(angle))
        y1 = cy + int(45 * math.sin(angle))
        x2 = cx + int(200 * math.cos(angle))
        y2 = cy + int(200 * math.sin(angle))
        spoke_col = (0, 100, 200)
        draw.line([(x1, y1), (x2, y2)], fill=spoke_col, width=1)

    # Floating data squares (financial data blocks)
    gold = (255, 200, 50)
    blue = (0, 180, 255)
    for _ in range(12):
        bx = random.randint(30, width - 80)
        by = random.randint(30, height - 80)
        bw = random.randint(20, 50)
        bh = random.randint(12, 30)
        col = random.choice([gold, blue, (0, 220, 180)])
        border_col = (col[0] // 3, col[1] // 3, col[2] // 3)
        draw.rectangle([(bx, by), (bx + bw, by + bh)], outline=col, width=1)
        # Fill partially
        draw.rectangle([(bx + 2, by + 2), (bx + bw - 2, by + bh - 2)], fill=border_col)

    # Shield / security overlay (top-left quadrant — risk management motif)
    sx, sy = 220, 280
    shield_pts = [
        (sx, sy - 80), (sx + 60, sy - 80), (sx + 60, sy + 20),
        (sx, sy + 60), (sx - 60, sy + 20), (sx - 60, sy - 80)
    ]
    draw.polygon(shield_pts, outline=(0, 180, 255), fill=(0, 30, 80))
    # Checkmark inside shield
    ck_col = (0, 220, 120)
    draw.line([(sx - 20, sy), (sx, sy + 20), (sx + 30, sy - 20)], fill=ck_col, width=3)

    # Binary/hex data rain (right side)
    hex_chars = ['0', '1', 'A', 'F', '9', '3', 'E', '7', 'B', '2']
    try:
        small_font = ImageFont.truetype(ASSETS + 'Satoshi-Regular.otf', 14)
    except Exception:
        small_font = ImageFont.load_default()

    for col_x in range(900, width - 20, 40):
        for row_y in range(0, height, 30):
            if random.random() < 0.3:
                ch = random.choice(hex_chars)
                brightness = random.randint(30, 100)
                char_col = (0, brightness, brightness * 2)
                draw.text((col_x, row_y), ch, font=small_font, fill=char_col)

    # Gold accent bar (bottom — financial stability)
    bar_h = 6
    for px in range(0, width):
        t = px / width
        r = int(200 + t * 55)
        g = int(150 + t * 50)
        b = int(20)
        draw.rectangle([(px, height - bar_h - 1), (px + 1, height - 1)], fill=(r, g, b))

    # Apply subtle vignette
    vignette = Image.new('RGB', (width, height), (0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for step in range(300):
        t = step / 300
        alpha = int(180 * t * t)
        col_v = (alpha, alpha, alpha)
        v_draw.ellipse(
            [(step, step), (width - step, height - step)],
            outline=(0, 0, 0)
        )
    # Blend vignette
    arr_img = np.array(img).astype(np.float32)
    arr_vig = np.array(vignette).astype(np.float32)
    blended = np.clip(arr_img * (1 - arr_vig / 600), 0, 255).astype(np.uint8)
    hero = Image.fromarray(blended)

    return hero


# ── STEP 2: Composite Banner ──────────────────────────────────────────────────
def find_asset(name):
    p = ASSETS + name
    if os.path.exists(p):
        return p
    raise FileNotFoundError(f"Asset not found: {p}")


hero_img = generate_hero(1200, H)
hero_img.save(OUT_DIR + 'hero_raw.png')
print("✅ Hero image generated")

# Load logo: c_white_claude (2).png — extract white pixels → render as black
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

# Fonts
def tw(txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    return bb[2] - bb[0]

def th(txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt)
    return bb[3] - bb[1]

MAX_W = 1200 - 80 - 40  # 1080px

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

# Vertically centre all text
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
