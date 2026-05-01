#!/usr/bin/env python3
"""Build PDF and captions from rendered PNGs."""

import glob
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
from PIL import Image

OUT = Path('/home/user/linkedin_post_creation/carousel_output')
FINAL_OUT = Path('/home/user/linkedin_post_creation/outputs')
FINAL_OUT.mkdir(exist_ok=True)

TOPIC = "ai_agents_saas_customer_success"
PDF_NAME = f"{TOPIC}_carousel.pdf"

# ─── Build PDF ────────────────────────────────────────────────────────────────
files = sorted(glob.glob(str(OUT / 'slide_*.png')))
img0 = Image.open(files[0])
w, h = img0.size
page_w, page_h = w * 0.75, h * 0.75

pdf_path = OUT / PDF_NAME
c = rl_canvas.Canvas(str(pdf_path), pagesize=(page_w, page_h))
for f in files:
    c.drawImage(f, 0, 0, width=page_w, height=page_h)
    c.showPage()
c.save()
print(f"PDF saved: {pdf_path} ({pdf_path.stat().st_size // 1024}KB)")

# ─── Generate captions.md ─────────────────────────────────────────────────────
captions = """# AI Agents for SaaS Customer Success — Carousel Captions

## LinkedIn

Your CS team headcount grew 40% last year.
Your net revenue churn still rose.

That's not a people problem. That's an architecture problem.

The traditional CS model was built for a different customer mix. Today, 60-80% of SaaS customers sit in self-serve tiers no CSM will ever touch. They expand quietly. And they churn quietly.

Agentic AI fixes the architecture by doing the one thing your CS team can't: monitoring every account simultaneously, surfacing churn risk before the customer goes silent, and converting expansion signals the team would otherwise miss.

The business model implication is bigger than the retention improvement.

When the agent reliably produces an outcome (recovered account, expansion signal converted, churn risk neutralized) that outcome becomes a priceable unit. Premium Success tiers priced at 8-25% of base ACV are seeing 38% adoption among mid-market and enterprise customers within 6 months of launch.

One Series C B2B SaaS company with $42M ARR deployed this in mid-2025:
- Net revenue churn: 14.2% down to 9.8% in 9 months
- Gross retention: 88% up to 93%
- $4.2M ARR added through a new Premium Success tier
- Combined return: $6.3M on a $720K investment

The deployment paid back in Q1.

If you're running a B2B SaaS with a growing customer base and a CS team that can't cover it all, the agentic CS layer is worth sizing for your specific mix.

Swipe through to see the full playbook.

#AIAgents #SaaS #CustomerSuccess #ChurnReduction #B2BSaaS #Codiste

---

## Instagram

Your CS team grew. Your churn still grew faster. Here's why -- and the fix. 👇

The traditional customer success model breaks when most of your customers are in self-serve tiers no CSM will ever reach.

AI agents change the architecture:
- 100% account coverage (not just the top 40% by ARR)
- Churn signals surface in hours, not at quarterly QBRs
- Expansion signals captured before they go cold
- Outcomes become priceable, not just trackable

Real deployment numbers from a Series C SaaS:
- 1,800 customers, $42M ARR
- Net churn cut from 14.2% to 9.8% in 9 months
- $4.2M new ARR from a Premium Success tier
- $6.3M return on a $720K investment

Swipe through → to see the full breakdown of manual vs tool-assisted vs agentic CS, the rollout sequence, and the math that pays back in Q1.

Save this if you're planning a CS infrastructure overhaul.

#AIAgents #SaaS #CustomerSuccess #ChurnReduction #B2BSaaS #ArtificialIntelligence #SaaSGrowth #ProductLedGrowth #CustomerRetention #RevenueGrowth #Codiste #AIAutomation #StartupGrowth #VentureCapital #SaaSMetrics #ChurnPrevention #CustomerExperience #GrowthHacking #TechStartup #SaaSTips

---

## Twitter / X

**Single tweet:**
Your CS headcount grew 40%. Your churn still rose. That's not a people problem -- it's an architecture problem. AI agents fix it by covering 100% of accounts simultaneously. One Series C SaaS cut net churn 31% and added $4.2M ARR in 9 months.

**Thread version:**
1/ Your CS team grew 40% last year. Your churn still rose. Here's why -- and the agentic fix that cut net revenue churn 31% at a $42M ARR SaaS. (Thread)

2/ The traditional CS model covers only 30-40% of your customer base by ARR. The remaining 60-70% -- mostly self-serve -- churn quietly. No CSM ever touches them.

3/ AI agents change the architecture: 100% account coverage, churn signals in hours (not quarters), expansion signals before they go cold. Cost per covered account drops from $9K to $700.

4/ Real numbers: 1,800 customers, $42M ARR. Net churn from 14.2% to 9.8% in 9 months. Self-serve churn from 22% to 12%. Gross retention from 88% to 93%.

5/ The bigger story: when the agent reliably produces outcomes, those outcomes become priceable. A Premium Success tier at 8-25% of ACV hit 38% adoption in 6 months. Added $4.2M ARR.

6/ The ROI: $720K year-one cost. $2.8M retained ARR from churn reduction. $4.2M new ARR from the Success tier. $6.3M combined return. Paid back in Q1.

7/ Sequence the rollout right: start with SMB and mid-market, not enterprise. The enterprise relationship is the moat. Build the data layer first, then intervention orchestration. @codiste builds this layer for B2B SaaS.
"""

captions_path = OUT / f"{TOPIC}_captions.md"
captions_path.write_text(captions)
print(f"Captions saved: {captions_path}")

# ─── Copy to outputs folder ────────────────────────────────────────────────────
import shutil

# Remove old outputs
for f in FINAL_OUT.glob('slide_*.png'):
    f.unlink()
for f in FINAL_OUT.glob('*.pdf'):
    f.unlink()
for f in FINAL_OUT.glob('*captions*.md'):
    f.unlink()

# Copy new outputs
for f in sorted(OUT.glob('slide_*.png')):
    shutil.copy(f, FINAL_OUT / f.name)
shutil.copy(pdf_path, FINAL_OUT / PDF_NAME)
shutil.copy(captions_path, FINAL_OUT / f"{TOPIC}_captions.md")

print(f"\nFiles copied to {FINAL_OUT}:")
for f in sorted(FINAL_OUT.iterdir()):
    print(f"  {f.name}  ({f.stat().st_size // 1024}KB)")
