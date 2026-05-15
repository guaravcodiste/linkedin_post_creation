---
name: carousel-generation-workflow
description: >
  Complete end-to-end autonomous workflow for generating Codiste-branded LinkedIn/Instagram
  carousel images from Google Sheet content. Covers: reading sheet data via n8n, building
  9-slide carousels in Python + Playwright, pushing to GitHub, uploading to Google Drive,
  and sending Google Chat notification. Only includes conditions and code that are confirmed
  to work in production.
---

# Codiste Carousel Generation — Full Workflow

**Fully autonomous.** Read sheet → build slides → render PNGs → commit/push → upload to Drive → notify Google Chat.

---

## Environment (Confirmed Working)

| Item | Path / Value |
|---|---|
| Repo dir (fonts + logos) | `/home/user/linkedin_post_creation/` |
| Slide HTML workspace | `/home/claude/` |
| Outputs dir | `/mnt/user-data/outputs/` |
| Chromium executable | `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell` |
| Playwright version | `1.43.0` (matches chromium-1194) |
| GitHub branch | `claude/cool-tesla-UYzOH` (current working branch) |

---

## n8n Workflow IDs

| Workflow | ID |
|---|---|
| Read LinkedIn Sheet Data & Github (Carousel) | `01VGbkQh9V5Cz8DQ` |
| Upload AI Agent Carousel to Google Drive | `QMMl6ELpEz0wfbaW` |

**Google Drive folder ID:** `1pM75JINX2pud4fZ-Wk82S1zzSH9dI7mT`

**Google Chat webhook:**
`https://chat.googleapis.com/v1/spaces/AAQAT72CHuU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=meuLGzxAlDIIlSDFTG7skunMSeC6N2QPIZaqS93-93M`

---

## STEP 1 — Read Sheet Data via n8n

Execute workflow `01VGbkQh9V5Cz8DQ` in manual mode. It reads the **Carousel Content** tab from the Codiste Automation Google Sheet and also fetches the GitHub repo metadata.

```
executionMode: manual
workflowId: 01VGbkQh9V5Cz8DQ
```

**Output:** Each row in the sheet is one carousel to produce. Fields returned:
- `row_number` — row index (start from 2)
- `Content Source` — full article/blog text to repurpose into carousel slides

**Process rows sequentially:** complete the full pipeline for row 1 (build → render → push → upload → notify), then start row 2.

---

## STEP 2 — Analyse Content & Plan 9 Slides

Read the `Content Source` text. Extract universal insights — do NOT copy specific demos or examples verbatim. Rewrite everything in punchy, original voice.

**Determine topic slug** (lowercase, underscores, max 5 words):
- Example: `hire_ai_agent_dev_saas_skills`

### Slide structure
- **Slide 1:** Always Template A (Bold Statement), **Dark**
- **Slides 2–8:** Choose template per content type using the mapping below
- **Slide 9:** Always Template F (CTA), **Dark**

### Template selection rule

| If the slide content is… | Use |
|---|---|
| A single stat, %, or metric | **G — Stat** |
| A direct quote with attribution | **H — Pull Quote** |
| Two things being compared side by side | **I — Comparison Table** |
| A sequence of 3–5 ordered steps | **J — Step Cards** |
| A provocative question or rhetorical hook | **K — Question** |
| A term being defined | **L — Definition** |
| A linear flow of 3–4 connected concepts | **M — Framework** |
| Before vs after / X vs Y dichotomy | **N — Before/After Split** |
| A list of tasks, criteria, or audit items | **O — Checklist** |
| A list of 3–5 peer items (genuine list) | **C / D — Bullets** |
| A bold thesis or opening punchline | **A — Bold Statement** |
| Final pitch / call to action | **F — CTA** |

**Rule:** Use 4–5 different template types across the 9 slides. Never stack 7 bullet slides in a row.

### Light/dark rhythm
- Alternate light and dark backgrounds
- Never 3+ same-background slides in a row
- Slide 1 = Dark, Slide 9 = Dark

---

