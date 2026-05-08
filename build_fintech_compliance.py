import base64, asyncio
from pathlib import Path

REPO = Path('/home/user/linkedin_post_creation')
OUT  = REPO / 'outputs'
OUT.mkdir(exist_ok=True)

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Fonts
r400 = b64(REPO / 'Satoshi-Regular.otf')
r700 = b64(REPO / 'Satoshi-Bold.otf')
r900 = b64(REPO / 'Satoshi-Black.otf')

FONT_FACE = f"""
@font-face {{font-family:'Satoshi';font-weight:400;src:url('data:font/otf;base64,{r400}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:700;src:url('data:font/otf;base64,{r700}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:900;src:url('data:font/otf;base64,{r900}') format('opentype');}}
"""

# Logos (white = for dark BG, black = for light BG)
LOGO_WHITE_B64 = b64(REPO / 'c_white_claude (2).png')
LOGO_BLACK_B64 = b64(REPO / 'c_black_claude (2).png')

LOGO_DARK  = f'<img src="data:image/png;base64,{LOGO_WHITE_B64}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'
LOGO_LIGHT = f'<img src="data:image/png;base64,{LOGO_BLACK_B64}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'

GRID_DARK = """
.grid{position:absolute;inset:0;pointer-events:none;z-index:1;
background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),
linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);
background-size:54px 54px;}
"""
GRID_LIGHT = """
.grid{position:absolute;inset:0;pointer-events:none;z-index:1;
background-image:linear-gradient(rgba(0,0,0,0.04) 1px,transparent 1px),
linear-gradient(90deg,rgba(0,0,0,0.04) 1px,transparent 1px);
background-size:54px 54px;}
"""

def head(bg, grid_css):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{FONT_FACE}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1350px;overflow:hidden;}}
body{{font-family:'Satoshi',sans-serif;background:{bg};position:relative;}}
{grid_css}
</style></head><body>"""

ASTERISK_DARK  = '<div style="position:absolute;top:30px;right:50px;font-size:280px;font-weight:900;color:#1a1a1a;line-height:1;z-index:1;font-family:Satoshi,sans-serif;">*</div>'
ASTERISK_LIGHT = '<div style="position:absolute;top:30px;right:50px;font-size:280px;font-weight:900;color:#efefef;line-height:1;z-index:1;font-family:Satoshi,sans-serif;">*</div>'

ARROW_DARK  = '<div style="position:absolute;bottom:60px;right:64px;font-size:48px;font-weight:400;color:#FAFAFA;z-index:5;">&#8599;</div>'
ARROW_LIGHT = '<div style="position:absolute;bottom:60px;right:64px;font-size:48px;font-weight:400;color:#010101;z-index:5;">&#8594;</div>'

def label(txt):
    return f'<div style="font-size:28px;font-weight:700;color:#868686;letter-spacing:3px;text-transform:uppercase;">{txt}</div>'

def bullet(text, dark=False):
    fg = '#FAFAFA' if dark else '#010101'
    return f"""
<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:34px;">
  <div style="width:8px;height:8px;border-radius:50%;background:#868686;flex-shrink:0;margin-top:22px;"></div>
  <div style="font-size:44px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>
"""

# ── Template A: Bold Statement / Cover ──────────────────────────────────────
def cover_slide(label_text, grey1, grey2, white_punch):
    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:420px;left:64px;right:64px;z-index:5;">
  <div style="font-size:92px;font-weight:900;color:#868686;line-height:1.08;letter-spacing:-2px;">{grey1}</div>
  <div style="font-size:92px;font-weight:900;color:#868686;line-height:1.08;letter-spacing:-2px;">{grey2}</div>
  <div style="font-size:92px;font-weight:900;color:#FAFAFA;line-height:1.08;letter-spacing:-2px;">{white_punch}</div>
</div>
{ARROW_DARK}
</body></html>
"""

