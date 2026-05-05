"""
Carousel builder: AI Agents for SaaS Customer Success
Codiste brand system — Satoshi fonts, #010101/#FAFAFA/#868686 palette
"""
import os
import glob
import textwrap
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas as rl_canvas

WORK_DIR = '/home/user/linkedin_post_creation'
OUT_DIR  = '/mnt/user-data/outputs'
CLAUDE   = '/home/claude'
TOPIC    = 'ai_agents_saas_customer_success'
W, H     = 1080, 1350
PAD      = 64

BLACK = (1, 1, 1)
WHITE = (250, 250, 250)
GREY  = (134, 134, 134)


# ── fonts ─────────────────────────────────────────────────────────────────────
def font(weight, size):
    names = {400: 'Satoshi-Regular.otf', 700: 'Satoshi-Bold.otf', 900: 'Satoshi-Black.otf'}
    return ImageFont.truetype(os.path.join(WORK_DIR, names[weight]), size)


# ── logo ──────────────────────────────────────────────────────────────────────
LOGO_WHITE = Image.open(os.path.join(WORK_DIR, 'c_white_claude (2).png')).convert('RGBA')
LOGO_BLACK = Image.open(os.path.join(WORK_DIR, 'c_black_claude (2).png')).convert('RGBA')

def paste_logo(img, dark):
    logo_src = LOGO_WHITE if dark else LOGO_BLACK
    logo = logo_src.resize((52, 55), Image.LANCZOS)
    img.paste(logo, (PAD, 58), logo)


# ── grid overlay ──────────────────────────────────────────────────────────────
def draw_grid(draw, dark):
    step  = 54
    alpha = 10   # ~4% of 255
    color = (255, 255, 255, alpha) if dark else (0, 0, 0, alpha)
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=color)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=color)


# ── text helpers ──────────────────────────────────────────────────────────────
def draw_label(draw, text, y, dark):
    f = font(700, 26)
    color = GREY
    # letter-spacing simulation: draw char by char
    x = PAD
    for ch in text.upper():
        draw.text((x, y), ch, font=f, fill=color)
        bbox = f.getbbox(ch)
        x += (bbox[2] - bbox[0]) + 3
    return y + 42


def wrap_text(text, f, max_width):
    words = text.split()
    lines, line = [], ''
    for w in words:
        test = (line + ' ' + w).strip()
        if f.getlength(test) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_headline(draw, lines_data, start_y, line_h=94):
    """lines_data = list of (text, color, weight, size)"""
    y = start_y
    for text, color, weight, size in lines_data:
        f = font(weight, size)
        draw.text((PAD, y), text, font=f, fill=color)
        y += line_h
    return y


def draw_bullets(draw, bullets, start_y, dark):
    f_bullet = font(400, 44)
    text_color = WHITE if dark else BLACK
    dot_color  = GREY
    y = start_y
    for bullet in bullets:
        # dot
        dot_x, dot_y = PAD, y + 22
        draw.ellipse([(dot_x, dot_y), (dot_x + 8, dot_y + 8)], fill=dot_color)
        # text (wrap to width)
        max_w = W - PAD * 2 - 32
        lines = wrap_text(bullet, f_bullet, max_w)
        tx = PAD + 32
        for line in lines:
            draw.text((tx, y), line, font=f_bullet, fill=text_color)
            y += 58
        y += 10
    return y


# ── decorative elements ───────────────────────────────────────────────────────
def draw_asterisk(draw, dark):
    f = font(900, 320)
    color = (255, 255, 255, 10) if dark else (0, 0, 0, 10)
    draw.text((W - 280, -80), '*', font=f, fill=color)


def draw_arrow(draw, dark, symbol='→'):
    f = font(700, 52)
    color = GREY
    bbox = f.getbbox(symbol)
    x = W - PAD - (bbox[2] - bbox[0])
    draw.text((x, H - PAD - 60), symbol, font=f, fill=color)


def draw_divider(draw, y, dark):
    color = (80, 80, 80) if dark else (200, 200, 200)
    draw.line([(PAD, y), (W - PAD, y)], fill=color, width=1)