## STEP 3 — Build the Python Script

Create `/home/claude/build_{topic_slug}.py`.

### 3a — Asset setup (CONFIRMED WORKING paths)

```python
import base64, asyncio, shutil, os
from pathlib import Path

REPO_DIR = Path('/home/user/linkedin_post_creation')

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Fonts — loaded from repo root
r400 = b64(REPO_DIR / 'Satoshi-Regular.otf')
r700 = b64(REPO_DIR / 'Satoshi-Bold.otf')
r900 = b64(REPO_DIR / 'Satoshi-Black.otf')

FONT_FACE = f"""
@font-face {{font-family:'Satoshi';font-weight:400;src:url('data:font/otf;base64,{r400}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:700;src:url('data:font/otf;base64,{r700}') format('opentype');}}
@font-face {{font-family:'Satoshi';font-weight:900;src:url('data:font/otf;base64,{r900}') format('opentype');}}
"""
```

### 3b — Logo setup (CRITICAL — file meaning is opposite to their names)

```python
# VERIFIED by pixel analysis (May 2026):
# c_white_claude.png → avg Red channel = 250 → WHITE logo pixels → use on DARK backgrounds
# c_black_claude.png → avg Red channel = 1   → BLACK logo pixels → use on LIGHT backgrounds
# The SKILL.md variable names (LOGO_WHITE_B64, LOGO_BLACK_B64) are MISLEADING — ignore them.
# Use the mapping below — it is confirmed correct.

LOGO_FOR_DARK  = b64(REPO_DIR / 'c_white_claude.png')   # white logo on dark slide
LOGO_FOR_LIGHT = b64(REPO_DIR / 'c_black_claude.png')   # black logo on light slide

LOGO_DARK  = f'<img src="data:image/png;base64,{LOGO_FOR_DARK}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'
LOGO_LIGHT = f'<img src="data:image/png;base64,{LOGO_FOR_LIGHT}" style="position:absolute;top:60px;left:64px;width:48px;height:51px;object-fit:contain;z-index:10;" />'
```

### 3c — Shared helpers

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
    return f"""<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:34px;">
  <div style="width:8px;height:8px;border-radius:50%;background:#868686;flex-shrink:0;margin-top:22px;"></div>
  <div style="font-size:44px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>"""
```

---

## STEP 4 — Slide Template Reference (All Working Templates)

### Template A — Bold Statement (Cover / Dark)
Use for: Cover hook, punchy single thesis.

```python
def slide_cover(label_text, grey_line, white_headline, footer_line):
    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:310px;left:64px;right:64px;z-index:5;">
  <div style="font-size:60px;font-weight:400;color:#868686;line-height:1.25;margin-bottom:28px;">{grey_line}</div>
  <div style="font-size:98px;font-weight:900;color:#FAFAFA;line-height:1.0;letter-spacing:-3px;">{white_headline}</div>
</div>
<div style="position:absolute;bottom:130px;left:64px;right:120px;z-index:5;">
  <div style="font-size:34px;font-weight:400;color:#868686;">{footer_line}</div>
</div>
{ARROW_DARK}
</body></html>"""
```

---

### Template F — CTA Close (Dark)
Use for: Slide 9 always.

```python
def slide_cta(label_text, grey_setup, white_headline, button_text, url_text):
    return head('#010101', GRID_DARK) + f"""
{LOGO_DARK}
{ASTERISK_DARK}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:310px;left:64px;right:64px;z-index:5;">
  <div style="font-size:50px;font-weight:400;color:#868686;line-height:1.3;margin-bottom:36px;">{grey_setup}</div>
  <div style="font-size:92px;font-weight:900;color:#FAFAFA;line-height:1.0;letter-spacing:-3px;">{white_headline}</div>
</div>
<div style="position:absolute;bottom:230px;left:64px;z-index:10;">
  <div style="display:inline-flex;align-items:center;gap:16px;background:linear-gradient(135deg,#222,#383838);color:#FAFAFA;font-size:34px;font-weight:700;padding:22px 46px;border-radius:60px;letter-spacing:-0.5px;">{button_text} &#8599;</div>
