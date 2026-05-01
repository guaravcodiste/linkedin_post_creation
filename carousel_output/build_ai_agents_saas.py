#!/usr/bin/env python3
"""
Codiste Carousel Builder — AI Agents for SaaS Customer Success
9 slides, 1080x1350px, Codiste brand system
"""

import base64, json, os, glob, asyncio
from pathlib import Path

OUT = Path('/home/user/linkedin_post_creation/carousel_output')
OUT.mkdir(exist_ok=True)

# ─── Fonts ────────────────────────────────────────────────────────────────────
with open(OUT / 'fonts.json') as f:
    fdata = json.load(f)

FONT_FACE = f"""
@font-face {{font-family:'PJS';font-weight:400;src:url('data:font/ttf;base64,{fdata["r400"]}') format('truetype');}}
@font-face {{font-family:'PJS';font-weight:700;src:url('data:font/ttf;base64,{fdata["r700"]}') format('truetype');}}
@font-face {{font-family:'PJS';font-weight:800;src:url('data:font/ttf;base64,{fdata["r800"]}') format('truetype');}}
"""

# ─── Codiste Logo SVG (white and black variants) ──────────────────────────────
# Concentric-C mark: three arcs forming a stylized C + "Codiste" wordmark
LOGO_WHITE_SVG = """<svg width="160" height="36" viewBox="0 0 160 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Concentric C mark -->
  <path d="M18 4 A14 14 0 0 0 18 32" stroke="#FAFAFA" stroke-width="3.5" stroke-linecap="round" fill="none"/>
  <path d="M18 8 A10 10 0 0 0 18 28" stroke="#FAFAFA" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M18 12 A6 6 0 0 0 18 24" stroke="#FAFAFA" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <!-- Wordmark -->
  <text x="34" y="25" font-family="Arial,sans-serif" font-size="18" font-weight="700" fill="#FAFAFA" letter-spacing="1">codiste</text>
</svg>"""

LOGO_BLACK_SVG = """<svg width="160" height="36" viewBox="0 0 160 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M18 4 A14 14 0 0 0 18 32" stroke="#010101" stroke-width="3.5" stroke-linecap="round" fill="none"/>
  <path d="M18 8 A10 10 0 0 0 18 28" stroke="#010101" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M18 12 A6 6 0 0 0 18 24" stroke="#010101" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <text x="34" y="25" font-family="Arial,sans-serif" font-size="18" font-weight="700" fill="#010101" letter-spacing="1">codiste</text>
</svg>"""

LOGO_WHITE_B64 = "data:image/svg+xml;base64," + base64.b64encode(LOGO_WHITE_SVG.encode()).decode()
LOGO_BLACK_B64 = "data:image/svg+xml;base64," + base64.b64encode(LOGO_BLACK_SVG.encode()).decode()

# ─── Shared CSS constants ─────────────────────────────────────────────────────
GRID_DARK = """
.grid{position:absolute;inset:0;pointer-events:none;z-index:1;
background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),
linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);
background-size:54px 54px;}"""

GRID_LIGHT = """
.grid{position:absolute;inset:0;pointer-events:none;z-index:1;
background-image:linear-gradient(rgba(0,0,0,0.04) 1px,transparent 1px),
linear-gradient(90deg,rgba(0,0,0,0.04) 1px,transparent 1px);
background-size:54px 54px;}"""

BASE_STYLE = """*{margin:0;padding:0;box-sizing:border-box;}
body{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:'PJS',sans-serif;}
.logo{position:absolute;top:60px;left:64px;z-index:10;width:160px;}
.asterisk{position:absolute;top:40px;right:64px;font-size:260px;line-height:1;opacity:0.04;
  font-weight:800;z-index:1;user-select:none;}
.label{font-size:26px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#868686;
  position:relative;z-index:10;}
.content{position:absolute;left:64px;right:64px;z-index:10;}
"""

def head(bg, is_dark):
    grid_css = GRID_DARK if is_dark else GRID_LIGHT
    ast_color = "#FAFAFA" if is_dark else "#010101"
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
{FONT_FACE}
{grid_css}
{BASE_STYLE}
body{{background:{bg};}}
.asterisk{{color:{ast_color};}}
</style></head><body>
<div class="grid"></div>
<img class="logo" src="{LOGO_WHITE_B64 if is_dark else LOGO_BLACK_B64}" />
<div class="asterisk">*</div>
"""

def bullet(text, color):
    return f"""<div style="display:flex;align-items:flex-start;gap:24px;margin-bottom:28px;">
  <div style="width:8px;height:8px;border-radius:50%;background:#868686;flex-shrink:0;margin-top:22px;"></div>
  <div style="font-size:42px;font-weight:400;color:{color};line-height:1.35;">{text}</div>
