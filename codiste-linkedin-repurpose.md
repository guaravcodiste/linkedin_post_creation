---
name: codiste-linkedin-repurpose
description: >
  Full end-to-end autonomous workflow: turn a blog URL, raw blog content, an already-written
  article, a topic + a few points, or even an inspiring tweet into a complete LinkedIn
  deliverable — article (if needed), single best caption with hashtags, AI-generated hero image
  via Freepik Mystic, and a fully composited Codiste-branded banner. Trigger whenever the user
  provides any of: a blog URL, blog text, a written article, a topic with points, rough notes,
  or a social post to base content on. Also trigger when the user says "repurpose this blog",
  "convert to LinkedIn", "make a LinkedIn version", "turn this into an article", "create a
  banner for this article", "I have my article, give me the banner", "make a post about X",
  or any similar request.
---
 
# Codiste LinkedIn Full Workflow
## Blog/Topic/Article → LinkedIn Article → Caption → Banner (Fully Autonomous)
 
This skill handles the **complete pipeline** in one session, fully autonomously:
1. Input (URL / blog content / written article / topic+points / tweet) → LinkedIn article (skip if user already provided one)
2. Best title chosen automatically (no 5-option presentations unless user explicitly asks)
3. Caption written (single best version, no multiple options unless user asks)
4. Hero image generated via **Freepik Mystic** — article-specific composition, never generic
5. Python/Pillow banner compositor → PNG + JPG delivered
**Default mode is autonomous.** Only ask for input when something is genuinely missing (e.g., the user provided no content). Never ask the user to choose between angles, titles, or captions unless they explicitly request options.
 
---
 
## ASSETS — Always Load From Project Folder
 
**The assets folder is permanently seeded.** All four required assets are confirmed to live at `/mnt/skills/user/codiste-linkedin-repurpose/assets/` as of April 2026. **Never ask the user to upload fonts or the logo — they are already there.** The user has explicitly requested zero asset-upload interrupts.
 
```
ASSETS = '/mnt/skills/user/codiste-linkedin-repurpose/assets/'
```
 
| Asset | Path |
|---|---|
| Logo (white version) | `ASSETS + 'c_white_claude__2_.png'` |
| Font Regular | `ASSETS + 'Satoshi-Regular.otf'` |
| Font Bold | `ASSETS + 'Satoshi-Bold.otf'` |
| Font Medium | `ASSETS + 'Satoshi-Medium.otf'` |
 
**Loading code (used in the compositor):**
```python
import os
ASSETS = '/mnt/skills/user/codiste-linkedin-repurpose/assets/'
UPLOADS = '/mnt/user-data/uploads/'
 
def find_asset(name):
    """Load from ASSETS folder. Uploads is a defensive fallback only —
    the assets folder is seeded and should always have the files."""
    for base in [ASSETS, UPLOADS]:
        p = base + name
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Asset {name} not found — assets folder may have been wiped, ask user to re-upload")
 
required = ['c_white_claude__2_.png', 'Satoshi-Regular.otf', 'Satoshi-Bold.otf', 'Satoshi-Medium.otf']
```
 
**Only ask the user to upload assets if the assets folder has been wiped AND uploads is empty** — i.e., a true catastrophic loss. This is a recovery path, not a normal flow. If you are tempted to ask for assets in a normal session, you are wrong; the files are there.
 
---
 
## INTAKE FLOW — How to Decide What to Do
 
When a request comes in, classify it into one of these:
 
| User provides | What Claude does |
|---|---|
| Blog URL | Fetch via `web_fetch` → write LinkedIn article → caption → banner |
| Raw blog content (pasted) | Write LinkedIn article → caption → banner |
| Already-written LinkedIn article | Skip article writing → use/refine title → caption → banner |
| Topic + bullets / rough notes | Write LinkedIn article → caption → banner |
| Tweet, social post, or external content | Write LinkedIn article inspired by it → caption → banner |
| "I have my article, just give me the banner" | Skip article + caption (unless asked), go straight to banner |
 
**Never ask "topic-led or audience-led?"** when the user has already given you the article — it's already been written. The angle question only applies *before* writing a fresh article. Default to **audience-led (CTO / founder / product leader POV)** unless the user explicitly says otherwise.
 
**Angle definitions** (only relevant when writing a fresh article and the user explicitly asks for the choice):
- **Topic-led:** Title and article center on the subject matter — the technology, the event, the concept. Tone is informative and insight-driven.
- **Audience-led (DEFAULT):** Title and article speak directly to CTOs, startup founders, and tech-forward business owners. Tone is strategic, challenge-framing, and outcome-focused.
---
 
## PHASE 1 — ARTICLE (skip if user provides one)
 
### Step 1 — Extract / Receive Content
 
- URL → use `web_fetch`
- Pasted text → use directly
- Topic + bullets → use as the seed argument
- Reference tweet / social post → treat as inspiration, build the article around the same insight
After extracting, internally note:
- The **core message** (what is this content really saying?)
- The **3–5 key insights** worth keeping
- The **target audience** (who would benefit from reading this?)
### Step 2 — Choose the Title (Autonomously)
 
**Default behavior: pick the best title yourself, no options.**
 