</div>
<div style="position:absolute;bottom:130px;left:64px;font-size:30px;color:#868686;z-index:5;">{url_text}</div>
{ARROW_DARK}
</body></html>"""
```

---

### Template G — Stat (Dark or Light)
Use for: A single number/% that deserves the whole slide.

```python
def stat_slide(label_text, big_number, supporting_line, dark=True):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:400px;left:64px;right:64px;z-index:5;">
  <div style="font-size:260px;font-weight:900;color:{fg};line-height:1;letter-spacing:-8px;">{big_number}</div>
</div>
<div style="position:absolute;top:840px;left:64px;right:80px;z-index:5;">
  <div style="font-size:46px;font-weight:400;color:#868686;line-height:1.35;">{supporting_line}</div>
</div>
{arrow}
</body></html>"""
```

---

### Template H — Pull Quote (Dark preferred)
Use for: A direct quote strong enough to carry the whole slide.

```python
def quote_slide(label_text, quote_text, attribution, dark=True):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    qmark_color = '#1a1a1a' if dark else '#efefef'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:300px;left:48px;font-size:380px;font-weight:900;color:{qmark_color};line-height:1;z-index:2;">"</div>
<div style="position:absolute;top:560px;left:64px;right:64px;z-index:5;">
  <div style="font-size:64px;font-weight:700;color:{fg};line-height:1.2;letter-spacing:-1px;">{quote_text}</div>
</div>
<div style="position:absolute;bottom:140px;left:64px;right:64px;z-index:5;">
  <div style="font-size:32px;font-weight:400;color:#868686;letter-spacing:1px;">— {attribution}</div>
</div>
{arrow}
</body></html>"""
```

---

### Template I — Comparison Table (Light preferred)
Use for: Two things directly compared side by side.

```python
def comparison_slide(label_text, headline, left_title, left_items, right_title, right_items, dark=False):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    divider = '#333' if dark else '#dadada'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    def col(title, items, title_color):
        rows = ''.join(
            f'<div style="font-size:30px;font-weight:400;color:{fg};line-height:1.4;padding:15px 0;border-bottom:1px solid {divider};">{x}</div>'
            for x in items)
        return f"""<div style="flex:1;">
  <div style="font-size:28px;font-weight:900;color:{title_color};margin-bottom:18px;letter-spacing:2px;text-transform:uppercase;">{title}</div>
  {rows}
</div>"""

    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:26px;font-size:74px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:570px;left:64px;right:64px;z-index:5;display:flex;gap:56px;">
  {col(left_title, left_items, "#868686")}
  <div style="width:1px;background:{divider};"></div>
  {col(right_title, right_items, fg)}
</div>
{arrow}
</body></html>"""
```

---

### Template J — Step Cards (Light or Dark)
Use for: A numbered sequence of 3–4 ordered steps.

```python
def step_slide(label_text, headline, steps, dark=False):
    # steps = [(title_str, body_str), ...]
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    cards = ''
    for i, (title, body) in enumerate(steps, 1):
        cards += f"""
<div style="margin-bottom:30px;display:flex;gap:28px;align-items:flex-start;">
  <div style="font-size:60px;font-weight:900;color:#868686;line-height:1;letter-spacing:-2px;min-width:76px;">0{i}</div>
  <div style="flex:1;">
    <div style="font-size:36px;font-weight:700;color:{fg};line-height:1.2;margin-bottom:6px;">{title}</div>
    <div style="font-size:28px;font-weight:400;color:#868686;line-height:1.35;">{body}</div>
  </div>
</div>"""

    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:26px;font-size:74px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:530px;left:64px;right:64px;z-index:5;">
  {cards}