</div>"""

def arrow_dark():
    return '<div style="position:absolute;bottom:64px;right:64px;font-size:80px;color:#FAFAFA;opacity:0.3;z-index:10;font-weight:700;">↗</div>'

def arrow_light():
    return '<div style="position:absolute;bottom:64px;right:64px;font-size:80px;color:#010101;opacity:0.2;z-index:10;font-weight:700;">→</div>'

def close_html():
    return "</body></html>"

# ─── Slide 1 — Cover / Hook (DARK) ────────────────────────────────────────────
def slide1():
    # Try to embed cover image if available
    cover_img_html = ""
    cover_path = OUT / "cover_generated.png"
    if cover_path.exists() and cover_path.stat().st_size > 1000:
        with open(cover_path, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()
        cover_img_html = f"""
<div style="position:absolute;top:200px;left:64px;right:64px;z-index:10;
  border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.12);">
  <img src="data:image/png;base64,{img_b64}" style="width:100%;height:auto;display:block;" />
</div>"""
        headline_top = "760px"
    else:
        headline_top = "280px"

    html = head("#010101", True)
    html += cover_img_html
    html += f"""
<div class="content" style="top:{headline_top};">
  <div class="label" style="margin-bottom:32px;">AI AGENTS</div>
  <div style="font-size:84px;font-weight:800;color:#868686;line-height:1.1;letter-spacing:-2px;margin-bottom:8px;">Your CS team grew 40%.</div>
  <div style="font-size:84px;font-weight:800;color:#868686;line-height:1.1;letter-spacing:-2px;margin-bottom:8px;">Your churn still rose.</div>
  <div style="font-size:84px;font-weight:800;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;margin-bottom:48px;">Here's the agentic fix.</div>
  <div style="font-size:38px;font-weight:400;color:#868686;">Swipe →</div>
</div>"""
    html += arrow_dark()
    html += close_html()
    return html

# ─── Slide 2 — Problem / Why CS Breaks (LIGHT) ────────────────────────────────
def slide2():
    html = head("#FAFAFA", False)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">THE PROBLEM</div>
  <div style="font-size:78px;font-weight:800;color:#010101;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">Why Traditional CS<br>Breaks at Scale</div>
"""
    bullets = [
        "60-80% of customers are in self-serve tiers no CSM covers",
        "Enterprise CSMs now cost $250K+ fully loaded",
        "Renewal velocity demands sub-24hr signal detection",
        "Churn signals need to surface in days, not quarters",
    ]
    for b in bullets:
        html += bullet(b, "#010101")
    html += "</div>"
    html += arrow_light()
    html += close_html()
    return html

# ─── Slide 3 — Solution / What Agentic AI Does (DARK) ─────────────────────────
def slide3():
    html = head("#010101", True)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">THE SOLUTION</div>
  <div style="font-size:78px;font-weight:800;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">What Agentic AI<br>Adds to Your Stack</div>
"""
    bullets = [
        "Monitors 100% of accounts simultaneously",
        "Surfaces churn risk before customers go quiet",
        "Captures expansion signals the team would miss",
        "Turns reliable outcomes into priceable units",
    ]
    for b in bullets:
        html += bullet(b, "#FAFAFA")
    html += "</div>"
    html += arrow_dark()
    html += close_html()
    return html

# ─── Slide 4 — Case Study: Real Numbers (LIGHT) ───────────────────────────────
def slide4():
    html = head("#FAFAFA", False)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">CASE STUDY</div>
  <div style="font-size:78px;font-weight:800;color:#010101;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">31% Churn Cut<br>in 9 Months</div>
"""
    bullets = [
        "1,800 customers, $42M ARR, 19-person CS team",
        "Net revenue churn: 14.2% down to 9.8%",
        "Self-serve account churn: 22% down to 12%",
        "Gross retention climbed: 88% up to 93%",
    ]
    for b in bullets:
        html += bullet(b, "#010101")
    html += "</div>"
    html += arrow_light()
    html += close_html()
    return html