Title rules:
- **Keep titles SHORT and PUNCHY** — aim for 50–65 characters, max 70. Do NOT push the 100-char limit.
- **Use `:` (colon) for splits, NEVER `—` (em-dash).** Em-dashes don't render well at large banner sizes and break the rhythm.
- Audience-led by default (CTO / founder / product leader POV).
- Use curiosity, urgency, or strong POV — not descriptive labels.
- Title must be completely different from the source content's title.
**Title style examples:**
| Original Style | LinkedIn Title (audience-led, short, colon) |
|---|---|
| "Introduction to AI Agents" | "Why AI Agents Are Replacing Workflows in 2026" |
| "Mistral vs Llama 3" | "Mistral vs Llama 3: A Practical Decision Guide" |
| "GPT-5.5 release notes" | "GPT-5.5: The Agentic Leap (and the 2x Price Tag)" |
| "Email tracking pixel changes" | "Gmail's Pixel Change: A Wake-Up Call for Every Business Relying on Email" |
| "ML vs Generative AI guide" | "When to Use Machine Learning vs Generative AI: A Practical Guide" |
| "MCP audit checklist" | "The Ultimate CISO Checklist: Audit-Ready MCP Servers in Fintech" |
| "Anthropic prompt workshop" | "You're Using Claude at 5%: Anthropic Just Showed Why" |
| "Benefits of Blockchain for Supply Chain" | "What Supply Chain Leaders Are Getting Wrong About Blockchain" |
| "Future-Oriented Generative AI Applications" | "Why Most Business AI Strategies Are Already Outdated in 2026" |
 
**Only present 5 options when:** user explicitly asks for "options" / "give me a few" / "5 titles" / similar.
 
### Step 3 — Write the Article (700–800 words)
 
#### Length
- **700–800 words** — tight and scannable
- Cut fluff, repetition, and overly technical detail
- **Do NOT go over 800 words.** Word count overrun is a top reason articles underperform on LinkedIn.
#### Opening Hook (first 2–3 lines — critical)
- LinkedIn truncates at ~200 chars before "...see more"
- Open with a bold statement, surprising stat, or relatable pain point
- NEVER start with "In today's digital world…", "In this article…", or generic openers
**Examples of strong openings:**
- *"Most companies are building AI wrong. Here's what the smart ones do differently."*
- *"We've helped 50+ startups launch blockchain products. The #1 mistake? Skipping this step."*
- *"Web3 isn't dead. It just grew up."*
- *"The model you pick isn't an AI decision — it's a product bet on speed vs reasoning."*
#### Structure
```
[HOOK PARAGRAPH]       — 2–3 punchy lines, no heading
[CONTEXT / PROBLEM]    — Why this matters now
[SECTION 1]            — First key insight (subheading) + bullets
[SECTION 2]            — Second key insight (subheading) + bullets
[SECTION 3]            — Third key insight (subheading) + bullets
[TAKEAWAY]             — 2–3 lines crystallizing the point
[CTA]                  — Read more + connect with Codiste
```
 
#### Formatting Rules
- Max 2–3 sentences per paragraph
- Each section uses 3–5 bullet points (1 sentence each, punchy)
- Mix: 1–2 intro sentences → 3–5 bullets → optional closing line
**Example section format:**
```
## Why Most AI Implementations Fail
 
Companies dive into AI without a clear strategy. The result? Wasted budgets and frustrated teams.
 
Here's what goes wrong:
- No defined use case before building
- Data is siloed or poorly structured
- Teams lack AI literacy to adopt the tools
- ROI is never measured properly
 
Getting this right from day one changes everything.
```
 
#### Subheading Rules
- **Make them outcome-oriented or question-based** — never copy the blog's subheadings verbatim
- Use numbers where natural ("3 reasons", "The 5-step…")
- Keep them under 8 words when possible
- Each subheading should make a reader want to read that section
#### Tone & Voice
- Conversational but credible — smart colleague, not sales pitch
- First-person plural where natural ("We've seen…", "Our team has worked with…")
- Active voice always
- No jargon without explanation
- Avoid: "leverage", "synergy", "cutting-edge", "game-changing", "in today's fast-paced world"
#### Keywords & SEO for LinkedIn
Naturally weave in:
- The **core topic keyword** (e.g., "AI agents", "blockchain development", "Web3")
- Related professional terms the target audience searches for
- Do NOT keyword-stuff — one natural mention per paragraph is enough
- Use the keyword in: the title, first paragraph, and at least one subheading
#### CTA Block (end of every article)
```
---
 
🔗 **Want the full breakdown?**
Read the complete guide on Codiste's blog: [Insert blog URL here]
 
🤝 **Building something in [topic area]?**
Connect with Codiste — we help startups and enterprises design, build, and scale
[AI / Blockchain / Web] solutions. Reach out at codiste.com or drop a comment below.
```
 
### Step 4 — Authenticity Check
 
Every claim, stat, example, or fact must trace back to the source content.
 
**Verify:**
1. **Stats & Numbers** — Every figure must appear in the original content. If not there, remove it.
2. **Examples & Case Studies** — Any specific company, product, or scenario must come from the source.
3. **Claims & Assertions** — Every bold claim must be grounded in the source.
4. **New Ideas** — If a sentence introduces an idea not in the source, remove it or mark it as a rhetorical device.
**What IS allowed:**
- Rewording the same idea in a punchier way ✅
- Reorganizing the order of points ✅
- Simplifying technical explanations ✅
- Adding a rhetorical question as a hook (grounded in the source) ✅
- Sharpening framing or POV (as long as the underlying claim is in the source) ✅
**What is NOT allowed:**
- Adding stats or numbers not in the source ❌
- Mentioning companies or products not referenced in the source ❌
- Drawing conclusions the source doesn't make ❌
- Filling gaps with general industry knowledge ❌
### Step 5 — Caption (Single Best Version)
 
