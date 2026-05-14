import base64
import asyncio
import os
import sys
import urllib.request
from pathlib import Path

REPO_DIR = Path('/home/user/linkedin_post_creation')
OUT_DIR = REPO_DIR / 'outputs' / 'hire_ai_agent_dev'
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOPIC = 'hire_ai_agent_dev'


# ── Font embedding ──────────────────────────────────────────────────────────

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

r400 = b64(REPO_DIR / 'Satoshi-Regular.otf')
r700 = b64(REPO_DIR / 'Satoshi-Bold.otf')
r900 = b64(REPO_DIR / 'Satoshi-Black.otf')

FONT_FACE = f"""
@font-face {{font-family:'Satoshi';font-weight:400;src:url('data:font/otf;base64,{r400}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:700;src:url('data:font/otf;base64,{r700}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:900;src:url('data:font/otf;base64,{r900}') format('opentype');}}
"""

# ── Logo embedding ──────────────────────────────────────────────────────────

LOGO_WHITE_B64 = b64(REPO_DIR / 'c_white_claude (2).png')
LOGO_BLACK_B64 = b64(REPO_DIR / 'c_black_claude (2).png')

LOGO_DARK  = f'<img src="data:image/png;base64,{LOGO_WHITE_B64}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'
LOGO_LIGHT = f'<img src="data:image/png;base64,{LOGO_BLACK_B64}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'

# ── Grid overlays ──────────────────────────────────────────────────────────

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

# ── Shared decoratives ─────────────────────────────────────────────────────

ASTERISK_DARK  = '<div style="position:absolute;top:30px;right:50px;font-size:280px;font-weight:900;color:#1a1a1a;line-height:1;z-index:1;font-family:Satoshi,sans-serif;">*</div>'
ASTERISK_LIGHT = '<div style="position:absolute;top:30px;right:50px;font-size:280px;font-weight:900;color:#efefef;line-height:1;z-index:1;font-family:Satoshi,sans-serif;">*</div>'
ARROW_DARK     = '<div style="position:absolute;bottom:60px;right:64px;font-size:48px;font-weight:400;color:#FAFAFA;z-index:5;">↗</div>'
ARROW_LIGHT    = '<div style="position:absolute;bottom:60px;right:64px;font-size:48px;font-weight:400;color:#010101;z-index:5;">→</div>'


def head(bg, grid_css):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{FONT_FACE}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1350px;overflow:hidden;}}
body{{font-family:'Satoshi',sans-serif;background:{bg};position:relative;}}
{grid_css}
</style></head><body>"""


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


# ── Template A — Cover with image (Slide 1, dark) ─────────────────────────

def slide1(img_b64=None):
    img_html = ''
    headline_top = '380px'
    if img_b64:
        img_html = f'''
<div style="position:absolute;top:230px;left:64px;right:64px;z-index:10;
            border-radius:20px;overflow:hidden;
            border:1px solid rgba(255,255,255,0.1);">
  <img src="data:image/png;base64,{img_b64}" style="width:100%;height:auto;display:block;" />
</div>'''
        headline_top = '790px'

    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>
{img_html}

<div style="position:absolute;top:{headline_top};left:64px;right:64px;z-index:5;">
  {label('AI AGENT HIRING')}
  <div style="margin-top:30px;font-size:90px;font-weight:900;color:#868686;line-height:1.05;letter-spacing:-2px;">340 applications.</div>
  <div style="font-size:90px;font-weight:900;color:#868686;line-height:1.05;letter-spacing:-2px;">Twelve shipped.</div>
  <div style="font-size:90px;font-weight:900;color:#FAFAFA;line-height:1.05;letter-spacing:-2px;">Three can build.</div>
</div>

{ARROW_DARK}
</body></html>
"""


# ── Template L — Definition (Slide 2, light) ──────────────────────────────

def slide2():
    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
{ASTERISK_LIGHT}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('DEFINITION')}
</div>

<div style="position:absolute;top:360px;left:64px;right:64px;z-index:5;">
  <div style="font-size:100px;font-weight:900;color:#010101;line-height:1;letter-spacing:-3px;">Production<br>Agent Dev</div>
  <div style="margin-top:14px;font-size:32px;font-weight:400;color:#868686;font-style:italic;">noun, software engineering</div>
</div>

<div style="position:absolute;top:760px;left:64px;right:64px;z-index:5;">
  <div style="height:1px;background:#dadada;margin-bottom:40px;"></div>
  <div style="font-size:42px;font-weight:400;color:#010101;line-height:1.4;">Someone who has shipped a stateful, multi-tenant agent to production and operated it under failure conditions. Not just a demo builder.</div>
</div>