# ─── Slide 5 — Comparison: Manual vs Agentic (DARK) ──────────────────────────
def slide5():
    html = head("#010101", True)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">CS MODELS COMPARED</div>
  <div style="font-size:72px;font-weight:800;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">Manual vs Tool-Assisted<br>vs Agentic</div>
"""
    bullets = [
        "Manual CS: top 30-40% ARR, quarterly QBRs only",
        "Tool-assisted: top 50-60%, weekly health scores",
        "Agentic CS: 100% coverage, continuous sub-24hr alerts",
        "Cost per account: $9K vs $3.4K vs $700",
    ]
    for b in bullets:
        html += bullet(b, "#FAFAFA")
    html += "</div>"
    html += arrow_dark()
    html += close_html()
    return html

# ─── Slide 6 — Outcome-Based Pricing (LIGHT) ──────────────────────────────────
def slide6():
    html = head("#FAFAFA", False)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">PROFIT POOLS</div>
  <div style="font-size:72px;font-weight:800;color:#010101;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">Outcomes as<br>Priceable Revenue Units</div>
"""
    bullets = [
        "Premium Success tier: 8-25% of base ACV",
        "$4.2M ARR added in 9 months from one deployment",
        "38% mid-market and enterprise adoption in 6 months",
        "First movers set the category pricing convention",
    ]
    for b in bullets:
        html += bullet(b, "#010101")
    html += "</div>"
    html += arrow_light()
    html += close_html()
    return html

# ─── Slide 7 — Implementation Sequence (DARK) ─────────────────────────────────
def slide7():
    html = head("#010101", True)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">IMPLEMENTATION</div>
  <div style="font-size:78px;font-weight:800;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">Sequence the<br>Rollout Right</div>
"""
    bullets = [
        "Start with SMB and mid-market, not enterprise",
        "Enterprise relationship is the moat: protect it",
        "Build the data layer first: telemetry, support, billing",
        "Add intervention orchestration as the second layer",
    ]
    for b in bullets:
        html += bullet(b, "#FAFAFA")
    html += "</div>"
    html += arrow_dark()
    html += close_html()
    return html

# ─── Slide 8 — ROI / The Math (LIGHT) ────────────────────────────────────────
def slide8():
    html = head("#FAFAFA", False)
    html += """
<div class="content" style="top:148px;">
  <div class="label" style="margin-bottom:28px;">THE MATH</div>
  <div style="font-size:78px;font-weight:800;color:#010101;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">Pays Back in<br>the First Quarter</div>
"""
    bullets = [
        "Year-one build and run cost: $720K total",
        "Retained ARR from churn reduction: $2.8M saved",
        "Net new ARR from Premium Success tier: $4.2M",
        "Combined first-year return: $6.3M on $720K invested",
    ]
    for b in bullets:
        html += bullet(b, "#010101")
    html += "</div>"
    html += arrow_light()
    html += close_html()
    return html

# ─── Slide 9 — CTA Close (DARK) ──────────────────────────────────────────────
def slide9():
    html = head("#010101", True)
    html += """
<div class="content" style="top:320px;text-align:center;left:64px;right:64px;">
  <div class="label" style="text-align:center;margin-bottom:40px;">CODISTE</div>
  <div style="font-size:96px;font-weight:800;color:#868686;line-height:1.1;letter-spacing:-2px;margin-bottom:16px;">Size Your</div>
  <div style="font-size:96px;font-weight:800;color:#FAFAFA;line-height:1.1;letter-spacing:-2px;margin-bottom:56px;">Churn Pickup.</div>
  <div style="font-size:40px;font-weight:400;color:#868686;line-height:1.5;margin-bottom:80px;max-width:800px;margin-left:auto;margin-right:auto;">
    We'll run your retention metrics and map<br>the deployment and new revenue stream.
  </div>
  <a style="display:inline-block;padding:28px 64px;background:linear-gradient(135deg,#222,#383838);
    border:1px solid rgba(255,255,255,0.15);border-radius:60px;
    font-size:40px;font-weight:700;color:#FAFAFA;text-decoration:none;letter-spacing:0.5px;">
    Book a Call ↗
  </a>
</div>"""
    html += arrow_dark()
    html += close_html()
    return html

# ─── Write all HTML files ──────────────────────────────────────────────────────
slides = [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8, slide9]
for i, fn in enumerate(slides, 1):
    path = OUT / f"slide_{i:02d}.html"
    path.write_text(fn())
    print(f"Written {path.name}")

print("All HTML files written.")