**Default: write ONE caption, your best one.** Only generate multiple options if the user asks for "more options", "give me variations", or similar.
 
Caption rules:
- **Strictly 2 lines only**
- **Line 1:** Bold standalone insight in **Unicode bold** — angle NOT covered in the article
- **Line 2:** Natural CTA to the article (with `→ [article link]`)
- 4–6 hashtags after Line 2 (separate from article hashtags)
- Tone: authoritative, strategic, CTO / product leadership audience
- Never start Line 1 with "In today's…", "AI is transforming…", or generic openers
**Caption examples by topic** (use the closest one as tone reference, never copy verbatim):
 
*ML/GenAI architecture (reframe hook):*
```
𝗧𝗵𝗲 𝗯𝘂𝘀𝗶𝗻𝗲𝘀𝘀𝗲𝘀 𝘄𝗶𝗻𝗻𝗶𝗻𝗴 𝘄𝗶𝘁𝗵 𝗔𝗜 𝘀𝘁𝗼𝗽𝗽𝗲𝗱 𝗮𝘀𝗸𝗶𝗻𝗴 "𝘄𝗵𝗶𝗰𝗵 𝘁𝗲𝗰𝗵𝗻𝗼𝗹𝗼𝗴𝘆" 𝗮𝗻𝗱 𝘀𝘁𝗮𝗿𝘁𝗲𝗱 𝗮𝘀𝗸𝗶𝗻𝗴 "𝘄𝗵𝗶𝗰𝗵 𝗮𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲."
ML vs Generative AI is the wrong debate — here's what's actually driving ROI → [article link]
#AIStrategy #MachineLearning #GenerativeAI #AIArchitecture #ProductStrategy
```
 
*Pattern-recognition / tech shifts:*
```
𝗙𝗶𝗿𝘀𝘁 𝗶𝘁 𝘄𝗮𝘀 𝗔𝗽𝗽𝗹𝗲. 𝗧𝗵𝗲𝗻 𝗶𝗻𝗯𝗼𝘅 𝗔𝗜. 𝗡𝗼𝘄 𝗚𝗺𝗮𝗶𝗹. 𝗧𝗵𝗲 𝗽𝗮𝘁𝘁𝗲𝗿𝗻 𝗶𝘀 𝘁𝗼𝗼 𝗼𝗯𝘃𝗶𝗼𝘂𝘀 𝘁𝗼 𝗶𝗴𝗻𝗼𝗿𝗲.
Stop treating this as a marketing problem — it's a product strategy one → [article link]
#EmailStrategy #ProductStrategy #CTOInsights #PrivacyFirst #DigitalTransformation
```
 
*Capital efficiency / studio:*
```
𝗧𝗵𝗲 𝘀𝘁𝘂𝗱𝗶𝗼𝘀 𝘄𝗶𝗻𝗻𝗶𝗻𝗴 𝗶𝗻 𝟮𝟬𝟮𝟲 𝗮𝗿𝗲𝗻'𝘁 𝘁𝗵𝗲 𝗼𝗻𝗲𝘀 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗯𝗶𝗴𝗴𝗲𝘀𝘁 𝗳𝘂𝗻𝗱𝘀 — 𝘁𝗵𝗲𝘆'𝗿𝗲 𝘁𝗵𝗲 𝗼𝗻𝗲𝘀 𝘁𝗮𝗸𝗶𝗻𝗴 𝟯𝘅 𝗺𝗼𝗿𝗲 𝘀𝗵𝗼𝘁𝘀 𝗼𝗻 𝗴𝗼𝗮𝗹.
The math behind AI-powered venture studios — and why most are still using the old playbook → [article link]
#VentureStudios #AIForStartups #StartupStrategy #CapitalEfficiency #AIStrategy
```
 
*Security / fintech (challenge hook):*
```
𝗬𝗼𝘂𝗿 𝗔𝗜 𝗮𝗴𝗲𝗻𝘁𝘀 𝗮𝗿𝗲 𝗺𝗮𝗸𝗶𝗻𝗴 𝗱𝗲𝗰𝗶𝘀𝗶𝗼𝗻𝘀 𝘁𝗵𝗮𝘁 𝗮𝘂𝗱𝗶𝘁𝗼𝗿𝘀 𝘄𝗶𝗹𝗹 𝗼𝗻𝗲 𝗱𝗮𝘆 𝗮𝘀𝗸 𝘆𝗼𝘂 𝘁𝗼 𝗲𝘅𝗽𝗹𝗮𝗶𝗻. 𝗖𝗮𝗻 𝘆𝗼𝘂?
The 7-point MCP audit checklist every fintech CISO should run → [article link]
#MCPSecurity #FintechAI #AIGovernance #CISO #DORA
```
 
### Step 6 — Quality Checklist (Run Before Delivering)
 