</div>
{arrow}
</body></html>"""
```

---

### Template K — Question (Dark preferred)
Use for: A single provocative question as a pattern interrupt. No asterisk — uses a large `?` instead.

```python
def question_slide(label_text, question_text, dark=True):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    qmark_color = '#1a1a1a' if dark else '#efefef'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_css) + f"""
{logo}
<div class="grid"></div>
<div style="position:absolute;top:80px;right:50px;font-size:520px;font-weight:900;color:{qmark_color};line-height:1;z-index:1;">?</div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:500px;left:64px;right:80px;z-index:5;">
  <div style="font-size:86px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{question_text}</div>
</div>
{arrow}
</body></html>"""
```

---

### Template L — Definition (Dark or Light)
Use for: Introducing a term in dictionary style.

```python
def definition_slide(label_text, term, category, definition, dark=True):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    divider = '#333' if dark else '#dadada'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT
    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
</div>
<div style="position:absolute;top:360px;left:64px;right:64px;z-index:5;">
  <div style="font-size:98px;font-weight:900;color:{fg};line-height:1.0;letter-spacing:-3px;">{term}</div>
  <div style="margin-top:14px;font-size:30px;font-weight:400;color:#868686;font-style:italic;">{category}</div>
</div>
<div style="position:absolute;top:760px;left:64px;right:64px;z-index:5;">
  <div style="height:1px;background:{divider};margin-bottom:36px;"></div>
  <div style="font-size:40px;font-weight:400;color:{fg};line-height:1.4;">{definition}</div>
</div>
{arrow}
</body></html>"""
```

---

### Template M — Framework / Flow (Light or Dark)
Use for: A simple linear flow of 3–4 connected concepts.

```python
def framework_slide(label_text, headline, nodes, dark=False):
    # nodes = [str, str, str]
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    box_bg = '#151515' if dark else '#ffffff'
    box_border = '#333' if dark else '#dadada'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    boxes = ''
    for i, node in enumerate(nodes):
        boxes += f"""
<div style="background:{box_bg};border:1px solid {box_border};border-radius:16px;padding:40px 36px;margin-bottom:20px;display:flex;align-items:center;gap:24px;">
  <div style="width:48px;height:48px;border-radius:50%;background:#868686;color:{bg};font-size:28px;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{i+1}</div>
  <div style="font-size:42px;font-weight:700;color:{fg};line-height:1.2;">{node}</div>
</div>"""
        if i < len(nodes) - 1:
            boxes += '<div style="text-align:center;font-size:36px;color:#868686;line-height:1;margin:-4px 0 16px 0;">&#8595;</div>'

    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:26px;font-size:74px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:530px;left:64px;right:64px;z-index:5;">
  {boxes}
</div>
{arrow}
</body></html>"""
```

---

### Template N — Before/After Split (Light)
Use for: X vs Y, wrong way vs right way.

```python
def split_slide(label_text, headline, before_label, before_items, after_label, after_items):
    return head('#FAFAFA', GRID_LIGHT) + f"""
{LOGO_LIGHT}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:26px;font-size:74px;font-weight:900;color:#010101;line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:550px;left:64px;right:64px;bottom:110px;z-index:5;display:flex;gap:0;">
  <div style="flex:1;background:#010101;padding:40px 36px;border-radius:20px 0 0 20px;">
    <div style="font-size:22px;font-weight:700;color:#868686;letter-spacing:3px;text-transform:uppercase;margin-bottom:26px;">{before_label}</div>
    {''.join(f'<div style="font-size:31px;font-weight:400;color:#FAFAFA;line-height:1.35;margin-bottom:18px;">{x}</div>' for x in before_items)}
  </div>
  <div style="flex:1;background:#010101;padding:40px 36px;border-radius:0 20px 20px 0;border-left:1px solid #333;">
    <div style="font-size:22px;font-weight:700;color:#FAFAFA;letter-spacing:3px;text-transform:uppercase;margin-bottom:26px;">{after_label}</div>
    {''.join(f'<div style="font-size:31px;font-weight:400;color:#FAFAFA;line-height:1.35;margin-bottom:18px;">{x}</div>' for x in after_items)}
  </div>