{ARROW_LIGHT}
</body></html>
"""


# ── Template K — Question (Slide 3, dark) ────────────────────────────────

def slide3():
    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
<div class="grid"></div>

<div style="position:absolute;top:80px;right:60px;font-size:520px;font-weight:900;color:#1a1a1a;line-height:1;font-family:Satoshi,sans-serif;z-index:1;">?</div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('THE REAL QUESTION')}
</div>

<div style="position:absolute;top:460px;left:64px;right:540px;z-index:5;">
  <div style="font-size:88px;font-weight:900;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;">Can they explain a state transition boundary failure?</div>
</div>

{ARROW_DARK}
</body></html>
"""


# ── Template I — Comparison Table (Slide 4, light) ────────────────────────

def slide4():
    fg = '#010101'
    divider = '#dadada'

    def col(title, items, title_color):
        rows = ''.join(
            f'<div style="font-size:30px;font-weight:400;color:{fg};line-height:1.4;padding:16px 0;border-bottom:1px solid {divider};">{x}</div>'
            for x in items
        )
        return f"""
<div style="flex:1;">
  <div style="font-size:34px;font-weight:900;color:{title_color};margin-bottom:22px;letter-spacing:-1px;">{title}</div>
  {rows}
</div>
"""

    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
{ASTERISK_LIGHT}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('SKILLS THAT MATTER')}
  <div style="margin-top:28px;font-size:72px;font-weight:900;color:#010101;line-height:1.1;letter-spacing:-2px;">Demo builder vs.<br>production engineer</div>
</div>

<div style="position:absolute;top:600px;left:64px;right:64px;z-index:5;display:flex;gap:48px;">
  {col('Demo Builder', ['Ran LangChain tutorials', 'Used vector DB as black box', 'Checks outputs manually', 'Single-user test environment'], '#868686')}
  <div style="width:1px;background:{divider};"></div>
  {col('Production Engineer', ['Designed LangGraph state graphs', 'Chunking + embedding + re-ranking', 'Trajectory-based eval framework', 'Multi-tenant memory isolation'], '#010101')}
</div>

{ARROW_LIGHT}
</body></html>
"""


# ── Template J — Step Cards (Slide 5, dark) ──────────────────────────────

def slide5():
    steps = [
        ('Memory architecture', 'Describe the last agent you shipped. What was in working memory vs long-term?'),
        ('API failure modes', 'Walk through your orchestration failures. What happens on the third retry?'),
        ('Eval methodology', 'How do you eval? What does a regression look like and how fast do you catch it?'),
    ]
    cards = ''
    for i, (title, body) in enumerate(steps, 1):
        cards += f"""
<div style="margin-bottom:36px;display:flex;gap:32px;align-items:flex-start;">
  <div style="font-size:72px;font-weight:900;color:#868686;line-height:1;letter-spacing:-2px;min-width:90px;">0{i}</div>
  <div style="flex:1;">
    <div style="font-size:38px;font-weight:700;color:#FAFAFA;line-height:1.2;margin-bottom:8px;">{title}</div>
    <div style="font-size:28px;font-weight:400;color:#868686;line-height:1.35;">{body}</div>
  </div>
</div>
"""

    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('INTERVIEW FRAMEWORK')}
  <div style="margin-top:28px;font-size:72px;font-weight:900;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;">3 questions that reveal real experience</div>
</div>

<div style="position:absolute;top:570px;left:64px;right:64px;z-index:5;">
  {cards}
</div>

{ARROW_DARK}
</body></html>
"""


# ── Template G — Stat (Slide 6, light) ───────────────────────────────────

def slide6():
    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
{ASTERISK_LIGHT}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('HIRING REALITY')}
</div>

<div style="position:absolute;top:380px;left:64px;right:64px;z-index:5;">
  <div style="font-size:260px;font-weight:900;color:#010101;line-height:1;letter-spacing:-8px;">8-14</div>
</div>

<div style="position:absolute;top:860px;left:64px;right:64px;z-index:5;">
  <div style="font-size:46px;font-weight:700;color:#010101;line-height:1.2;margin-bottom:12px;">weeks to hire a qualified<br>AI agent developer.</div>
  <div style="font-size:34px;font-weight:400;color:#868686;line-height:1.3;">The combination of LangGraph, multi-tenant experience, and eval competency is rare.</div>
</div>

{ARROW_LIGHT}
</body></html>
"""


# ── Template M — Framework (Slide 7, dark) ───────────────────────────────

def slide7():
    nodes = [
        'AI Agent Dev: orchestration, memory, evals',
        'Backend Engineer: APIs, infrastructure, scaling',
        'Product Engineer: UI surface, telemetry, UX',
    ]
    boxes = ''
    for i, node in enumerate(nodes):
        boxes += f"""
<div style="background:#151515;border:1px solid #333;border-radius:16px;padding:36px;margin-bottom:16px;display:flex;align-items:center;gap:24px;">
  <div style="width:48px;height:48px;border-radius:50%;background:#868686;color:#010101;font-size:28px;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{i+1}</div>
  <div style="font-size:38px;font-weight:700;color:#FAFAFA;line-height:1.2;">{node}</div>