- [ ] Title under 70 characters
- [ ] Title uses `:` not `—`
- [ ] Title is fresh, audience-led, not copied from source
- [ ] All subheadings are rephrased (not copied verbatim from source)
- [ ] Opening hook is strong — grabs attention in the first 2 lines
- [ ] Each section uses short paragraphs (max 2–3 sentences) + bullet points
- [ ] Article is **700–800 words** — not over, not under
- [ ] Core message and all key insights from the source are preserved
- [ ] Tone is conversational and engaging — not corporate or robotic
- [ ] No jargon left unexplained
- [ ] Keywords appear naturally (not stuffed)
- [ ] CTA includes both: link to blog + connect with Codiste (codiste.com)
- [ ] 5 relevant hashtags suggested for the article
- [ ] Authenticity check passed — every fact, stat, claim traces back to source
- [ ] LinkedIn caption is exactly 2 lines — Line 1 in Unicode bold, Line 2 with CTA
- [ ] Caption hook does NOT repeat or summarize the article — introduces higher-level angle
- [ ] Caption has 4–6 hashtags (separate from article hashtags)
- [ ] Publishing notes included
### Step 7 — Article Output Format
 
Deliver in this exact format:
 
```
════════════════════════════════════════
🔷 LINKEDIN ARTICLE — CODISTE
════════════════════════════════════════
 
TITLE:
[Confirmed LinkedIn title]
 
KEYWORDS TO USE AS HASHTAGS:
#Keyword1 #Keyword2 #Keyword3 #Keyword4 #Keyword5
 
════════════════════════════════════════
ARTICLE BODY:
════════════════════════════════════════
 
[Full article here]
 
════════════════════════════════════════
💬 LINKEDIN CAPTION:
════════════════════════════════════════
 
[Line 1 Unicode bold]
[Line 2 CTA with article link]
 
#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5
 
════════════════════════════════════════
📋 PUBLISHING NOTES:
════════════════════════════════════════
• Word count: ~[X] words
• Estimated read time: [X] min
• Remember to: add the blog URL in the CTA
```
 
**After delivering the article, immediately proceed to Phase 2 — Banner. Do NOT wait for the user to ask.**
 
---
 
## PHASE 2 — BANNER (article-specific, fully autonomous)
 
### Step 8 — Analyze the Article BEFORE Generating the Hero
 
**This is critical.** Every banner must look distinct. Before writing the Freepik prompt, mentally extract:
 
1. **Core argument** — what is the article *actually* saying? (Not just the topic)
2. **Unique metaphor** — what specific visual framing does this article carry? (Not a default "AI core + nodes")
3. **What the visual must communicate** — the one idea a reader should feel from the image
**Article-specific visual mappings (reference — never reuse for the same topic; always generate fresh):**
 
| Article topic | Visual metaphor used |
|---|---|
| Mistral vs Llama 3 (model comparison) | Two diverging glowing AI pathways — one streamlined/fast, one expansive/layered |
| Gmail tracking pixels / email reliability | Glowing envelope fragmenting into pixels with privacy lock + warning signals |
| ML vs GenAI (complementary architectures) | Data lattice flowing into generative neural burst via central energy stream |
| CISO checklist for MCP servers | Layered translucent shields around vault with audit-trail data streams + checkmarks |
| GPT-5.5 agentic AI | Central AI core with mechanical arms operating multiple interfaces simultaneously |
| AI for venture studios | Top-down strategic command center with portfolio of glowing product cards orbiting an AI core |
| Anthropic prompt workshop | Exploded translucent layered chip — deconstructed precision mechanism |
 
**Each banner must be visually distinct from prior banners.** If a new article happens to be on a similar topic, push the metaphor in a different direction.
 