</div>
{ARROW_LIGHT}
</body></html>"""
```

---

### Template O — Checklist (Light or Dark)
Use for: Audit items, criteria, completable tasks.

```python
def checklist_slide(label_text, headline, items, dark=False):
    # items = [(text_str, checked_bool), ...]
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    rows = ''
    for text, checked in items:
        if checked:
            box = f'<div style="width:36px;height:36px;border-radius:6px;background:{fg};display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:8px;"><div style="font-size:22px;font-weight:900;color:{bg};line-height:1;">&#10003;</div></div>'
        else:
            box = f'<div style="width:36px;height:36px;border-radius:6px;border:2px solid #868686;flex-shrink:0;margin-top:8px;"></div>'
        rows += f"""
<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:24px;">
  {box}
  <div style="font-size:37px;font-weight:400;color:{fg};line-height:1.35;">{text}</div>
</div>"""

    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:26px;font-size:74px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:540px;left:64px;right:64px;z-index:5;">
  {rows}
</div>
{arrow}
</body></html>"""
```

---

### Templates C / D — Two-Column Bullets (Light / Dark)
Use for: A genuine list of 3–5 peer items. Fallback only — not the default.

```python
def bullets_slide(label_text, headline, bullets_list, dark=False):
    bg = '#010101' if dark else '#FAFAFA'
    fg = '#FAFAFA' if dark else '#010101'
    grid_css = GRID_DARK if dark else GRID_LIGHT
    logo = LOGO_DARK if dark else LOGO_LIGHT
    asterisk = ASTERISK_DARK if dark else ASTERISK_LIGHT
    arrow = ARROW_DARK if dark else ARROW_LIGHT

    items_html = ''.join(bullet(b, dark=dark) for b in bullets_list)

    return head(bg, grid_css) + f"""
{logo}
{asterisk}
<div class="grid"></div>
<div style="position:absolute;top:180px;left:64px;right:64px;z-index:5;">
  {label(label_text)}
  <div style="margin-top:26px;font-size:74px;font-weight:900;color:{fg};line-height:1.1;letter-spacing:-2px;">{headline}</div>
</div>
<div style="position:absolute;top:540px;left:64px;right:64px;z-index:5;">
  {items_html}
</div>
{arrow}
</body></html>"""
```

---

## STEP 5 — Write HTML Files and Render PNGs

```python
# Write HTML
slides = [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06, slide_07, slide_08, slide_09]
for i, fn in enumerate(slides, 1):
    with open(f'/home/claude/slide_{i:02d}.html', 'w') as f:
        f.write(fn())
    print(f"Written slide_{i:02d}.html")

# Render with Playwright — MUST use explicit executable path
CHROMIUM_EXEC = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'

async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROMIUM_EXEC)
        for i in range(1, 10):
            page = await browser.new_page(viewport={'width': 1080, 'height': 1350})
            await page.goto(f'file:///home/claude/slide_{i:02d}.html')
            await page.wait_for_timeout(1500)   # required — lets base64 fonts load
            await page.screenshot(path=f'/home/claude/slide_{i:02d}.png', full_page=False, type='png')
            print(f"Rendered slide_{i:02d}.png")
        await browser.close()

asyncio.run(render())

# Clean old outputs and copy new ones
os.makedirs('/mnt/user-data/outputs', exist_ok=True)
for f in Path('/mnt/user-data/outputs').glob('slide_*.png'):
    f.unlink()

for i in range(1, 10):
    shutil.copy(f'/home/claude/slide_{i:02d}.png', f'/mnt/user-data/outputs/slide_{i:02d}.png')
    print(f"Copied slide_{i:02d}.png")
```

---

## STEP 6 — Generate Captions File

Save as `/mnt/user-data/outputs/{topic_slug}_captions.md`.

### Format

```markdown
# Carousel Captions
## Topic: [topic title]

---

## LinkedIn
[1300–1800 chars]
- Hook line (first line must stop the scroll)
- 2–3 short paragraphs
- 3–5 bullet takeaways (• or →)
- Strong CTA
- 3–5 hashtags

---