# ── Template G: Stat ─────────────────────────────────────────────────────────
def stat_slide(label_text, big_number, supporting_line, dark=False):
    bg    = '#010101' if dark else '#FAFAFA'
    fg    = '#FAFAFA' if dark else '#010101'
    grid  = GRID_DARK if dark else GRID_LIGHT
    logo  = LOGO_DARK if dark else LOGO_LIGHT
    ast   = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid) + f"""
{logo}
{ast}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:420px;left:64px;right:64px;z-index:5;">
  <div style="font-size:280px;font-weight:900;color:{fg};line-height:1;letter-spacing:-8px;">{big_number}</div>
</div>
<div style="position:absolute;top:860px;left:64px;right:64px;z-index:5;">
  <div style="font-size:48px;font-weight:400;color:#868686;line-height:1.3;max-width:880px;">{supporting_line}</div>
</div>
{arrow}
</body></html>
"""

# ── Template K: Question ─────────────────────────────────────────────────────
def question_slide(label_text, question_text, dark=True):
    bg    = '#010101' if dark else '#FAFAFA'
    fg    = '#FAFAFA' if dark else '#010101'
    mc    = '#1a1a1a' if dark else '#efefef'
    grid  = GRID_DARK if dark else GRID_LIGHT
    logo  = LOGO_DARK if dark else LOGO_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid) + f"""
{logo}
<div class="grid"></div>
<div style="position:absolute;top:80px;right:60px;font-size:520px;font-weight:900;color:{mc};line-height:1;font-family:Satoshi,sans-serif;z-index:1;">?</div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:500px;left:64px;right:64px;z-index:5;">
  <div style="font-size:86px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{question_text}</div>
</div>
{arrow}
</body></html>
"""

# ── Template I: Comparison Table ─────────────────────────────────────────────
def comparison_slide(label_text, headline, left_title, left_items, right_title, right_items, dark=False):
    bg      = '#010101' if dark else '#FAFAFA'
    fg      = '#FAFAFA' if dark else '#010101'
    divider = '#333' if dark else '#dadada'
    grid    = GRID_DARK if dark else GRID_LIGHT
    logo    = LOGO_DARK if dark else LOGO_LIGHT
    ast     = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow   = ARROW_DARK if dark else ARROW_LIGHT

    def col(title, items):
        rows = ''.join(
            f'<div style="font-size:30px;font-weight:400;color:{fg};line-height:1.4;padding:16px 0;border-bottom:1px solid {divider};">{x}</div>'
            for x in items
        )
        return f"""
<div style="flex:1;">
  <div style="font-size:34px;font-weight:900;color:{fg};margin-bottom:24px;letter-spacing:-1px;">{title}</div>
  {rows}
</div>
"""
    return head(bg, grid) + f"""
{logo}
{ast}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:24px;font-size:68px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:540px;left:64px;right:64px;z-index:5;display:flex;gap:60px;">
  {col(left_title, left_items)}
  <div style="width:1px;background:{divider};"></div>
  {col(right_title, right_items)}
</div>
{arrow}
</body></html>
"""

# ── Template J: Step Cards ────────────────────────────────────────────────────
def step_slide(label_text, headline, steps, dark=False):
    bg    = '#010101' if dark else '#FAFAFA'
    fg    = '#FAFAFA' if dark else '#010101'
    nc    = '#868686'
    grid  = GRID_DARK if dark else GRID_LIGHT
    logo  = LOGO_DARK if dark else LOGO_LIGHT
    ast   = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    cards = ''
    for i, (title, body) in enumerate(steps, 1):
        cards += f"""
<div style="margin-bottom:36px;display:flex;gap:32px;align-items:flex-start;">
  <div style="font-size:72px;font-weight:900;color:{nc};line-height:1;letter-spacing:-2px;min-width:90px;">0{i}</div>
  <div style="flex:1;">
    <div style="font-size:38px;font-weight:700;color:{fg};line-height:1.2;margin-bottom:6px;">{title}</div>
    <div style="font-size:28px;font-weight:400;color:#868686;line-height:1.35;">{body}</div>
  </div>
</div>
"""
    return head(bg, grid) + f"""
{logo}
{ast}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:24px;font-size:68px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:520px;left:64px;right:64px;z-index:5;">
  {cards}
</div>
{arrow}
</body></html>
"""

