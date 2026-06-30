from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

ASSETS = '/home/user/linkedin_post_creation/'
W, H = 2400, 1348

ARTICLES = [
    {
        'slug': 'saas-support-deflection',
        'hero': 'freepik-hero-saas-support-deflection.png',
        'LINE1': 'AI Support Agents:',
        'LINE2': '38% Fewer Tickets, Same CSAT',
    },
    {
        'slug': 'fintech-trading-desks',
        'hero': 'freepik-hero-fintech-trading-desks.png',
        'LINE1': 'Agentic AI for Fintech:',
        'LINE2': 'Built for Latency & Compliance',
    },
    {
        'slug': 'martech-campaign-ops',
        'hero': 'freepik-hero-martech-campaign-ops.png',
        'LINE1': 'AI Campaign Agents:',
        'LINE2': '16 Days to 3.8 Days',
    },
    {
        'slug': 'enterprise-ai-solutions',
        'hero': 'freepik-hero-enterprise-ai-solutions.png',
        'LINE1': 'Enterprise AI Agents:',
        'LINE2': 'Map Workflows Before Vendors',
    },
]

def find_asset(name):
    p = ASSETS + name
    if os.path.exists(p): return p
    raise FileNotFoundError(f"Asset {name} not found")

def tw(draw, t, f):
    bb = draw.textbbox((0,0), t, font=f)
    return bb[2] - bb[0]

def th(draw, t, f):
    bb = draw.textbbox((0,0), t, font=f)
    return bb[3] - bb[1]

def wrap_to_n(draw, text, font, max_w, n):
    words = text.split()
    if n == 1:
        return [text] if tw(draw, text, font) <= max_w else None
    if n == 2:
        best = None
        for i in range(1, len(words)):
            l1, l2 = " ".join(words[:i]), " ".join(words[i:])
            if tw(draw, l1, font) <= max_w and tw(draw, l2, font) <= max_w:
                d = abs(tw(draw, l1, font) - tw(draw, l2, font))
                if best is None or d < best[0]: best = (d, [l1, l2])
        return best[1] if best else None
    if n == 3:
        best = None
        for i in range(1, len(words)-1):
            for j in range(i+1, len(words)):
                l1 = " ".join(words[:i])
                l2 = " ".join(words[i:j])
                l3 = " ".join(words[j:])
                if all(tw(draw, l, font) <= max_w for l in [l1, l2, l3]):
                    s = max(tw(draw, l, font) for l in [l1,l2,l3]) - min(tw(draw, l, font) for l in [l1,l2,l3])
                    if best is None or s < best[0]: best = (s, [l1, l2, l3])
        return best[1] if best else None

os.makedirs(f'{ASSETS}outputs', exist_ok=True)

for art in ARTICLES:
    LINE1 = art['LINE1']
    LINE2 = art['LINE2']
    slug  = art['slug']
    hero_path = ASSETS + art['hero']

    # Hero panel (left 1200px)
    hero_src = Image.open(hero_path).convert('RGB')
    scale = max(1200 / hero_src.width, H / hero_src.height)
    dw, dh = int(hero_src.width * scale), int(hero_src.height * scale)
    hero = hero_src.resize((dw, dh), Image.LANCZOS)
    ox, oy = (dw - 1200) // 2, (dh - H) // 2
    hero_panel = hero.crop((ox, oy, ox + 1200, oy + H))

    # Logo
    logo_src = Image.open(find_asset('c_white_claude.png')).convert('RGBA')
    arr = np.array(logo_src)
    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[arr[:, :, 0] > 200] = [1, 1, 1, 255]
    logo = Image.fromarray(rgba, 'RGBA')
    bbox = logo.getbbox()
    if bbox: logo = logo.crop(bbox)
    logo_h = 80
    logo_w = int(logo.width * logo_h / logo.height)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    # Canvas
    banner = Image.new('RGB', (W, H), (250, 250, 250))
    banner.paste(hero_panel, (0, 0))
    draw = ImageDraw.Draw(banner)
    draw.rectangle([1200, 0, W, H], fill=(250, 250, 250))
    draw.line([(1200, 0), (1200, H)], fill=(215, 215, 215), width=2)
    banner.paste(logo, (W - logo_w - 64, 52), logo)

    MAX_W = 1200 - 80 - 40

    # Auto-fit Line 1 (Regular)
    fs1 = 62
    line1_lines = [LINE1]
    while fs1 >= 32:
        f1 = ImageFont.truetype(find_asset('Satoshi-Regular.otf'), fs1)
        if tw(draw, LINE1, f1) <= MAX_W:
            line1_lines = [LINE1]; break
        r = wrap_to_n(draw, LINE1, f1, MAX_W, 2)
        if r: line1_lines = r; break
        r = wrap_to_n(draw, LINE1, f1, MAX_W, 3)
        if r: line1_lines = r; break
        fs1 -= 2
    font_l1 = ImageFont.truetype(find_asset('Satoshi-Regular.otf'), fs1)

    # Auto-fit Line 2 (Bold)
    fs2 = 88
    line2_lines = [LINE2]
    while fs2 >= 36:
        f2 = ImageFont.truetype(find_asset('Satoshi-Bold.otf'), fs2)
        if tw(draw, LINE2, f2) <= MAX_W:
            line2_lines = [LINE2]; break
        r = wrap_to_n(draw, LINE2, f2, MAX_W, 2)
        if r: line2_lines = r; break
        r = wrap_to_n(draw, LINE2, f2, MAX_W, 3)
        if r: line2_lines = r; break
        fs2 -= 2
    font_l2 = ImageFont.truetype(find_asset('Satoshi-Bold.otf'), fs2)

    font_url = ImageFont.truetype(find_asset('Satoshi-Medium.otf'), 36)
    BLACK = (1, 1, 1)
    PAD_R = 80
    gap = 28
    line_gap = 12

    l1h = [th(draw, l, font_l1) for l in line1_lines]
    l2h = [th(draw, l, font_l2) for l in line2_lines]
    total_h = sum(l1h) + line_gap*(len(l1h)-1) + gap + sum(l2h) + line_gap*(len(l2h)-1)
    ty = (H - total_h) // 2

    y = ty
    for i, line in enumerate(line1_lines):
        draw.text((W - tw(draw, line, font_l1) - PAD_R, y), line, font=font_l1, fill=BLACK)
        y += l1h[i] + line_gap
    y = ty + sum(l1h) + line_gap*(len(l1h)-1) + gap
    for i, line in enumerate(line2_lines):
        draw.text((W - tw(draw, line, font_l2) - PAD_R, y), line, font=font_l2, fill=BLACK)
        y += l2h[i] + line_gap

    # codiste.com URL
    url_txt = "codiste.com"
    cs = -int(36 * 0.02)
    uw = sum(tw(draw, c, font_url) for c in url_txt) + cs * (len(url_txt) - 1)
    x = W - uw - PAD_R
    uy = H - 65
    for c in url_txt:
        draw.text((x, uy), c, font=font_url, fill=BLACK)
        x += tw(draw, c, font_url) + cs

    out_png = f'{ASSETS}outputs/codiste-banner-{slug}.png'
    out_jpg = f'{ASSETS}outputs/codiste-banner-{slug}.jpg'
    banner.save(out_png, 'PNG', dpi=(288, 288))
    banner.save(out_jpg, 'JPEG', quality=95, dpi=(288, 288))
    print(f"✅ {slug}: L1:{fs1}px L2:{fs2}px  PNG:{os.path.getsize(out_png)//1024}KB  JPG:{os.path.getsize(out_jpg)//1024}KB")