## Instagram
[800–1500 chars]
- Hook + emoji (max 2–3 emoji total)
- Short punchy paragraphs
- "Swipe through →" early
- CTA: "Save this post"
- 15–20 hashtags in one block at end

---

## Twitter / X

**Single tweet:** [under 280 chars]

**Thread version:**
1/ [hook]
2/ [point]
...
7/ [CTA]
```

### Caption rules
- **No em dashes (—).** Use `:`, `,`, or period.
- Hook first — first line stops the scroll.
- Conversational, not corporate.
- Tease the carousel's insight; don't recap it fully.
- End with a CTA matching slide 9.
- Hashtags at the end only.

---

## STEP 7 — Rename Files with Topic Prefix and Commit to GitHub

```bash
TOPIC="hire_ai_agent_dev_saas_skills"   # set per row
mkdir -p outputs/${TOPIC}

for i in 01 02 03 04 05 06 07 08 09; do
  cp /mnt/user-data/outputs/slide_${i}.png outputs/${TOPIC}/${TOPIC}_slide_${i}.png
done
cp /mnt/user-data/outputs/${TOPIC}_captions.md outputs/${TOPIC}/${TOPIC}_captions.md

git add outputs/
git commit -m "Add ${TOPIC} carousel (9 slides + captions)"
git push -u origin claude/cool-tesla-UYzOH
```

**File naming convention:** `{topic_slug}_slide_01.png` through `{topic_slug}_slide_09.png` + `{topic_slug}_captions.md`

---

## STEP 8 — Update n8n Upload Workflow and Execute

Before executing, update the **Build File List** node in workflow `QMMl6ELpEz0wfbaW` to point to the correct GitHub branch and topic slug. Update the `jsCode`:

```javascript
const base = 'https://raw.githubusercontent.com/guaravcodiste/linkedin_post_creation/claude/cool-tesla-UYzOH/outputs/hire_ai_agent_dev_saas_skills';
const topic = 'hire_ai_agent_dev_saas_skills';
const files = [
  topic + '_slide_01.png', topic + '_slide_02.png', topic + '_slide_03.png',
  topic + '_slide_04.png', topic + '_slide_05.png', topic + '_slide_06.png',
  topic + '_slide_07.png', topic + '_slide_08.png', topic + '_slide_09.png',
  topic + '_captions.md'
];
return files.map(name => ({
  json: {
    fileName: name,
    url: base + '/' + name,
    mimeType: name.endsWith('.png') ? 'image/png' : 'text/markdown'
  }
}));
```

Then execute:
```
executionMode: manual
workflowId: QMMl6ELpEz0wfbaW
```

Wait for `status: success`. The workflow:
1. Downloads all 10 files from GitHub raw URL
2. Uploads each to Google Drive folder `1pM75JINX2pud4fZ-Wk82S1zzSH9dI7mT`
3. Sends a Google Chat notification (runs once via `executeOnce: true`)

---

## STEP 9 — Confirm and Present

- Check execution status via `get_execution` (status = `success`)
- Send slides to user via `present_files` (captions.md first, then slide_01 through slide_09)
- Report: Drive upload confirmed, Google Chat notification sent

---

## Brand System (Non-Negotiable)

### Colors
| Token | Hex | Use |
|---|---|---|
| Black | `#010101` | Dark backgrounds, text on light |
| White | `#FAFAFA` | Light backgrounds, text on dark |
| Grey | `#868686` | Labels, muted text, dividers, decorative |

**No other colors.** CTA gradient only: `linear-gradient(135deg,#222,#383838)`.

### Canvas
- Size: **1080 × 1350 px** (portrait 4:5)
- Padding: **64px** all sides minimum

### Typography — Satoshi (base64 embedded per slide)
| Use | File | Weight | Size |
|---|---|---|---|
| Labels | Satoshi-Bold.otf | 700 | 28px, UPPERCASE, 3px letter-spacing |
| Headlines | Satoshi-Black.otf | 900 | 74–100px, -2px letter-spacing |
| Body / bullets | Satoshi-Regular.otf | 400 | 44–46px, line-height 1.35 |