# ── slide base ────────────────────────────────────────────────────────────────
def new_slide(dark=True):
    bg = BLACK if dark else WHITE
    img  = Image.new('RGBA', (W, H), bg + (255,))
    over = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(over)
    draw_grid(draw, dark)
    img  = Image.alpha_composite(img, over)
    draw = ImageDraw.Draw(img)
    draw_asterisk(draw, dark)
    paste_logo(img, dark)
    return img, draw


def save_slide(img, n):
    path = f'{CLAUDE}/slide_{n:02d}.png'
    img.convert('RGB').save(path, 'PNG')
    print(f'  saved slide_{n:02d}.png')


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

def slide_01():
    img, draw = new_slide(dark=True)
    y = draw_label(draw, 'AI STRATEGY', 155, dark=True)
    y += 22

    # 3-line headline: grey / grey / white
    lines = [
        ('Gross retention dropped.', GREY,  900, 72),
        ('CS team grew 40%.',        GREY,  900, 72),
        ('The math broke.',          WHITE, 900, 80),
    ]
    y = draw_headline(draw, lines, y, line_h=88)
    y += 24

    # body
    body = 'AI agents fix the architecture. Outcome-based pricing makes it pay back.'
    f_body = font(400, 38)
    for line in wrap_text(body, f_body, W - PAD * 2):
        draw.text((PAD, y), line, font=f_body, fill=GREY)
        y += 50

    draw_arrow(draw, dark=True, symbol='Swipe →')
    save_slide(img, 1)


def slide_02():
    img, draw = new_slide(dark=False)
    y = draw_label(draw, 'THE PROBLEM', 145, dark=False)
    y += 18

    draw.text((PAD, y), 'Why CS models fail at scale', font=font(900, 78), fill=BLACK)
    y += 100
    draw_divider(draw, y, dark=False)
    y += 30

    bullets = [
        'Product-led growth flooded self-serve tiers no CSM covers',
        'Self-serve churn runs 22% vs. 9% for named accounts',
        'Fully loaded US CSM cost crossed $250K in 2025',
        'Quarterly renewals demand sub-24-hour churn signals',
    ]
    draw_bullets(draw, bullets, y, dark=False)
    draw_arrow(draw, dark=False)
    save_slide(img, 2)


def slide_03():
    img, draw = new_slide(dark=True)
    y = draw_label(draw, 'THE SHIFT', 145, dark=True)
    y += 18

    draw.text((PAD, y), 'Agents are a profit pool play', font=font(900, 72), fill=WHITE)
    y += 96
    draw_divider(draw, y, dark=True)
    y += 30

    bullets = [
        'Pattern recognition across every account simultaneously',
        'Churn risk surfaces before the customer goes quiet',
        'Expansion signals CSMs would otherwise miss',
        'Outcomes the agent produces become priceable units',
    ]
    draw_bullets(draw, bullets, y, dark=True)
    draw_arrow(draw, dark=True, symbol='↗')
    save_slide(img, 3)


def slide_04():
    img, draw = new_slide(dark=False)
    y = draw_label(draw, 'REAL NUMBERS', 145, dark=False)
    y += 18

    draw.text((PAD, y), '31% churn cut in 9 months', font=font(900, 76), fill=BLACK)
    y += 98
    draw_divider(draw, y, dark=False)
    y += 30

    bullets = [
        '1,800 customers, $42M ARR before deployment',
        'Net revenue churn: 14.2% down to 9.8%',
        'Self-serve churn fell from 22% to 12%',
        'Gross retention climbed from 88% to 93%',
    ]
    draw_bullets(draw, bullets, y, dark=False)
    draw_arrow(draw, dark=False)
    save_slide(img, 4)


def slide_05():
    img, draw = new_slide(dark=True)
    y = draw_label(draw, 'THE PRICING PLAY', 145, dark=True)
    y += 18

    draw.text((PAD, y), 'Outcomes become new revenue', font=font(900, 70), fill=WHITE)
    y += 96
    draw_divider(draw, y, dark=True)
    y += 30

    bullets = [
        'Premium Success tier: $40K-$120K per year',
        '38% of mid-market customers adopted in 6 months',
        '$4.2M net new ARR added by month nine',
        '$720K deployment cost, $6.3M first-year return',
    ]
    draw_bullets(draw, bullets, y, dark=True)
    draw_arrow(draw, dark=True, symbol='↗')
    save_slide(img, 5)


