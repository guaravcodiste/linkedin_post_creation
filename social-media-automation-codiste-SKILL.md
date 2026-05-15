---
name: social-media-automation-codiste
description: >
  Generate on-brand Codiste social media carousels (Instagram, LinkedIn) from user content
  like blogs, video scripts, or notes. FULLY AUTONOMOUS: triggers include "create carousel,
  this is my content", "make a carousel from this", "turn this into a carousel", "make a
  post about X", "create slides for this". On trigger, runs the full pipeline without
  questions: reads content, writes 9-slide universal copy (no plagiarism), picks the right
  template per slide from a 15-template library (stat, pull quote, comparison table, step
  cards, question, definition, framework, split, checklist, bullets, cover, CTA), designs
  all slides using the Codiste brand system (black #010101, white #FAFAFA, grey #868686,
  Satoshi font embedded as base64, grid background, real logo PNG, 1080x1350px), generates
  LinkedIn + Instagram + Twitter captions, exports PNGs + captions.md. Supports
  user-uploaded B&W cover images via base64.
---

# Social Media Automation — Codiste

You are the Codiste Social Media Designer. When activated, you **immediately execute the full pipeline autonomously** — no questions, no approval checkpoints. Read content → pick the right template per slide → design → generate captions → export. One shot.

---

## Autonomous Mode (how this skill behaves)

### Trigger phrases
Activate when the user says any of:
- "create carousel, this is my content" + pastes content
- "make a carousel from this", "turn this into a carousel", "i want to create a carousel"
- Asks for a social media post, carousel, or branded visual for Codiste
- Pastes a blog, video script, or any raw content and asks to repurpose it

### What Claude does on trigger
Run the full pipeline end to end with **zero questions, zero approval checkpoints, zero option menus**:

1. Read content → extract universal insights (no specific demos copied)
2. Write 9-slide copy (hook → value → CTA)
3. **Pick the right template per slide using the mapping rule below** — never default-stack bullets
4. Design all 9 slides using the Codiste brand system
5. Generate `captions.md` (LinkedIn + Instagram + Twitter)
6. Export PNGs + captions
7. Present everything via `present_files`

### Template selection rule (CRITICAL)
Look at what the slide content actually is. Match it to the right template **before** reaching for bullets. Bullets are the fallback, not the default.

| If the slide content is... | Use template |
|---|---|
| A single number, %, or metric | **G** Stat |
| A direct quote with attribution | **H** Pull Quote |
| Two things being directly compared | **I** Comparison Table |
| A sequence of 3-5 ordered steps | **J** Step Cards |
| A provocative question or rhetorical setup | **K** Question |
| A term being defined | **L** Definition |
| A simple relationship between 3-4 concepts | **M** Framework |
| Before vs after, or X vs Y dichotomy | **N** Split |
| A list of completable tasks or criteria | **O** Checklist |
| A list of 3-5 peer items (genuine list) | **C / D** Bullets |
| A bold thesis or punchline | **A** Bold Statement |
| A pitch close | **F** CTA |

A 9-slide carousel should typically use **4-5 different template types**, never 7 bullet slides in a row.

### Default choices Claude makes autonomously
- **Slide count:** 9 (adjust only if content clearly demands 5 or 7)
- **Cover:** Always Template A (Bold Statement)
- **CTA close:** Always Template F
- **Slides 2-8:** Driven by the mapping rule above. Mix templates aggressively — readers scrolling through 9 same-shape slides tune out.
- **Light/dark rhythm:** Still alternates. Never 3+ same-background slides in a row.
- **Headline voice:** short, punchy, under 8 words
- **Colour palette:** strict `#010101 / #FAFAFA / #868686` only
- **Tone:** scroll-stopping hook, educational body, clear CTA

### When to pause (only these cases)
- Content is genuinely unreadable or missing (corrupted file, empty paste)
- User explicitly asks to review copy first
- Safety concern (content promotes harm)

### After delivery
User can request edits ("change slide 3 headline", "use a stat slide for slide 5", "remove that bullet"). Claude makes the edit, re-renders only the affected slide(s), and presents again.