Font files live at repo root `/home/user/linkedin_post_creation/Satoshi-*.otf`.

### Logo
| Slide type | File to use | Why |
|---|---|---|
| Dark background (`#010101`) | `c_white_claude.png` | White pixels (avg R=250) are visible on dark |
| Light background (`#FAFAFA`) | `c_black_claude.png` | Black pixels (avg R=1) are visible on light |

Position: `top:60px; left:64px; width:48px; height:51px; z-index:10`

> **CRITICAL NOTE:** The original SKILL.md has the variable names swapped (`LOGO_WHITE_B64` reads `c_black_claude.png`). This is wrong. Always use the verified pixel values above to decide which file to load.

### Decorative elements
- **Asterisk `*`:** `position:absolute; top:30px; right:50px; font-size:280px; color:#1a1a1a (dark) / #efefef (light); z-index:1`
- **Arrow `↗` (dark) / `→` (light):** `position:absolute; bottom:60px; right:64px; font-size:48px; z-index:5`
- **Question slides:** replace asterisk with large `?` at `top:80px; right:50px; font-size:520px`

### z-index stack (never change)
| Layer | z-index |
|---|---|
| Grid overlay | 1 |
| Asterisk / `?` | 1 |
| Content blocks | 5 |
| Logo | 10 |

---

## Language & Style Rules

- **Never use em dashes (—).** Use `:`, `,`, or period.
- **Headlines:** under 8 words, sentence case. UPPERCASE only for labels.
- **Hierarchy:** Grey label → Grey setup/context → White/Black bold punchline.
- **Bullet dots:** 8×8px grey circle (`border-radius:50%`), NOT em-dashes or hyphens.
- **Labels:** 2–3 words, UPPERCASE, 3px letter-spacing, 28px, font-weight 700, `#868686`.

---

## Universal Content Rule

When repurposing blogs or articles:
- Extract universal insights only — do NOT copy specific demos or examples verbatim.
- If a bullet could only come from that specific source article, it is a plagiarism risk. Remove it.
- The test: "Could a knowledgeable person say this from general knowledge?" If yes, safe. If no, rewrite.

---

## Quality Checklist (Run Before Presenting)

- [ ] Only `#010101`, `#FAFAFA`, `#868686` used (no other colors)
- [ ] Satoshi embedded as base64 from repo root fonts
- [ ] Logo: `c_white_claude.png` on dark slides, `c_black_claude.png` on light slides
- [ ] Logo visible (z-index:10, position:absolute, correct file used)
- [ ] Grid overlay present on every slide (subtle, pointer-events:none)
- [ ] Label → headline → body hierarchy on every slide
- [ ] Asterisk / `?` / decorative element on every slide
- [ ] Arrow present on every slide (`↗` dark, `→` light)
- [ ] Canvas exactly 1080×1350px
- [ ] No em dashes (—) anywhere — slides or captions
- [ ] Headlines short and punchy (under 8 words)
- [ ] 4–5 different template types across the 9 slides (not all bullets)
- [ ] Light/dark alternation — never 3+ same-background slides in a row
- [ ] Slide 1 = Template A (dark), Slide 9 = Template F (dark)
- [ ] Playwright wait_for_timeout(1500) used — fonts load correctly before screenshot
- [ ] Old outputs cleaned before copying new PNGs
- [ ] Files renamed with `{topic_slug}_` prefix before committing
- [ ] Files committed and pushed to correct branch
- [ ] Captions MD generated (LinkedIn + Instagram + Twitter)
- [ ] n8n upload workflow `Build File List` node updated to correct branch + topic slug
- [ ] n8n upload workflow executed and status = `success`
- [ ] Google Chat notification confirmed sent

---

## Common Failures and Fixes