def slide_06():
    img, draw = new_slide(dark=False)
    y = draw_label(draw, 'COVERAGE COMPARED', 145, dark=False)
    y += 18

    draw.text((PAD, y), 'What changes at 100% coverage', font=font(900, 68), fill=BLACK)
    y += 96
    draw_divider(draw, y, dark=False)
    y += 30

    bullets = [
        'Manual CS covers only 30-40% of the customer base',
        'Tool-assisted platforms reach 50-60% at best',
        'Agentic layer monitors every account, every signal',
        'Cost per account drops from up to $9K to under $700',
    ]
    draw_bullets(draw, bullets, y, dark=False)
    draw_arrow(draw, dark=False)
    save_slide(img, 6)


def slide_07():
    img, draw = new_slide(dark=True)
    y = draw_label(draw, 'HOW IT WORKS', 145, dark=True)
    y += 18

    draw.text((PAD, y), 'Three signals, one reasoning layer', font=font(900, 65), fill=WHITE)
    y += 90
    draw_divider(draw, y, dark=True)
    y += 30

    bullets = [
        'Churn risk: flagged before accounts go quiet',
        'Expansion: usage patterns trigger timely AE alerts',
        'Intervention: right playbook routed to the right tier',
        'Every agent action is logged and auditable',
    ]
    draw_bullets(draw, bullets, y, dark=True)
    draw_arrow(draw, dark=True, symbol='↗')
    save_slide(img, 7)


def slide_08():
    img, draw = new_slide(dark=False)
    y = draw_label(draw, 'IMPLEMENTATION', 145, dark=False)
    y += 18

    draw.text((PAD, y), 'Sequence agents into SMB first', font=font(900, 72), fill=BLACK)
    y += 98
    draw_divider(draw, y, dark=False)
    y += 30

    bullets = [
        'Over-automation kills enterprise relationships',
        'Deploy into SMB and mid-market tiers first',
        'Build the data layer before the reasoning layer',
        'Outcome-based pricing follows reliability, not the reverse',
    ]
    draw_bullets(draw, bullets, y, dark=False)
    draw_arrow(draw, dark=False)
    save_slide(img, 8)


def slide_09():
    """CTA close — dark Template F"""
    img, draw = new_slide(dark=True)

    # Main headline
    y = 220
    draw.text((PAD, y), 'Size your', font=font(900, 100), fill=GREY)
    y += 110
    draw.text((PAD, y), 'churn pickup.', font=font(900, 100), fill=WHITE)
    y += 130

    # body
    body = 'We run your retention metrics and show you what a nine-month agentic deployment looks like for your customer mix.'
    f_body = font(400, 40)
    for line in wrap_text(body, f_body, W - PAD * 2):
        draw.text((PAD, y), line, font=f_body, fill=GREY)
        y += 54
    y += 40

    # CTA pill button
    btn_text = '  Book a Call  ↗  '
    f_btn = font(700, 38)
    bbox = f_btn.getbbox(btn_text)
    btn_w = bbox[2] - bbox[0] + 48
    btn_h = 72
    btn_x = PAD
    btn_y = y

    # pill background
    draw.rounded_rectangle(
        [(btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h)],
        radius=36,
        fill=(40, 40, 40)
    )
    draw.text((btn_x + 24, btn_y + 16), btn_text, font=f_btn, fill=WHITE)

    save_slide(img, 9)


# ── build all slides ──────────────────────────────────────────────────────────
print('Building slides...')
slide_01()
slide_02()
slide_03()
slide_04()
slide_05()
slide_06()
slide_07()
slide_08()
slide_09()
print('All slides rendered.')

# ── build PDF ────────────────────────────────────────────────────────────────
print('Building PDF...')
files = sorted(glob.glob(f'{CLAUDE}/slide_*.png'))
first = Image.open(files[0])
pw, ph = first.size[0] * 0.75, first.size[1] * 0.75

pdf_path = f'{CLAUDE}/{TOPIC}_carousel.pdf'
c = rl_canvas.Canvas(pdf_path, pagesize=(pw, ph))
for f in files:
    c.drawImage(f, 0, 0, width=pw, height=ph)
    c.showPage()
c.save()
print(f'PDF saved: {pdf_path}')

# ── copy to outputs ───────────────────────────────────────────────────────────
import shutil, os
os.makedirs(OUT_DIR, exist_ok=True)