# ── Template N: Before/After Split ───────────────────────────────────────────
def split_slide(label_text, headline, before_label, before_items, after_label, after_items):
    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:24px;font-size:68px;font-weight:900;color:#010101;line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:540px;left:64px;right:64px;bottom:100px;z-index:5;display:flex;gap:0;">
  <div style="flex:1;background:#010101;padding:44px 36px;border-radius:20px 0 0 20px;">
    <div style="font-size:22px;font-weight:700;color:#868686;letter-spacing:3px;text-transform:uppercase;margin-bottom:28px;">{before_label}</div>
    {''.join(f'<div style="font-size:32px;font-weight:400;color:#FAFAFA;line-height:1.35;margin-bottom:18px;">{x}</div>' for x in before_items)}
  </div>
  <div style="flex:1;background:#010101;padding:44px 36px;border-radius:0 20px 20px 0;border-left:1px solid #333;">
    <div style="font-size:22px;font-weight:700;color:#FAFAFA;letter-spacing:3px;text-transform:uppercase;margin-bottom:28px;">{after_label}</div>
    {''.join(f'<div style="font-size:32px;font-weight:400;color:#FAFAFA;line-height:1.35;margin-bottom:18px;">{x}</div>' for x in after_items)}
  </div>
</div>
{ARROW_LIGHT}
</body></html>
"""

# ── Template O: Checklist ─────────────────────────────────────────────────────
def checklist_slide(label_text, headline, items, dark=False):
    bg    = '#010101' if dark else '#FAFAFA'
    fg    = '#FAFAFA' if dark else '#010101'
    grid  = GRID_DARK if dark else GRID_LIGHT
    logo  = LOGO_DARK if dark else LOGO_LIGHT
    ast   = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    rows  = ''
    for text, checked in items:
        if checked:
            box = f'<div style="width:36px;height:36px;border-radius:6px;background:{fg};display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:8px;"><div style="font-size:22px;font-weight:900;color:{bg};line-height:1;">&#10003;</div></div>'
        else:
            box = f'<div style="width:36px;height:36px;border-radius:6px;border:2px solid #868686;flex-shrink:0;margin-top:8px;"></div>'
        rows += f"""
<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:28px;">
  {box}
  <div style="font-size:40px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>
"""
    return head(bg, grid) + f"""
{logo}
{ast}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:24px;font-size:68px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:520px;left:64px;right:64px;z-index:5;">
  {rows}
</div>
{arrow}
</body></html>
"""

# ── Template F: CTA Close ─────────────────────────────────────────────────────
def cta_slide(label_text, headline, sub, cta_text):
    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:380px;left:64px;right:64px;z-index:5;">
  <div style="font-size:88px;font-weight:900;color:#FAFAFA;line-height:1.08;letter-spacing:-2px;">{headline}</div>
  <div style="margin-top:32px;font-size:44px;font-weight:400;color:#868686;line-height:1.4;max-width:840px;">{sub}</div>
</div>
<div style="position:absolute;bottom:140px;left:64px;z-index:5;">
  <div style="display:inline-flex;align-items:center;gap:16px;background:linear-gradient(135deg,#222,#383838);border-radius:60px;padding:24px 52px;">
    <span style="font-size:36px;font-weight:700;color:#FAFAFA;letter-spacing:-0.5px;">{cta_text}</span>
    <span style="font-size:32px;color:#FAFAFA;">&#8599;</span>
  </div>
</div>
{ARROW_DARK}
</body></html>
"""