| Failure | Cause | Fix |
|---|---|---|
| Logo not visible | Wrong logo file used (color invisible on bg) | `c_white_claude.png` → dark slides, `c_black_claude.png` → light slides |
| Font renders as system font | Playwright took screenshot before fonts loaded | `wait_for_timeout(1500)` — never reduce below 1000ms |
| Chromium not found | Playwright version mismatch with installed browser | Use explicit `executable_path='/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'` |
| n8n downloads wrong files | Build File List still pointing to old branch/topic | Update `jsCode` in Build File List node before every run |
| Em dash renders badly | Used `—` in copy | Replace with `:`, `,`, or period |
| All middle slides look the same | Used bullet template for everything | Apply the template mapping rule — vary 4–5 types |
| Logo too small | Transparent padding not removed | Only applies to Pillow/banner workflow — for HTML carousel use `width:48px; height:51px; object-fit:contain` |

---

## Confirmed Working n8n SDK Workflow (Upload to Drive)

```javascript
import { workflow, node, trigger } from '@n8n/workflow-sdk';

const start = trigger({
  type: 'n8n-nodes-base.manualTrigger',
  version: 1,
  config: { name: 'Start', position: [0, 0] },
  output: [{}]
});

const buildFileList = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Build File List',
    position: [224, 0],
    parameters: {
      jsCode: `const base = 'https://raw.githubusercontent.com/guaravcodiste/linkedin_post_creation/claude/cool-tesla-UYzOH/outputs/hire_ai_agent_dev_saas_skills';
const topic = 'hire_ai_agent_dev_saas_skills';
const files = [
  topic + '_slide_01.png', topic + '_slide_02.png', topic + '_slide_03.png',
  topic + '_slide_04.png', topic + '_slide_05.png', topic + '_slide_06.png',
  topic + '_slide_07.png', topic + '_slide_08.png', topic + '_slide_09.png',
  topic + '_captions.md'
];
return files.map(name => ({
  json: {
    fileName: name,
    url: base + '/' + name,
    mimeType: name.endsWith('.png') ? 'image/png' : 'text/markdown'
  }
}));`
    }
  },
  output: [{ json: { fileName: 'slide_01.png', url: '...', mimeType: 'image/png' } }]
});

const downloadFromGitHub = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.4,
  config: {
    name: 'Download from GitHub',
    position: [448, 0],
    parameters: {
      url: '={{ $json.url }}',
      options: { response: { response: { responseFormat: 'file' } } }
    }
  },
  output: [{}]
});

const uploadToGoogleDrive = node({
  type: 'n8n-nodes-base.googleDrive',
  version: 3,
  config: {
    name: 'Upload to Google Drive',
    position: [672, 0],
    parameters: {
      operation: 'upload',
      name: "={{ $('Build File List').item.json.fileName }}",
      driveId: { __rl: true, mode: 'list', value: 'My Drive' },
      folderId: { __rl: true, mode: 'id', value: '1pM75JINX2pud4fZ-Wk82S1zzSH9dI7mT' },
      options: {}
    }
  },
  output: [{}]
});

const sendGoogleChat = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.4,
  config: {
    name: 'Send Google Chat Success',
    position: [896, 0],
    executeOnce: true,
    parameters: {
      method: 'POST',
      url: 'https://chat.googleapis.com/v1/spaces/AAQAT72CHuU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=meuLGzxAlDIIlSDFTG7skunMSeC6N2QPIZaqS93-93M',
      sendBody: true,
      specifyBody: 'json',
      jsonBody: { text: 'Carousel ready! [Topic] — 9 slides + captions uploaded to Google Drive.' },
      options: {}
    }
  },
  output: [{}]
});

export default workflow('QMMl6ELpEz0wfbaW', 'LinkedIn Content — Upload to Google Drive (carsoual)')
  .add(start)
  .to(buildFileList)
  .to(downloadFromGitHub)
  .to(uploadToGoogleDrive)
  .to(sendGoogleChat);
```

---

*Last updated: May 2026 — based on confirmed production run.*
*Corrections in this version vs SKILL.md: logo file mapping fixed (pixel-verified), Playwright executable path added, font path corrected to repo root, all unused asset-upload and Freepik sections removed.*