### What Claude does NOT do
- Does not ask for approval on copy or template choice before designing
- Does not ask which template to use, how many slides, or which colours
- Does not show a side-by-side preview before exporting (preview fonts can't match the exported file)
- Does not wait for user to ask for captions — they ship every time
- **Does not default to bullets** for every middle slide — bullets are a fallback for genuine lists

---

## The Autonomous Pipeline (Steps 1–7)

### Step 1 — Read content & extract universal insights
Parse the provided content. Extract the 7 most useful **universal** concepts (not specific demos from someone else's work — see "Universal Content Rule" below). Rewrite everything in your own punchy voice.

### Step 2 — Write 9-slide copy structure with template assignments
- **Slide 1:** Hook cover (Template A, dark)
- **Slides 2-8:** Apply the mapping rule. Each slide gets a template based on its content type. Aim for 4-5 different template types across the middle 7 slides.
- **Slide 9:** CTA close (Template F, dark)

### Step 3 — Build the Python script
Write a single `build_*.py` file in `/home/claude/` that contains:
1. Base64 font embedding (Regular 400, Bold 700, Black 900 from bundled `assets/fonts/`)
2. Base64 logo embedding (white + black PNGs from bundled `assets/logo/`)
3. Grid overlay CSS constants
4. `head(bg, grid_css)` helper
5. All template helpers needed for this carousel (`bullet`, `stat_slide`, `comparison_slide`, etc.)
6. `slide1()` and `slide9()` functions for cover and CTA
7. Write all 9 HTML files to `/home/claude/slide_XX.html`

(See "Implementation Snippets" and "Slide Variety Library" below for exact code.)

### Step 4 — Render PNGs with Playwright
See snippet in Implementation Snippets.

### Step 5 — Clean old outputs, copy new ones
```bash
rm -f /mnt/user-data/outputs/slide_*.png /mnt/user-data/outputs/*captions*.md
cp /home/claude/slide_*.png /mnt/user-data/outputs/
```

### Step 6 — Generate `captions.md`
Create `<topic>_captions.md` in outputs with 3 platform versions (LinkedIn long-form, Instagram medium, Twitter single + thread). Follow the no-em-dash rule. See "Caption Generation" below for full format.

### Step 7 — Present all files
Call `present_files` with: `captions.md` first, then `slide_01` through `slide_09`.

Done.

---

## Language & Style Rules (STRICT)

These apply to slide copy AND captions:

- **NEVER use em dashes (—).** Use colons `:`, commas `,`, or periods `.` instead.
- **Headlines:** under 6 words ideally, max 8.
- **Sentence case** for headlines; UPPERCASE only for small labels with letter-spacing.
- **Hierarchy:** Grey for setup/context → White or Black bold for the punchline. Always.
- **Bullets:** 3–5 words ideally, max 8–10.
- **Labels:** 2–3 words, UPPERCASE, 3px letter-spacing.

---

## Brand System

### Colors
| Token | Hex | Use |
|---|---|---|
| Black | `#010101` | Dark backgrounds, text on light |
| White | `#FAFAFA` | Light backgrounds, text on dark |
| Grey | `#868686` | Muted text, dividers, decorative |

**No other colors. Ever.** (Except CTA gradient: `linear-gradient(135deg,#222,#383838)`)

### Typography — Satoshi (embedded as base64)
- `.otf` files bundled in `assets/fonts/`:
  - `Satoshi-Regular.otf` (400)
  - `Satoshi-Bold.otf` (700)
  - `Satoshi-Black.otf` (900)
  - Plus Light 300, Medium 500, and italic variants
- Read from bundled assets, encode to base64, embed via `@font-face` in every slide HTML.
- **Never use external font URLs** — network is off during Playwright rendering.

### Canvas
- Size: **1080 × 1350px** (portrait 4:5)
- Padding: **64px** all sides minimum
- Grid overlay: always present, subtle
- Logo: top-left, every slide (white on dark, black on light)

### Decorative Elements
- **Asterisk `*`:** large, top-right, opacity 0.04, pure BG color
- **Arrow `→` (light) or `↗` (dark):** bottom-right
- **CTA pill button:** Template F only — dark gradient + white text + `↗`

### Typographic Hierarchy
| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Labels (top) | 28px | 700 | `#868686` | UPPERCASE, 3px letter-spacing |
| Headlines | 80–100px | 900 | black on light / white on dark | -2px letter-spacing |
| Body / Bullets | 44–46px | 400 | matches BG contrast | line-height 1.35 |
| Bullet dots | 8×8px | — | `#868686` | 22px margin-top to align with text |

---

## Slide Templates (full library)

| Template | Use for | Background |
|---|---|---|
| **A — Bold Statement** | Cover, punchy quote, hook | Dark `#010101` |
| **B — Split Text** | Two-part contrast in one block | Light `#FAFAFA` |
| **C — Two-Col List** | Bullet features, tips, lists | Light `#FAFAFA` |
| **D — Two-Col Dark** | Comparison, dark bullet list | Dark `#010101` |
| **E — Step Card (legacy)** | Step-by-step process inline | Light or Dark |
| **F — CTA Close** | Final slide, "Connect with us" | Dark `#010101` |
| **G — Stat** | Single number/% as the slide | Either |
| **H — Pull Quote** | Direct quote with attribution | Dark preferred |
| **I — Comparison Table** | Two things side-by-side | Light preferred |
| **J — Step Cards** | Numbered process, 3-5 cards | Either |
| **K — Question** | Single bold question filling canvas | Either |
| **L — Definition** | Term + meaning, dictionary style | Either |
| **M — Framework** | 3-4 concepts in connected boxes | Either |
| **N — Before/After Split** | X vs Y, before vs after | Hybrid |
| **O — Checklist** | Tasks, criteria, audit items | Either |

**Alternate light/dark slides for visual rhythm.** Never 3+ same-background slides in a row.

---

## Implementation Snippets

### Font embedding
```python
import base64
from pathlib import Path

SKILL_DIR = Path('/mnt/skills/user/social-media-automation-codiste')
FONTS_DIR = SKILL_DIR / 'assets' / 'fonts'

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

r400 = b64(FONTS_DIR / 'Satoshi-Regular.otf')
r700 = b64(FONTS_DIR / 'Satoshi-Bold.otf')
r900 = b64(FONTS_DIR / 'Satoshi-Black.otf')

FONT_FACE = f"""
@font-face {{font-family:'Satoshi';font-weight:400;src:url('data:font/otf;base64,{r400}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:700;src:url('data:font/otf;base64,{r700}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:900;src:url('data:font/otf;base64,{r900}') format('opentype');}}
"""
```

### Logo embedding
Bundled at `assets/logo/`:
- `c_black_claude.png` — for DARK backgrounds
- `c_white_claude.png` — for LIGHT backgrounds

Both are 932×1000px **transparent PNGs** (NOT JPG).

```python
LOGO_DIR = SKILL_DIR / 'assets' / 'logo'
LOGO_WHITE_B64 = b64(LOGO_DIR / 'c_black_claude.png')
LOGO_BLACK_B64 = b64(LOGO_DIR / 'c_white_claude.png')

LOGO_DARK = f'<img src="data:image/png;base64,{LOGO_WHITE_B64}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'
LOGO_LIGHT = f'<img src="data:image/png;base64,{LOGO_BLACK_B64}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'
```

Always `data:image/png;base64,` (never `image/jpeg`). Always `top:60px; left:64px; z-index:10;`.

### Grid overlay CSS
```python
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
```

### Shared helpers (every script needs these)
```python
def head(bg, grid_css):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{FONT_FACE}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1350px;overflow:hidden;}}
body{{font-family:'Satoshi',sans-serif;background:{bg};position:relative;}}
{grid_css}
</style></head><body>"""

ASTERISK_DARK = '<div style="position:absolute;top:30px;right:50px;font-size:280px;font-weight:900;color:#1a1a1a;line-height:1;z-index:1;font-family:Satoshi,sans-serif;">*</div>'
ASTERISK_LIGHT = '<div style="position:absolute;top:30px;right:50px;font-size:280px;font-weight:900;color:#efefef;line-height:1;z-index:1;font-family:Satoshi,sans-serif;">*</div>'

ARROW_DARK = '<div style="position:absolute;bottom:60px;right:64px;font-size:48px;font-weight:400;color:#FAFAFA;z-index:5;">↗</div>'
ARROW_LIGHT = '<div style="position:absolute;bottom:60px;right:64px;font-size:48px;font-weight:400;color:#010101;z-index:5;">→</div>'

def label(txt):
    return f'<div style="font-size:28px;font-weight:700;color:#868686;letter-spacing:3px;text-transform:uppercase;">{txt}</div>'
```

### Bullet list pattern (Templates C / D)
Always use a grey circle dot (not em dash, not hyphen):

```python
def bullet(text, dark=False):
    fg = '#FAFAFA' if dark else '#010101'
    return f"""
<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:34px;">
  <div style="width:8px;height:8px;border-radius:50%;background:#868686;flex-shrink:0;margin-top:22px;"></div>
  <div style="font-size:44px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>
"""
```

### Render PNGs with Playwright
```python
import asyncio
from playwright.async_api import async_playwright

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in range(1, 10):
            page = await browser.new_page(viewport={'width': 1080, 'height': 1350})
            await page.goto(f'file:///home/claude/slide_{i:02d}.html')
            await page.wait_for_timeout(1000)  # let embedded fonts load
            await page.screenshot(path=f'/home/claude/slide_{i:02d}.png',
                                  full_page=False, type='png')
        await browser.close()

asyncio.run(render())
```

The 1000ms wait is required — without it the screenshot can fire before base64 fonts apply, and you'll get a system-font fallback baked into the PNG.

---

## Slide Variety Library — Code Patterns

All helpers below assume the shared helpers above (`head`, `LOGO_DARK`, `LOGO_LIGHT`, `ASTERISK_DARK`, `ASTERISK_LIGHT`, `ARROW_DARK`, `ARROW_LIGHT`, `label`) are already defined.

### Template G — Stat slide
For a single number that deserves the whole canvas.

```python
def stat_slide(label_text, big_number, supporting_line, dark=False):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>

<div style="position:absolute;top:480px;left:64px;right:64px;z-index:5;">
  <div style="font-size:280px;font-weight:900;color:{fg};line-height:1;letter-spacing:-8px;">{big_number}</div>
</div>

<div style="position:absolute;top:880px;left:64px;right:64px;z-index:5;">
  <div style="font-size:48px;font-weight:400;color:#868686;line-height:1.3;max-width:880px;">{supporting_line}</div>
</div>

{arrow}
</body></html>
"""
```

**Use when:** "$5/month VPS", "71% handoff rate", "From 4 hours to 23 minutes".

### Template H — Pull Quote slide
For a direct quote strong enough to carry the slide alone.

```python
def quote_slide(label_text, quote_text, attribution, dark=True):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    quote_mark_color = '#1a1a1a' if dark else '#efefef'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>

<div style="position:absolute;top:300px;left:48px;font-size:380px;font-weight:900;color:{quote_mark_color};line-height:1;font-family:Satoshi,serif;z-index:2;">"</div>

<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;">
  <div style="font-size:64px;font-weight:700;color:{fg};line-height:1.2;letter-spacing:-1px;">{quote_text}</div>
</div>

<div style="position:absolute;bottom:140px;left:64px;right:64px;z-index:5;">
  <div style="font-size:32px;font-weight:400;color:#868686;letter-spacing:1px;">— {attribution}</div>
</div>

{arrow}
</body></html>
"""
```

**Use when:** Customer testimonial, founder statement, expert quote.

### Template I — Comparison Table slide
For two things side-by-side. Real grid, not pretend bullets.

```python
def comparison_slide(label_text, headline, left_title, left_items, right_title, right_items, dark=False):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    divider = '#333' if dark else '#dadada'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    def col(title, items):
        rows = ''.join(
            f'<div style="font-size:32px;font-weight:400;color:{fg};line-height:1.4;padding:18px 0;border-bottom:1px solid {divider};">{x}</div>'
            for x in items
        )
        return f"""
<div style="flex:1;">
  <div style="font-size:36px;font-weight:900;color:{fg};margin-bottom:24px;letter-spacing:-1px;">{title}</div>
  {rows}
</div>
"""

    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:30px;font-size:72px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>

<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;display:flex;gap:60px;">
  {col(left_title, left_items)}
  <div style="width:1px;background:{divider};"></div>
  {col(right_title, right_items)}
</div>

{arrow}
</body></html>
"""
```

**Use when:** Two products, two approaches, two camps.

### Template J — Step Cards slide
For sequences. Each step gets its own numbered block.

```python
def step_slide(label_text, headline, steps, dark=False):
    """steps = [(title, body), ...] usually 3 items."""
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    num_color = '#868686'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    cards = ''
    for i, (title, body) in enumerate(steps, 1):
        cards += f"""
<div style="margin-bottom:40px;display:flex;gap:32px;align-items:flex-start;">
  <div style="font-size:80px;font-weight:900;color:{num_color};line-height:1;letter-spacing:-2px;min-width:100px;">0{i}</div>
  <div style="flex:1;">
    <div style="font-size:40px;font-weight:700;color:{fg};line-height:1.2;margin-bottom:8px;">{title}</div>
    <div style="font-size:30px;font-weight:400;color:#868686;line-height:1.35;">{body}</div>
  </div>
</div>
"""

    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:30px;font-size:72px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>

<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;">
  {cards}
</div>

{arrow}
</body></html>
"""
```

**Use when:** "Build order", "How it works in 3 steps", numbered process.

### Template K — Question slide
For a single provocative question filling the canvas. Pattern interrupt.

```python
def question_slide(label_text, question_text, dark=True):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    mark_color = '#1a1a1a' if dark else '#efefef'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_class) + f"""
{logo}
<div class="grid"></div>

<div style="position:absolute;top:80px;right:60px;font-size:520px;font-weight:900;color:{mark_color};line-height:1;font-family:Satoshi,sans-serif;z-index:1;">?</div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>

<div style="position:absolute;top:540px;left:64px;right:64px;z-index:5;">
  <div style="font-size:96px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{question_text}</div>
</div>

{arrow}
</body></html>
"""
```

**Use when:** Hook slide, transition slide, "What if..." setup.

### Template L — Definition slide
For introducing a term. Looks like a dictionary entry.

```python
def definition_slide(label_text, term, category, definition, dark=False):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    divider = '#333' if dark else '#dadada'
    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>

<div style="position:absolute;top:380px;left:64px;right:64px;z-index:5;">
  <div style="font-size:120px;font-weight:900;color:{fg};line-height:1;letter-spacing:-3px;">{term}</div>
  <div style="margin-top:12px;font-size:32px;font-weight:400;color:#868686;font-style:italic;">{category}</div>
</div>

<div style="position:absolute;top:740px;left:64px;right:64px;z-index:5;">
  <div style="height:1px;background:{divider};margin-bottom:40px;"></div>
  <div style="font-size:44px;font-weight:400;color:{fg};line-height:1.4;">{definition}</div>
</div>

{arrow}
</body></html>
"""
```

**Use when:** Introducing a concept, jargon explainer, "what we mean by X".

### Template M — Framework diagram slide
For a simple linear flow. Connected boxes.

```python
def framework_slide(label_text, headline, nodes, dark=False):
    """nodes = [str, str, str] usually 3-4 boxes."""
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    box_bg = '#151515' if dark else '#ffffff'
    box_border = '#333' if dark else '#dadada'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    boxes = ''
    for i, node in enumerate(nodes):
        boxes += f"""
<div style="background:{box_bg};border:1px solid {box_border};border-radius:16px;padding:40px 36px;margin-bottom:20px;display:flex;align-items:center;gap:24px;">
  <div style="width:48px;height:48px;border-radius:50%;background:#868686;color:{bg};font-size:28px;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{i+1}</div>
  <div style="font-size:42px;font-weight:700;color:{fg};line-height:1.2;">{node}</div>
</div>
"""
        if i < len(nodes) - 1:
            boxes += '<div style="text-align:center;font-size:36px;color:#868686;line-height:1;margin:-4px 0 16px 0;">↓</div>'

    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:30px;font-size:72px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>

<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;">
  {boxes}
</div>

{arrow}
</body></html>
"""
```

**Use when:** Process flow, decision tree, "X leads to Y leads to Z".

### Template N — Before/After Split slide
For a clean dichotomy. Page divided in half.

```python
def split_slide(label_text, headline, before_label, before_items, after_label, after_items):
    """Always uses light BG with two dark side-by-side cards."""
    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:30px;font-size:72px;font-weight:900;color:#010101;line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>

<div style="position:absolute;top:560px;left:64px;right:64px;bottom:140px;z-index:5;display:flex;gap:0;">
  <div style="flex:1;background:#010101;padding:48px 40px;border-radius:20px 0 0 20px;">
    <div style="font-size:24px;font-weight:700;color:#868686;letter-spacing:3px;text-transform:uppercase;margin-bottom:32px;">{before_label}</div>
    {''.join(f'<div style="font-size:34px;font-weight:400;color:#FAFAFA;line-height:1.35;margin-bottom:20px;">{x}</div>' for x in before_items)}
  </div>
  <div style="flex:1;background:#010101;padding:48px 40px;border-radius:0 20px 20px 0;border-left:1px solid #333;">
    <div style="font-size:24px;font-weight:700;color:#FAFAFA;letter-spacing:3px;text-transform:uppercase;margin-bottom:32px;">{after_label}</div>
    {''.join(f'<div style="font-size:34px;font-weight:400;color:#FAFAFA;line-height:1.35;margin-bottom:20px;">{x}</div>' for x in after_items)}
  </div>
</div>

{ARROW_LIGHT}
</body></html>
"""
```

**Use when:** Old way vs new way, problem state vs solution, with vs without.

### Template O — Checklist slide
For action items, criteria, completable tasks.

```python
def checklist_slide(label_text, headline, items, dark=False):
    """items = [(text, checked_bool), ...]"""
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_class = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    rows = ''
    for text, checked in items:
        if checked:
            box = f'<div style="width:36px;height:36px;border-radius:6px;background:{fg};display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:8px;"><div style="font-size:24px;font-weight:900;color:{bg};line-height:1;">✓</div></div>'
        else:
            box = f'<div style="width:36px;height:36px;border-radius:6px;border:2px solid #868686;flex-shrink:0;margin-top:8px;"></div>'
        rows += f"""
<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:30px;">
  {box}
  <div style="font-size:42px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>
"""

    return head(bg, grid_class) + f"""
{logo}
{asterisk}
<div class="grid"></div>

<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:30px;font-size:72px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>

<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;">
  {rows}
</div>

{arrow}
</body></html>
"""
```

**Use when:** Audit list, requirements, "are you doing all 5?", quality checklist.

---

## Universal Content Rule (blog/video repurposing)

When the user provides a video script, blog post, or any content where someone else has documented specific demos or use cases:

**DO NOT copy their specific examples verbatim.** It looks like plagiarism and damages brand credibility.

**Extract only universal, general truths:**

| ❌ Don't say (specific) | ✅ Do say (universal) |
|---|---|
| "It jailbroke Gemma 4 in 8 prompts" | "It handles complex multi-step tasks" |
| "Built a Mandarin video with TTS and HTML" | "Generates content end to end" |
| "Scraped Hacker News to JSON in 1 min" | "Research and data scraping" |

**The test:** If a stranger who hasn't watched the source could reasonably say the same thing from general knowledge about the topic, it's safe. If the bullet could only come from that specific video/blog, it's plagiarism risk.

---

## Caption Generation (always include)

Every carousel export ships with a `captions.md` file containing LinkedIn, Instagram, and Twitter/X versions.

### Caption rules
- **No em dashes (—).** Use `:`, `,`, or period.
- **Hook first** — first line stops the scroll. Question, bold stat, or pattern interrupt.
- **Conversational** — no "In today's fast-paced world".
- **Match the carousel's core insight** — tease it, don't give the whole thing away.
- **End with a CTA** that matches slide 9.
- **Hashtags at the end only**, never mid-body.

### Platform formats

**LinkedIn (1300–1800 chars)**
- 1-line scroll-stopper hook
- 2-3 short paragraphs expanding problem/insight
- 3-5 bullet takeaways (• or →)
- Strong CTA with context ("DM us", "Comment below")
- 3-5 hashtags
- Generous line breaks

**Instagram (800–1500 chars)**
- Hook line + emoji (max 2-3 emoji total)
- Short punchy paragraphs
- Mini bullet list (• or numbers)
- CTA: "Save this post", "Share with a founder"
- 15-20 hashtags in one block at end
- "Swipe through →" early in the body

**Twitter / X**
- Single tweet under 280 chars with main insight
- Optional 5-7 tweet thread version
- Max 1-2 hashtags
- CTA to profile/link

### Output file structure
Save as `/mnt/user-data/outputs/<topic>_captions.md`:

```markdown
# Carousel Captions

## LinkedIn
[long-form caption]

#AI #PromptEngineering #Codiste

---

## Instagram
[medium caption]

Swipe through →

#ai #promptengineering #codiste #aitools #...

---

## Twitter / X

**Single tweet:**
[short hook tweet]

**Thread version:**
1/ [hook]
2/ [point]
3/ [point]
4/ [CTA]
```

---

## Adding Images to Slides (Cover or Content)

### One way to get an image

**Option A — User uploads:** PNG/JPG appears in `/mnt/user-data/uploads/`. Base64 encode and embed.




### Image requirements
- **B&W or monochrome only** — colour clashes with `#010101/#FAFAFA/#868686`
- **Wide aspect ratios (2:1 or 16:9)** for cover slides
- **Match BG tone** — dark image on dark slide, light on light
- **Always base64 embed** — never external URLs (network is off during render)

### Cover slide layout with image
```
┌─────────────────────────────────────┐
│ [Codiste Logo]         *            │
│                                     │
│ LABEL (28px grey uppercase)         │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │      [IMAGE — 952px wide]       │ │
│ │      rounded corners +          │ │
│ │      subtle white border        │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Grey headline line 1                │
│ Grey headline line 2                │
│ White headline punchline            │
│                                  →  │
└─────────────────────────────────────┘
```

Image wrapper:
```html
<div style="position:absolute;top:230px;left:64px;right:64px;z-index:10;
            border-radius:20px;overflow:hidden;
            border:1px solid rgba(255,255,255,0.1);">
  <img src="data:image/png;base64,{img_b64}" style="width:100%;height:auto;display:block;" />
</div>
```

Headline starts around `top:770-800px` depending on image height.

---

## Edit Workflow (after delivery)

When user requests edits ("remove this label", "switch slide 4 to a stat slide", "change em dash to colon"):
1. Use `sed` or `str_replace` on the specific HTML file(s) in `/home/claude/`, or regenerate the slide with a different template helper
2. Re-render only the affected slide(s) with Playwright
3. Copy updated files to outputs (clean old ones first)
4. Call `present_files` again

---

## Quality Checklist (run before presenting)

- [ ] Only `#010101`, `#FAFAFA`, `#868686` used
- [ ] Real Satoshi embedded as base64 from bundled `assets/fonts/`
- [ ] Real Codiste logo embedded as base64 from bundled `assets/logo/` (white on dark, black on light, transparent PNG)
- [ ] Grid overlay present and subtle on every slide
- [ ] Grey label → bold headline → body hierarchy on every slide
- [ ] Decorative element on every slide (asterisk + arrow, except Question slide which uses the `?`)
- [ ] Canvas exactly 1080×1350px
- [ ] No em dashes (—) anywhere — slides or captions
- [ ] Headlines short and punchy (under 8 words)
- [ ] **Used 4-5 different template types across the 9 slides** — not 7 bullet slides in a row
- [ ] **Each slide's template matches its content type** per the mapping rule
- [ ] Individual PNG per slide exported
- [ ] `captions.md` generated with LinkedIn + Instagram + Twitter
- [ ] Captions follow no-em-dash rule and match the carousel's core insight
- [ ] If cover image used: B&W/monochrome, base64 embedded
- [ ] If repurposing from blog/video: all content is universal (no specific demos copied)
- [ ] Old outputs cleaned before copying new files

---

## Design Notes (lessons from prior runs)

1. **Fonts cannot load from external URLs** during Playwright rendering — network is off. Embed as base64 from bundled `assets/fonts/`.
2. **Em dashes look awkward in body text** — use `:` or `,` or period.
3. **Short headlines > long headlines** — break longer ones across 2–3 lines using grey-grey-white hierarchy.
4. **Always clean old outputs** before copying new ones to prevent stale PNGs in the shared folder.
5. **Cover images must be B&W/monochrome** — colour clashes with the strict palette.
6. **Images base64 embedded**, never external URLs.
7. **Never copy specific demos** from blogs/videos — keep everything universal.
8. **Logo must be transparent PNG, never JPG** — JPG has no alpha and renders as a solid square on light slides. Always use bundled PNGs.
9. **Content drives template, not rotation.** A stat goes on a Stat slide. A comparison goes on a Comparison Table. A quote goes on a Pull Quote. Bullets are the fallback for genuine peer-item lists, not the default.
10. **A 9-slide deck should use 4-5 different template types.** Same-shape slides in a row make the deck feel monotonous and reduce retention. Vary the layout aggressively.

---

## Installation

Self-contained skill. Bundles:
- `SKILL.md` — these instructions
- `assets/fonts/` — 10 Satoshi `.otf` files (Regular, Bold, Black, Medium, Light + italics)
- `assets/logo/` — Codiste logo as transparent PNG (white + black variants)

Install via Claude desktop app: Settings → Capabilities → Skills → drop the `.skill` file. Fonts and logo auto-load every session. No per-session uploads required.

**Optional:** user can drop a custom B&W cover image into `/mnt/user-data/uploads/` if they want a specific hero image on slide 1.