</div>
"""
        if i < len(nodes) - 1:
            boxes += '<div style="text-align:center;font-size:32px;color:#868686;line-height:1;margin:-4px 0 12px 0;">↓</div>'

    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('TEAM SHAPE')}
  <div style="margin-top:28px;font-size:72px;font-weight:900;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;">3 roles every production agent needs</div>
</div>

<div style="position:absolute;top:540px;left:64px;right:64px;z-index:5;">
  {boxes}
</div>

{ARROW_DARK}
</body></html>
"""


# ── Template O — Checklist (Slide 8, light) ──────────────────────────────

def slide8():
    items = [
        ('LangGraph state management', True),
        ('Semantic memory architecture', True),
        ('API orchestration under failure', True),
        ('Agent evaluation frameworks', True),
    ]
    fg = '#010101'
    bg = '#FAFAFA'
    rows = ''
    for text, checked in items:
        box = (
            f'<div style="width:36px;height:36px;border-radius:6px;background:{fg};display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:10px;"><div style="font-size:22px;font-weight:900;color:{bg};line-height:1;">&#10003;</div></div>'
            if checked else
            f'<div style="width:36px;height:36px;border-radius:6px;border:2px solid #868686;flex-shrink:0;margin-top:10px;"></div>'
        )
        rows += f"""
<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:36px;">
  {box}
  <div style="font-size:46px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>
"""

    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
{ASTERISK_LIGHT}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('4 CORE COMPETENCIES')}
  <div style="margin-top:28px;font-size:72px;font-weight:900;color:#010101;line-height:1.1;letter-spacing:-2px;">Does your candidate have all four?</div>
</div>

<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;">
  {rows}
</div>

{ARROW_LIGHT}
</body></html>
"""


# ── Template F — CTA Close (Slide 9, dark) ───────────────────────────────

def slide9():
    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label('BUILD WITH CODISTE')}
</div>

<div style="position:absolute;top:380px;left:64px;right:64px;z-index:5;">
  <div style="font-size:96px;font-weight:900;color:#868686;line-height:1.05;letter-spacing:-2px;">Your agent team,</div>
  <div style="font-size:96px;font-weight:900;color:#FAFAFA;line-height:1.05;letter-spacing:-2px;">ready to ship.</div>
</div>

<div style="position:absolute;top:800px;left:64px;right:64px;z-index:5;">
  <div style="font-size:38px;font-weight:400;color:#868686;line-height:1.4;margin-bottom:60px;">We embed as your technical build partner for production SaaS agents. You own the product.</div>
  <a style="display:inline-flex;align-items:center;gap:16px;background:linear-gradient(135deg,#222,#383838);border:1px solid #444;border-radius:60px;padding:24px 48px;text-decoration:none;">
    <span style="font-size:38px;font-weight:700;color:#FAFAFA;letter-spacing:-0.5px;">Book a Technical Call</span>
    <span style="font-size:38px;color:#FAFAFA;">↗</span>
  </a>
  <div style="margin-top:28px;font-size:30px;font-weight:400;color:#868686;">codiste.com/book-a-call</div>
</div>

</body></html>
"""


# ── Write all HTML files ──────────────────────────────────────────────────

def write_slides(cover_img_b64=None):
    slides = {
        1: slide1(cover_img_b64),
        2: slide2(),
        3: slide3(),
        4: slide4(),
        5: slide5(),
        6: slide6(),
        7: slide7(),
        8: slide8(),
        9: slide9(),
    }
    for n, html in slides.items():
        path = OUT_DIR / f'{TOPIC}_slide_{n:02d}.html'
        path.write_text(html, encoding='utf-8')
        print(f'  wrote {path.name}')
    return slides


# ── Render PNGs with Playwright ───────────────────────────────────────────

async def render():
    from playwright.async_api import async_playwright
    chromium_exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=chromium_exe)
        for i in range(1, 10):
            html_path = OUT_DIR / f'{TOPIC}_slide_{i:02d}.html'
            png_path  = OUT_DIR / f'{TOPIC}_slide_{i:02d}.png'
            page = await browser.new_page(viewport={'width': 1080, 'height': 1350})
            await page.goto(f'file://{html_path}')
            await page.wait_for_timeout(1200)
            await page.screenshot(path=str(png_path), full_page=False, type='png')
            print(f'  rendered {png_path.name}')
        await browser.close()


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    cover_b64 = None
    cover_path = OUT_DIR / 'cover_generated.png'
    if cover_path.exists():
        print('Loading cover image...')
        cover_b64 = b64(cover_path)

    print('Writing HTML slides...')
    write_slides(cover_b64)

    print('Rendering PNGs...')
    asyncio.run(render())

    print('Done. PNGs saved to:', OUT_DIR)


if __name__ == '__main__':
    main()