**Topic → fallback style mapping** (use only when the article's metaphor is genuinely generic):
| Article topic | Visual style direction |
|---|---|
| Fintech / MCP / Finance | Glowing financial data streams, circuit boards, dark navy |
| AI Strategy / Business AI | Business executive with AI dashboards, corporate tech environment |
| Security / Cybersecurity | Digital vault, glowing security shield, red/blue warning signals |
| Healthcare AI | Clinical environment with AI overlays, clean white and blue |
| Blockchain / Web3 | Interconnected blockchain nodes, decentralised network |
| Logistics / Supply Chain | Aerial logistics network, connected routes, warm gold tones |
| General AI / ML | Neural network, glowing nodes, electric blue on dark navy |
| AI Frameworks / Dev Tools | Diverging pathways, structured pipeline vs collaborative agents |
 
### Step 9 — Generate the Hero Image via Freepik Mystic
 
**Use Freepik Mystic — fully autonomous, no Canva detour, no user upload step.**
 
#### Critical anti-text rules
 
AI image generators frequently hallucinate text/labels. Always include explicit suppression in the prompt:
 
> "Absolutely no text, no letters, no numbers, no logos, no labels anywhere in the image."
 
**Crucial nuance:** Do NOT name parts of your visual using textual labels in the prompt itself (e.g., "a layer labeled 'role-setting'"). The model will pick those words up and try to render them as text, producing garbled output. Describe layers/components only by their visual properties (geometry, color, position, glow), never by name.
 
**Hero prompt = LEFT PANEL VISUAL ONLY:**
- Describe only the visual scene for the left panel
- NEVER mention "right half white", "split composition", "white background", or any layout in the Freepik prompt
- The right panel (white, title, logo, codiste.com) is handled entirely by Python — NOT by the image model
#### Recommended Freepik settings
 
```
model: 'fluid'              # best prompt adherence for abstract conceptual visuals
aspect_ratio: 'square_1_1'  # gets cropped to 1200x1348 for left panel
resolution: '2k'             # 2048x2048 — clean for the banner
creative_detailing: 40       # balanced detail without HDR over-render
```
 
#### Workflow
 
```
1. freepik:create_image_mystic(...) → returns task_id
2. Wait 30 seconds (sleep)
3. freepik:get_mystic_task_status(task-id) → check until COMPLETED
4. Download the URL via curl with a brief retry loop
   (Freepik CDN sometimes 503s for ~10–20s after generation)
5. View the image to verify no text artifacts
6. If text/glitches present → regenerate with stronger anti-text wording
   AND no part-names mentioned in the prompt
```
 
#### Download retry pattern
 
```bash
# Freepik CDN returns 503 ("DNS cache overflow") for ~30-60s after generation.
# Real-world testing: ~50s of cumulative backoff was needed.
# Use a retry loop, NOT a single 15s sleep.
URL='URL_FROM_TASK_STATUS'
for i in 1 2 3 4 5; do
  sleep 20
  curl -sL -o /home/claude/freepik_hero.png "$URL"
  ftype=$(file /home/claude/freepik_hero.png)
  echo "attempt $i: $ftype"
  if echo "$ftype" | grep -q "PNG image"; then
    echo "✅ got PNG"; break
  fi
done
# If still ASCII text after 5 attempts → re-poll get_mystic_task_status for a refreshed URL
```
 
### Step 10 — Composite the Banner
 
Once the hero image is downloaded and verified:
- Use the confirmed article title — never ask for it again
- Load fonts + logo from ASSETS folder (with uploads fallback)
- Auto-fit BOTH lines (Line 1 Regular and Line 2 Bold), wrap to multiple lines if needed
#### Title Splitting Rule
 
Split title at the natural `:` colon point.
- **Line 1 (Regular):** Setup/context phrase before the colon — shorter, lighter
- **Line 2 (Bold):** Key payload after the colon — most impactful words
- Preserve all punctuation exactly
| Full title | Line 1 | Line 2 |
|---|---|---|
| Mistral vs Llama 3: A Practical Decision Guide for Product Leaders | Mistral vs Llama 3: | A Practical Decision Guide for Product Leaders |
| GPT-5.5: The Agentic Leap (and the 2x Price Tag) | GPT-5.5: | The Agentic Leap (and the 2x Price Tag) |
| You're Using Claude at 5%: Anthropic Just Showed Why | You're Using Claude at 5%: | Anthropic Just Showed Why |
| When to Use Machine Learning vs Generative AI: A Practical Guide for Businesses | When to Use Machine Learning vs Generative AI: | A Practical Guide for Businesses |
| The Ultimate CISO Checklist for Audit-Ready MCP Servers in Fintech | The Ultimate CISO Checklist for | Audit-Ready MCP Servers in Fintech |
 
If the title has no colon, find the natural break point at ~42–50% word mark.
 
#### Python Composition Code (with multi-line auto-fit for both lines)
 
```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
 
ASSETS = '/mnt/skills/user/codiste-linkedin-repurpose/assets/'
UPLOADS = '/mnt/user-data/uploads/'
W, H = 2400, 1348
 
def find_asset(name):
    for base in [ASSETS, UPLOADS]:
        p = base + name
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Asset {name} not found")
 
# Per session
HERO_FILE = '/home/claude/freepik_hero.png'   # from Freepik download
LINE1 = "Your title line 1:"                   # before colon
LINE2 = "Your bold payload after colon"        # after colon
slug = "your-banner-slug"                      # lowercase, hyphens
 
# ── Hero image (left panel, 1200 x 1348) ──────────────────────
hero_src = Image.open(HERO_FILE).convert('RGB')
scale = max(1200 / hero_src.width, H / hero_src.height)
dw, dh = int(hero_src.width * scale), int(hero_src.height * scale)
hero_resized = hero_src.resize((dw, dh), Image.LANCZOS)
ox, oy = (dw - 1200) // 2, (dh - H) // 2
hero_panel = hero_resized.crop((ox, oy, ox + 1200, oy + H))
 
# ── Logo — white pixels on black → render black on white ──────
# c_white_claude__2_.png = black background + white logo artwork
# Extract R>200 pixels (white logo art) → render as black [1,1,1,255]
# NEVER use c_black_claude__2_.png — fully black, unusable
logo_src = Image.open(find_asset('c_white_claude__2_.png')).convert('RGBA')
arr_l = np.array(logo_src)
rgba_l = np.zeros((arr_l.shape[0], arr_l.shape[1], 4), dtype=np.uint8)
rgba_l[arr_l[:, :, 0] > 200] = [1, 1, 1, 255]
logo = Image.fromarray(rgba_l, 'RGBA')
 
# CRITICAL: crop to bbox before resize to remove transparent padding
bbox = logo.getbbox()
if bbox:
    logo = logo.crop(bbox)
 
logo_h = 80
logo_w = int(logo.width * logo_h / logo.height)
logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
 
# ── Canvas ────────────────────────────────────────────────────
banner = Image.new('RGB', (W, H), (250, 250, 250))
banner.paste(hero_panel, (0, 0))
draw = ImageDraw.Draw(banner)
draw.rectangle([1200, 0, W, H], fill=(250, 250, 250))
draw.line([(1200, 0), (1200, H)], fill=(215, 215, 215), width=2)
banner.paste(logo, (W - logo_w - 64, 52), logo)
 
def tw(txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt); return bb[2] - bb[0]
def th(txt, fnt):
    bb = draw.textbbox((0, 0), txt, font=fnt); return bb[3] - bb[1]
 
MAX_W = 1200 - 80 - 40  # 1080px
 
def wrap_to_n(text, font, max_w, n_lines):
    """Wrap text into exactly n_lines, balanced widths. Returns None if impossible."""
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
                l1, l2, l3 = " ".join(words[:i]), " ".join(words[i:j]), " ".join(words[j:])
                if all(tw(l, font) <= max_w for l in [l1, l2, l3]):
                    widths = [tw(l, font) for l in [l1, l2, l3]]
                    spread = max(widths) - min(widths)
                    if best is None or spread < best[0]:
                        best = (spread, [l1, l2, l3])
        return best[1] if best else None
    return None
 
# Auto-fit Line 1 (Regular) — start 62px, may wrap to 2-3 lines
fs1 = 62
line1_lines = [LINE1]
while fs1 >= 32:
    font_l1 = ImageFont.truetype(find_asset('Satoshi-Regular.otf'), fs1)
    if tw(LINE1, font_l1) <= MAX_W:
        line1_lines = [LINE1]; break
    r2 = wrap_to_n(LINE1, font_l1, MAX_W, 2)
    if r2: line1_lines = r2; break
    r3 = wrap_to_n(LINE1, font_l1, MAX_W, 3)
    if r3: line1_lines = r3; break
    fs1 -= 2
 
# Auto-fit Line 2 (Bold) — start 88px, may wrap to 2-3 lines
fs2 = 88
line2_lines = [LINE2]
while fs2 >= 36:
    font_l2 = ImageFont.truetype(find_asset('Satoshi-Bold.otf'), fs2)
    if tw(LINE2, font_l2) <= MAX_W:
        line2_lines = [LINE2]; break
    r2 = wrap_to_n(LINE2, font_l2, MAX_W, 2)
    if r2: line2_lines = r2; break
    r3 = wrap_to_n(LINE2, font_l2, MAX_W, 3)
    if r3: line2_lines = r3; break
    fs2 -= 2
 
font_url = ImageFont.truetype(find_asset('Satoshi-Medium.otf'), 36)
 
# Text placement (vertically centred)
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
x_cur = W - total_url_w - PAD_R; url_y = H - 65
for ch in url_txt:
    draw.text((x_cur, url_y), ch, font=font_url, fill=BLACK)
    x_cur += tw(ch, font_url) + char_spacing
 
# Export
os.makedirs('/mnt/user-data/outputs', exist_ok=True)
banner.save(f'/mnt/user-data/outputs/codiste-banner-{slug}.png', 'PNG', dpi=(288, 288))
banner.save(f'/mnt/user-data/outputs/codiste-banner-{slug}.jpg', 'JPEG', quality=95, dpi=(288, 288))
print(f"✅ Banner saved! L1:{fs1}px L2:{fs2}px")
```
 
### Step 11 — Deliver the Banner
 
Always deliver **both files** via `present_files`:
```python
present_files([
    f'/mnt/user-data/outputs/codiste-banner-{slug}.png',
    f'/mnt/user-data/outputs/codiste-banner-{slug}.jpg'
])
```
 
---
 
## Full Workflow Summary (Autonomous)
 
```
USER PROVIDES INPUT (URL / blog / article / topic / tweet)
        ↓
Step 1: Extract / receive content
Step 2: Pick best title autonomously (short, colon, no em-dash, audience-led)
Step 3: Write article (700–800 words) — skip if user already wrote it
Step 4: Authenticity check
Step 5: Write single best caption (no options unless asked)
Step 6: Run quality checklist
Step 7: Deliver article output
        ↓
Step 8: ANALYZE the article — extract unique metaphor, NOT generic visual
Step 9: Generate hero via Freepik Mystic
        - Anti-text wording in prompt
        - Don't name visual components
        - Wait → poll → download with retry → verify
Step 10: Run compositor (auto-fit + multi-line wrap for both lines)
Step 11: Deliver PNG + JPG via present_files
        ✅ DONE
```
 
---
 
## Brand System (Non-Negotiable)
 
### Banner Specs
- **Size:** 2400 × 1348 px @ 288 DPI
- **Format:** PNG + JPG
### Colors
| Element | Color |
|---|---|
| Right panel background | `#FAFAFA` → RGB(250, 250, 250) |
| All text | `#010101` → RGB(1, 1, 1) |
| Divider line | `#D7D7D7` → RGB(215, 215, 215) |
 
### Typography — Satoshi ONLY
| Element | File | Start size |
|---|---|---|
| Line 1 | Satoshi-Regular.otf | 62px (auto-fit down + multi-line wrap) |
| Line 2 | Satoshi-Bold.otf | 88px (auto-fit down + multi-line wrap) |
| codiste.com | Satoshi-Medium.otf | 36px (-2% letter spacing) |
 
### Logo
- **File:** `c_white_claude__2_.png` from ASSETS — ONLY this file
- **Method:** Extract pixels where R > 200 → render as black [1,1,1,255]
- **Always crop to bbox before resizing** (removes transparent padding so the rendered logo isn't undersized)
- **Position:** Top-right, 80px tall, 64px from right, 52px from top
- **NEVER use** `c_black_claude__2_.png` — fully black, no extraction possible
- Both logo files have NO transparency — never rely on alpha channel for masking
### Layout
```
┌─────────────────────┬─────────────────────┐
│                     │    [LOGO]            │
│   HERO IMAGE        │   Line 1 text        │
│   (Freepik Mystic)  │   LINE 2 TEXT        │
│                     │          codiste.com │
└─────────────────────┴─────────────────────┘
     1200px                 1200px
     Left panel             Right panel
     = Freepik image        = Python compositor
```
 
---
 
## Things That Cause Failures (Avoid These)
 
| Mistake | What happens | Fix |
|---|---|---|
| Em-dash in title | Reads awkwardly at large size, breaks rhythm | Use `:` colon instead |
| Title over 70 chars | Wraps to 3+ lines, looks cramped | Keep titles 50–65 chars |
| Naming layers in Freepik prompt | Mystic renders garbled fake text | Describe by geometry/color/position only |
| Skipping anti-text wording | Random text appears in image | Always include "no text, no letters, no numbers, no logos, no labels" |
| Same metaphor for similar topics | Banners look indistinguishable | Always extract article-specific metaphor first |
| Downloading Freepik URL immediately | CDN 503s for ~30-60s after generation | Loop 5 × 20s sleep, verify with `file` each try |
| Asking angle when article exists | Wastes a turn | Angle Q only applies to fresh writing |
| Asking for 5-option title selection | Slows workflow | Pick best yourself unless user asks for options |
| Auto-fitting only one line | Long lines spill off the panel | Auto-fit + wrap BOTH lines independently |
| Forgetting `getbbox()` crop on logo | Rendered logo is undersized | Always `bbox = logo.getbbox(); logo = logo.crop(bbox)` before resize |
 
---
 
## What NOT to Do
 
- ❌ **Never ask the user to upload fonts or logo.** The assets folder is permanently seeded — files are at `/mnt/skills/user/codiste-linkedin-repurpose/assets/`. Asking is a workflow regression the user has explicitly forbidden.
- ❌ Never use Canva — Freepik Mystic handles hero generation autonomously
- ❌ Never use `—` (em-dash) in titles; always use `:` (colon)
- ❌ Never push titles to 100 chars; aim for 50–65, max 70
- ❌ Never present 5 title options or 5 caption options by default — pick the best yourself
- ❌ Never ask "topic-led or audience-led?" if the article is already written
- ❌ Never reuse the same hero metaphor for a new article — always analyze first
- ❌ Never name visual components in the Freepik prompt (causes garbled text)
- ❌ Never describe the white right panel / split layout in the Freepik prompt
- ❌ Never skip the banner phase — it's part of the workflow, not optional
- ❌ Never wait for user to ask for the banner — start hero generation right after article delivery
- ❌ Never ask for the title again before compositing — use confirmed title
- ❌ Never use `c_black_claude__2_.png` for the logo
- ❌ Never use `arr[:,:,0] > 0` for logo extraction — always `> 200`
- ❌ Never skip the `getbbox()` crop on the logo
- ❌ Never use fonts other than Satoshi
- ❌ Never auto-fit only one line — always auto-fit both Line 1 and Line 2 independently
- ❌ Never deliver only a preview — always export both PNG + JPG via `present_files`
- ❌ Never claim to perform actions the environment doesn't support (LinkedIn posting, scheduling, browser control)
- ❌ Never add stats, numbers, or companies not in the source content
- ❌ Never confirm a blog is already rephrased mid-session — if user asks for a new article, ask for the new content
---
 
## Boundary: What This Skill CANNOT Do
 
The skill cannot:
- Post content to LinkedIn (no LinkedIn connector / OAuth)
- Schedule posts at specific times (no time-triggered tools)
- Open browsers or control the user's device
- Upload images to LinkedIn or any external platform
If the user asks for any of these, explain plainly that the skill outputs a ready-to-publish bundle (article + caption + banner) and walk them through LinkedIn's native scheduler instead. **Don't pretend to "try"** — it's not a tooling gap, it's an architectural limit.
 
---
 
## Brand Constants
 
| Element | Value |
|---|---|
| Company name | Codiste |
| Website | codiste.com |
| Core services | AI/ML — Blockchain/Web3 — Web Development |
| Audience | CTOs, startup founders, tech-forward business owners |
| Tone | Conversational, credible, smart-colleague |
| CTA style | Warm invitation — never pushy |
 
---
 
## Lessons Learned (Updated April 2026 — post-seeding)
 
1. **Assets folder is seeded — do not ask for uploads.** All 4 required files (logo + 3 Satoshi fonts) live permanently in `/mnt/skills/user/codiste-linkedin-repurpose/assets/`. The user has explicitly forbidden mid-pipeline asset-upload interrupts. Load directly with `find_asset()` and proceed. Asking for uploads is the #1 way to break the autonomous-mode promise.
2. **Default to autonomous.** Skip the angle question, skip 5-option title presentations, skip 5-option captions. Pick the best, deliver, move on. Only present options when the user explicitly asks.
3. **Article analysis happens before the hero prompt.** Extract the article-specific metaphor. Different articles → different visuals. No generic templates.
4. **Freepik Mystic replaces Canva.** End-to-end autonomous, no user upload step in between.
5. **AI image models hallucinate text.** Always include explicit anti-text wording AND don't name visual components — the model picks those words up and renders them as garbled labels.
6. **Freepik CDN 503s persist longer than 15s.** Real-world testing showed ~50s of cumulative backoff was needed before the CDN served the PNG. Use a retry loop of 5 attempts × 20s sleep, not a single 15s wait. Always verify download with `file` command before proceeding.
7. **Titles: short + colon.** Aim for 50–65 chars. Use `:`, never `—`. The colon split looks cleaner at banner scale and gives the bold Line 2 more rhetorical weight.
8. **Auto-fit both lines independently.** Long Line 2 needs to wrap to 2–3 lines. Long Line 1 may also need wrapping when the pre-colon setup is long.
9. **Caption = meta-insight, not summary.** Line 1 introduces an angle the article doesn't cover. The reader should feel like clicking gives them more, not a recap.
10. **Don't fake capabilities.** If asked for posting/scheduling/browser actions, say plainly the skill can't do it. Offer the manual alternative. Never pretend.
11. **Logo always needs `getbbox()` crop before resize** — `c_white_claude__2_.png` has transparent padding that makes the rendered logo too small if not cropped first.
12. **Already-written article = skip Phase 1.** When user says "I have my article, just give me the banner", don't re-write or re-pitch.
13. **Word count 700–800 sweet spot.** Don't go over 800 words — articles past that underperform on LinkedIn. Run the Quality Checklist (Step 6) before every delivery.
14. **Subheadings must be fresh.** Never use the source's subheadings verbatim — always rephrase with a LinkedIn-friendly angle.
15. **Caption examples by topic exist for a reason.** Use the closest matching one as tone reference instead of inventing a new style every time.
16. **Title is automatic in compositor.** When the hero is ready, composite immediately — don't ask for the title again.
17. **Logo = `c_white_claude__2_.png` only.** R>200 extraction → black on white. Both logo files have no transparency.
---
 
## Project Folder Structure
 
```
/mnt/skills/user/codiste-linkedin-repurpose/
    ├── SKILL.md                    ← this file
    └── assets/
        ├── c_white_claude__2_.png  ← Codiste logo (white version)
        ├── Satoshi-Regular.otf     ← Line 1 font
        ├── Satoshi-Bold.otf        ← Line 2 font
        └── Satoshi-Medium.otf      ← codiste.com font
```
 
---
 
*Skill updated: April 2026 — full autonomous mode + Freepik Mystic integration*
 
*Patch — April 27, 2026 (post-first-real-run):*
*- Assets folder seeded permanently with logo + 3 Satoshi fonts. Asset-upload-asking is now explicitly forbidden in normal flow (only allowed on catastrophic asset-folder loss).*
*- Freepik CDN 503 retry pattern updated from single 15s wait to 5×20s loop (real-world test showed ~50s cumulative backoff was needed).*
*- Lessons Learned reordered to surface the "don't ask for assets" rule as #1.*
 
*Major changes from previous version:*
*- Switched from Canva (manual upload step) to Freepik Mystic (end-to-end autonomous)*
*- Removed angle clarifying question as a default (audience-led is default; topic-led only on explicit ask)*
*- Removed 5-title-option default (pick best autonomously; only present options on explicit ask)*
*- Removed 5-caption-option default (single best caption; options only on explicit ask)*
*- Added title length cap: 50–65 chars target, max 70 (was effectively 100)*
*- Replaced em-dash with colon as the canonical title splitter*
*- Added article-specific metaphor analysis as a hard requirement before hero generation*
*- Added anti-text Freepik prompt rules + don't-name-components rule*
*- Added Freepik CDN 503 retry pattern + `file` verification*
*- Added multi-line auto-fit for BOTH Line 1 and Line 2 (was only Line 2)*
*- Added intake flow table for different input types (URL / article / topic / tweet)*
*- Added "what this skill CANNOT do" boundary section (no posting, no scheduling, no browser)*
*- Added logo `getbbox()` crop step (was missing — caused undersized logos)*
*- Added asset fallback to /mnt/user-data/uploads/ when project folder isn't seeded*
 
*Preserved from previous version:*
*- Full Quality Checklist (Step 6) with all 18 items*
*- Opening hook examples (4 strong examples — including a new one for variety)*
*- Example section format code block*
*- Subheading rules detail (outcome-oriented, under 8 words, fresh)*
*- Keywords & SEO section*
*- 4 caption examples spanning different topic types (added 1 new — security/fintech)*
*- "What IS / What is NOT allowed" lists in authenticity check*
*- "Verify" 4-point list (Stats, Examples, Claims, New Ideas) in authenticity check*
*- Word count emphatic warning*
*- Topic → fallback style mapping table (for genuinely generic articles)*
*- Brand colors, typography, logo specs, layout diagram*
*- Original What NOT to Do entries about banner phase and Canva upload (adapted for Freepik)*