# ── Build all 9 slides ────────────────────────────────────────────────────────
SLIDES_DIR = OUT / 'ai_agents_fintech'
SLIDES_DIR.mkdir(exist_ok=True)

slides = [
    # Slide 1: Cover (A, dark)
    cover_slide(
        'FINTECH COMPLIANCE',
        'AI cut compliance',
        'false positives',
        'by 64%.'
    ),
    # Slide 2: Stat (G, light)
    stat_slide(
        'FALSE POSITIVE REDUCTION',
        '64%',
        'Achieved in a live US fintech deployment over 6 months, reasoning across full transaction context.',
        dark=False
    ),
    # Slide 3: Question (K, dark)
    question_slide(
        'THE REAL PROBLEM',
        'Why do your analysts spend 97% of their time clearing noise?',
        dark=True
    ),
    # Slide 4: Comparison Table (I, light)
    comparison_slide(
        'THE SHIFT',
        'Rules vs reasoning',
        'Rule engine',
        [
            'Matches single events to fixed rules',
            '96-98% false positive rate',
            'Manual rule updates take weeks',
            'Analysts buried in alert queues',
        ],
        'Agentic AI',
        [
            'Reasons across history and context',
            '65-75% false positive rate',
            'Adapts continuously with feedback',
            'Analysts focus on real signal',
        ],
        dark=False
    ),
    # Slide 5: Step Cards (J, dark)
    step_slide(
        'HOW IT WORKS',
        'The agentic compliance layer',
        [
            ('Alert fires', 'Rules engine flags a transaction as usual.'),
            ('Agent reasons', 'Reads history, KYC profile, and peer signals. Clears or escalates with confidence score.'),
            ('Analyst decides', 'Reviews only escalated cases with full context pre-assembled.'),
        ],
        dark=True
    ),
    # Slide 6: Before/After Split (N)
    split_slide(
        'THE RESULT',
        'Workload transformed',
        'BEFORE',
        ['2,170 analyst hours/month', '97.6% false positive rate', '31,000 alerts cleared manually'],
        'AFTER',
        ['522 analyst hours/month', '72.4% false positive rate', '64% of alerts auto-cleared'],
    ),
    # Slide 7: Stat (G, dark)
    stat_slide(
        'YEAR-ONE ROI',
        '7mo',
        'Payback period. $890K deployment cost against $1.4M in year-one labor savings.',
        dark=True
    ),
    # Slide 8: Checklist (O, light)
    checklist_slide(
        'DEPLOYMENT RULES',
        'What makes it work',
        [
            ('Layer AI over existing rules, do not replace them', True),
            ('Embed compliance team from week one', True),
            ('Build reasoning traces as first-class deliverables', True),
            ('Design reviewer escalation before launch', True),
            ('Audit infrastructure ships with the agent', True),
        ],
        dark=False
    ),
    # Slide 9: CTA (F, dark)
    cta_slide(
        'CODISTE',
        'Ready to cut your compliance costs?',
        'We scope and ship agentic compliance layers for US fintechs. Payback inside year one.',
        'Book a call'
    ),
]

# Write HTML files
for i, html in enumerate(slides, 1):
    path = SLIDES_DIR / f'slide_{i:02d}.html'
    path.write_text(html, encoding='utf-8')
    print(f'Wrote {path}')

print('All HTML files written.')

# Render PNGs
async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
        )
        for i in range(1, 10):
            page = await browser.new_page(viewport={'width': 1080, 'height': 1350})
            html_path = SLIDES_DIR / f'slide_{i:02d}.html'
            await page.goto(f'file://{html_path}')
            await page.wait_for_timeout(1500)
            out_path = SLIDES_DIR / f'slide_{i:02d}.png'
            await page.screenshot(path=str(out_path), full_page=False, type='png')
            print(f'Rendered {out_path}')
        await browser.close()

asyncio.run(render())
print('All slides rendered.')