# clear old slide PNGs and PDFs
for old in glob.glob(f'{OUT_DIR}/slide_*.png') + glob.glob(f'{OUT_DIR}/*.pdf'):
    os.remove(old)

for f in files:
    shutil.copy(f, OUT_DIR)
shutil.copy(pdf_path, OUT_DIR)
print('Copied to outputs.')

# ── captions.md ───────────────────────────────────────────────────────────────
captions = """# Carousel Captions — AI Agents for SaaS Customer Success

## LinkedIn

Your gross retention dropped 4 points last year. Your CS team grew 40%. The math no longer works.

The problem is not effort. It is architecture.

The traditional CSM-against-book-size model breaks when 60-80% of your customers are in self-serve tiers no human will ever touch. Those accounts churn quietly, and they contribute 50-65% of net revenue churn.

AI agents in SaaS customer success are not a productivity play. They are a profit pool play.

A Series C B2B SaaS with 1,800 customers deployed an agentic CS layer and cut net revenue churn from 14.2% to 9.8% in nine months. Self-serve churn dropped from 22% to 12%. Gross retention climbed from 88% to 93%.

Then they added a Premium Success tier that wrapped the agent's reliability around a retention guarantee. 38% of mid-market and enterprise customers adopted it within six months. $4.2M net new ARR. $720K deployment cost.

Key takeaways:
- Agentic CS monitors 100% of your customer base, not just the top 30-40%
- Churn risk surfaces in under 24 hours, not at the next quarterly review
- Expansion signals humans miss get routed to the right AE at the right time
- Outcome reliability makes outcome-based pricing structurally viable
- Start with SMB and mid-market. Over-automation on enterprise kills relationships.

The agent fixes the architecture. Outcome-based pricing makes it pay back.

If you want to size the churn pickup and the pricing story for your customer mix, DM us or book a call below.

#AIAgents #SaaS #CustomerSuccess #ChurnReduction #B2BSaaS

---

## Instagram

Your CS team grew. Your retention still dropped. Here is why the old model broke.

AI agents for SaaS customer success are changing the math entirely. Swipe through →

The problem: 60-80% of your customers are in self-serve tiers no CSM will ever touch. They generate 50%+ of your churn.

A real deployment at a Series C B2B SaaS:
- 1,800 customers, $42M ARR
- Net revenue churn: 14.2% to 9.8%
- Self-serve churn: 22% to 12%
- New revenue stream: $4.2M ARR in 9 months

Save this post if you are thinking about agentic CS for your team.

#aiagents #saas #customersuccess #churnreduction #b2bsaas #artificialintelligence #startups #saasgrowth #retention #productledgrowth #csm #revops #ai #techstartup #growth #agentic #automation #customerretention #mrr #arr

---

## Twitter / X

**Single tweet:**
Your gross retention dropped. Your CS team grew 40%. The math broke.

AI agents cut SaaS net revenue churn 31% in 9 months and added $4.2M ARR via outcome-based pricing. Here is how it works. 🧵

**Thread version:**
1/ Your CS team cannot cover 60-80% of your customers. Those self-serve accounts churn at 22% vs. 9% for named accounts. That is the architecture problem.

2/ AI agents in SaaS customer success do pattern recognition across product telemetry, support history, and engagement signals. For every account. Simultaneously.

3/ A Series C B2B SaaS deployed this in 2025: 1,800 customers, $42M ARR. Net revenue churn dropped from 14.2% to 9.8% in nine months.

4/ Then they launched a Premium Success tier: $40K-$120K/year, outcome-based retention guarantees. 38% adoption among mid-market customers. $4.2M net new ARR.

5/ Cost to deploy: $720K. First-year return: $6.3M. The agent pays for itself in the first quarter.

6/ Key constraint: start with SMB, not enterprise. Over-automation on strategic accounts where the human relationship is the moat will backfire.

7/ The agent fixes the architecture. Outcome-based pricing makes it pay back. If you want to size the pickup for your customer mix, DM or visit codiste.com/book-a-call
"""

captions_path = f'{OUT_DIR}/{TOPIC}_captions.md'
with open(captions_path, 'w') as fp:
    fp.write(captions)
print(f'Captions saved: {captions_path}')
print('\nDone!')
