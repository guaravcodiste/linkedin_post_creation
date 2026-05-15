# Codiste LinkedIn Article — End-to-End Working Workflow

This documents the **exact process that works** for generating a LinkedIn article + Codiste-branded banner and uploading everything to Google Drive.

---

## Environment Facts (Do Not Change)

| Item | Value |
|---|---|
| Assets folder | `/home/user/linkedin_post_creation/` |
| Logo file | `c_white_claude.png` (NOT `c_white_claude_2.png`) |
| Fonts | `Satoshi-Regular.otf`, `Satoshi-Bold.otf`, `Satoshi-Medium.otf` |
| Output folder | `/home/user/linkedin_post_creation/outputs/` |
| Articles folder | `/home/user/linkedin_post_creation/articles/` |
| Hero image (downloaded) | `/home/user/freepik_hero.png` |
| Working branch | `claude/eloquent-albattani-ddloz` |
| Google Drive folder ID | `17lV2MRywwjxbodXo5tnShUTgS0EVplWE` |

---

## Step 1 — Read Google Sheet Data

Execute n8n workflow **`ql2PCnotM9XHrT6O`** (Read LinkedIn Sheet Data & Github):

```
mcp__n8n__execute_workflow(workflowId: "ql2PCnotM9XHrT6O", executionMode: "manual")
→ get executionId
→ mcp__n8n__get_execution(workflowId, executionId, includeData: true, nodeNames: ["Read Sheet"])
→ Extract content from json["Content Source"] field
```

Process rows **one at a time** — complete the full pipeline for row 1 before starting row 2.

---

## Step 2 — Read the Instruction File

```
mcp__github__get_file_contents(
  owner: "guaravcodiste",
  repo: "linkedin_post_creation",
  path: "codiste-linkedin-repurpose.md"
)
```

Follow all instructions in that file for article writing, title rules, caption format, and banner specs.

---

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
- The **core topic keyword** (e.g., "AI agents","generative AI","MCP","AI Product Management","VC")
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
 
### Step 3.1 — Authenticity Check
 
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
### Step 3.2 — Caption (Single Best Version)
 
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
 
### Step 3.3 — Quality Checklist (Run Before Delivering)
 
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
### Step 3.4 — Article Output Format
 
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
 
Save article to file:
```
/home/user/linkedin_post_creation/articles/{topic-slug}-linkedin-article.txt
```

Also copy to repo root for git tracking:
```
/home/user/linkedin_post_creation/{topic-slug}.txt
```

**After delivering the article, immediately proceed to step 4 — Banner. Do NOT wait for the user to ask.**

---

## Step 4 — Generate Freepik Hero Image (Async)

Use `mcp__freepik__create_image_mystic` with these exact settings:

```
model: "fluid"
aspect_ratio: "square_1_1"
resolution: "2k"
creative_detailing: "40"
prompt: [article-specific visual — see rules below]
```

**Prompt rules:**
- Describe only the LEFT PANEL visual scene
- Never mention "white panel", "split layout", "right side"
- Always end with: `"Absolutely no text, no letters, no numbers, no logos, no labels, no words, no signs anywhere in the image."`
- Describe components by geometry/color/position — never by name (causes garbled text)

Poll status until COMPLETED:
```
mcp__freepik__get_mystic_task_status(task-id: "...")
→ repeat until status == "COMPLETED"
→ note the generated URL from "generated" array
```

---

## Step 5 — Download Freepik Image via n8n → GitHub

**Why:** The Freepik CDN (`ai-statics.freepik.com`) is blocked by the container's outbound network policy. The n8n server has unrestricted access and can push to GitHub.

### 5a — Update the Download Workflow

Update n8n workflow **`yAsw8h7U4uB8Gr8e`** with the fresh Freepik URL:

```javascript
import { workflow, node, trigger, newCredential } from '@n8n/workflow-sdk';

const startTrigger = trigger({
  type: 'n8n-nodes-base.manualTrigger',
  version: 1,
  config: { name: 'Start', position: [-240, 0] },
  output: [{}]
});

const downloadImage = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.4,
  config: {
    name: 'Download Freepik Image',
    parameters: {
      url: 'PASTE_FREEPIK_URL_HERE',
      responseFormat: 'file',
      options: {}
    },
    position: [0, 0]
  },
  output: [{ data: 'binary image' }]
});

const pushToGitHub = node({
  type: 'n8n-nodes-base.github',
  version: 1.1,
  config: {
    name: 'Push Image to GitHub',
    parameters: {
      resource: 'file',
      operation: 'create',
      owner: { __rl: true, mode: 'name', value: 'guaravcodiste' },
      repository: { __rl: true, mode: 'name', value: 'linkedin_post_creation' },
      filePath: 'freepik-hero.png',
      binaryData: true,
      binaryPropertyName: 'data',
      commitMessage: 'Add Freepik hero image for banner',
      additionalParameters: {
        branch: { branch: 'claude/eloquent-albattani-ddloz' }
      }
    },
    credentials: { githubApi: newCredential('GitHub') },
    position: [300, 0]
  },
  output: [{ content: { path: 'freepik-hero.png', sha: 'abc' } }]
});

export default workflow('yAsw8h7U4uB8Gr8e', 'Download images')
  .add(startTrigger)
  .to(downloadImage)
  .to(pushToGitHub);
```

### 5b — Execute and Verify

```
mcp__n8n__execute_workflow(workflowId: "yAsw8h7U4uB8Gr8e", executionMode: "manual")
→ get_execution(includeData: false) → confirm status: "success"
```

**Note:** If `freepik-hero.png` already exists on the branch (from a previous run), change `operation: 'create'` to `operation: 'edit'` — GitHub will reject `create` on an existing file.

### 5c — Pull Image from GitHub into Container

```bash
git pull --rebase origin claude/eloquent-albattani-ddloz
```

The file is now at `/home/user/linkedin_post_creation/freepik-hero.png`.

Or download directly:
```bash
curl -L -o /home/user/freepik_hero.png \
  "https://raw.githubusercontent.com/guaravcodiste/linkedin_post_creation/claude/eloquent-albattani-ddloz/freepik-hero.png"
```

---

## Step 6 — Composite the Banner (Python/Pillow)

Install dependencies if needed:
```bash
pip install Pillow numpy -q
```

Run the compositor script — replace `LINE1`, `LINE2`, `slug` for each topic:

```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

ASSETS = '/home/user/linkedin_post_creation/'
W, H = 2400, 1348

LINE1 = "Your Title Prefix:"        # text before colon (Regular font)
LINE2 = "Your Bold Payload"          # text after colon (Bold font)
slug  = "your-topic-slug"            # lowercase-hyphenated for filenames

def find_asset(name):
    p = ASSETS + name
    if os.path.exists(p): return p
    raise FileNotFoundError(f"Asset {name} not found")

# Hero panel (left 1200px)
hero_src = Image.open('/home/user/freepik_hero.png').convert('RGB')
scale = max(1200 / hero_src.width, H / hero_src.height)
dw, dh = int(hero_src.width * scale), int(hero_src.height * scale)
hero = hero_src.resize((dw, dh), Image.LANCZOS)
ox, oy = (dw - 1200) // 2, (dh - H) // 2
hero_panel = hero.crop((ox, oy, ox + 1200, oy + H))

# Logo: extract white pixels (R>200) from c_white_claude.png → render near-black
logo_src = Image.open(find_asset('c_white_claude.png')).convert('RGBA')
arr = np.array(logo_src)
rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
rgba[arr[:, :, 0] > 200] = [1, 1, 1, 255]
logo = Image.fromarray(rgba, 'RGBA')
bbox = logo.getbbox()
if bbox: logo = logo.crop(bbox)        # MUST crop before resize
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

def tw(t, f): bb = draw.textbbox((0,0),t,font=f); return bb[2]-bb[0]
def th(t, f): bb = draw.textbbox((0,0),t,font=f); return bb[3]-bb[1]
MAX_W = 1200 - 80 - 40

def wrap_to_n(text, font, max_w, n):
    words = text.split()
    if n == 1: return [text] if tw(text,font)<=max_w else None
    if n == 2:
        best = None
        for i in range(1, len(words)):
            l1,l2 = " ".join(words[:i])," ".join(words[i:])
            if tw(l1,font)<=max_w and tw(l2,font)<=max_w:
                d = abs(tw(l1,font)-tw(l2,font))
                if best is None or d<best[0]: best=(d,[l1,l2])
        return best[1] if best else None
    if n == 3:
        best = None
        for i in range(1,len(words)-1):
            for j in range(i+1,len(words)):
                l1,l2,l3=" ".join(words[:i])," ".join(words[i:j])," ".join(words[j:])
                if all(tw(l,font)<=max_w for l in [l1,l2,l3]):
                    s=max(tw(l,font) for l in [l1,l2,l3])-min(tw(l,font) for l in [l1,l2,l3])
                    if best is None or s<best[0]: best=(s,[l1,l2,l3])
        return best[1] if best else None

# Auto-fit Line 1 (Regular, start 62px)
fs1=62; line1_lines=[LINE1]
while fs1>=32:
    f1=ImageFont.truetype(find_asset('Satoshi-Regular.otf'),fs1)
    if tw(LINE1,f1)<=MAX_W: line1_lines=[LINE1]; break
    r=wrap_to_n(LINE1,f1,MAX_W,2)
    if r: line1_lines=r; break
    r=wrap_to_n(LINE1,f1,MAX_W,3)
    if r: line1_lines=r; break
    fs1-=2
font_l1=ImageFont.truetype(find_asset('Satoshi-Regular.otf'),fs1)

# Auto-fit Line 2 (Bold, start 88px)
fs2=88; line2_lines=[LINE2]
while fs2>=36:
    f2=ImageFont.truetype(find_asset('Satoshi-Bold.otf'),fs2)
    if tw(LINE2,f2)<=MAX_W: line2_lines=[LINE2]; break
    r=wrap_to_n(LINE2,f2,MAX_W,2)
    if r: line2_lines=r; break
    r=wrap_to_n(LINE2,f2,MAX_W,3)
    if r: line2_lines=r; break
    fs2-=2
font_l2=ImageFont.truetype(find_asset('Satoshi-Bold.otf'),fs2)

font_url=ImageFont.truetype(find_asset('Satoshi-Medium.otf'),36)
BLACK=(1,1,1); PAD_R=80; gap=28; line_gap=12

l1h=[th(l,font_l1) for l in line1_lines]
l2h=[th(l,font_l2) for l in line2_lines]
total_h=sum(l1h)+line_gap*(len(l1h)-1)+gap+sum(l2h)+line_gap*(len(l2h)-1)
ty=(H-total_h)//2

y=ty
for i,line in enumerate(line1_lines):
    draw.text((W-tw(line,font_l1)-PAD_R,y),line,font=font_l1,fill=BLACK); y+=l1h[i]+line_gap
y=ty+sum(l1h)+line_gap*(len(l1h)-1)+gap
for i,line in enumerate(line2_lines):
    draw.text((W-tw(line,font_l2)-PAD_R,y),line,font=font_l2,fill=BLACK); y+=l2h[i]+line_gap

# codiste.com — -2% letter spacing
url_txt="codiste.com"
cs=-int(36*0.02)
uw=sum(tw(c,font_url) for c in url_txt)+cs*(len(url_txt)-1)
x=W-uw-PAD_R; uy=H-65
for c in url_txt:
    draw.text((x,uy),c,font=font_url,fill=BLACK); x+=tw(c,font_url)+cs

os.makedirs(f'{ASSETS}outputs', exist_ok=True)
out_png=f'{ASSETS}outputs/codiste-banner-{slug}.png'
out_jpg=f'{ASSETS}outputs/codiste-banner-{slug}.jpg'
banner.save(out_png,'PNG',dpi=(288,288))
banner.save(out_jpg,'JPEG',quality=95,dpi=(288,288))
print(f"✅ L1:{fs1}px L2:{fs2}px  PNG:{os.path.getsize(out_png)//1024}KB  JPG:{os.path.getsize(out_jpg)//1024}KB")
```

---

## Step 7 — Organize Files and Push to GitHub

```bash
mkdir -p articles outputs

# Copy article
cp {topic-slug}.txt articles/{topic-slug}-linkedin-article.txt

# Stage and commit
git add articles/ outputs/
git commit -m "Add LinkedIn article and banner for {topic}"

# Push (pull --rebase first if n8n pushed a commit to the branch)
git pull --rebase origin claude/eloquent-albattani-ddloz
git push -u origin claude/eloquent-albattani-ddloz
```

**Expected file structure in repo after push:**
```
outputs/
  codiste-banner-{slug}.png
  codiste-banner-{slug}.jpg
articles/
  {slug}-linkedin-article.txt
```

---

## Step 8 — Upload to Google Drive via n8n

Update workflow **`j5QLzZK1iT96yOql`** with the correct branch, filenames, and folder ID, then execute.

**Critical:** Use `n8n-nodes-base.googleDrive` (NOT HTTP Request with predefinedCredentialType). The Google Drive node auto-assigns credential **"Google Drive Gaurav"** correctly.

```javascript
import { workflow, node, trigger, newCredential, expr } from '@n8n/workflow-sdk';

const startTrigger = trigger({
  type: 'n8n-nodes-base.manualTrigger',
  version: 1,
  config: { name: 'Start', position: [288, -96] },
  output: [{}]
});

const buildFileList = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Build File List',
    parameters: {
      jsCode: "const base = 'https://raw.githubusercontent.com/guaravcodiste/linkedin_post_creation/claude/eloquent-albattani-ddloz';\nconst files = [\n  { fileName: 'codiste-banner-{slug}.png', url: base + '/outputs/codiste-banner-{slug}.png', mimeType: 'image/png' },\n  { fileName: 'codiste-banner-{slug}.jpg', url: base + '/outputs/codiste-banner-{slug}.jpg', mimeType: 'image/jpeg' },\n  { fileName: '{slug}-linkedin-article.txt', url: base + '/articles/{slug}-linkedin-article.txt', mimeType: 'text/plain' }\n];\nreturn files.map(f => ({ json: f }));"
    },
    position: [512, -96]
  },
  output: [{ json: { fileName: 'file.png', url: 'https://...', mimeType: 'image/png' } }]
});

const downloadFromGitHub = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.4,
  config: {
    name: 'Download from GitHub',
    parameters: {
      url: expr('{{ $json.url }}'),
      options: { response: { response: { responseFormat: 'file' } } }
    },
    position: [736, -96]
  },
  output: [{ data: 'binary' }]
});

const uploadToDrive = node({
  type: 'n8n-nodes-base.googleDrive',
  version: 3,
  config: {
    name: 'Upload to Drive',
    parameters: {
      resource: 'file',
      operation: 'upload',
      inputDataFieldName: 'data',
      name: expr('{{ $("Build File List").item.json.fileName }}'),
      folderId: { __rl: true, mode: 'id', value: '17lV2MRywwjxbodXo5tnShUTgS0EVplWE' },
      options: { simplifyOutput: true }
    },
    credentials: { googleDriveOAuth2Api: newCredential('Google Drive') },
    position: [960, -96]
  },
  output: [{ json: { id: 'file_id', name: 'filename' } }]
});

const sendGoogleChat = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.4,
  config: {
    name: 'Send Google Chat Success',
    executeOnce: true,
    parameters: {
      method: 'POST',
      url: 'https://chat.googleapis.com/v1/spaces/AAQAT72CHuU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=zCkj-AiFjFoSx0BdeA-HmQZ5ODwZCv91bLNNn6TeiIM',
      sendBody: true,
      specifyBody: 'json',
      jsonBody: { text: "✅ LinkedIn Upload Complete!\n\nTopic: {Article Title}\n\nFiles in Drive (folder: 17lV2MRywwjxbodXo5tnShUTgS0EVplWE):\n• codiste-banner-{slug}.png\n• codiste-banner-{slug}.jpg\n• {slug}-linkedin-article.txt\n\n🎉 Pipeline done!" },
      options: {}
    },
    position: [1184, -96]
  },
  output: [{ json: { name: 'message' } }]
});

export default workflow('j5QLzZK1iT96yOql', 'LinkedIn Content — Upload to Google Drive (Artical)')
  .add(startTrigger)
  .to(buildFileList)
  .to(downloadFromGitHub)
  .to(uploadToDrive)
  .to(sendGoogleChat);
```

Execute:
```
mcp__n8n__execute_workflow(workflowId: "j5QLzZK1iT96yOql", executionMode: "manual")
→ poll get_execution(includeData: false) until status: "success"
```

---

## Key Rules That Prevent Failures

| Rule | Why |
|---|---|
| Use `n8n-nodes-base.googleDrive` node for Drive uploads | HTTP Request with `predefinedCredentialType` loses its credential ID when the workflow is rewritten via SDK — Drive node auto-assigns correctly |
| Never fetch binary execution data from n8n via `get_execution` | Large binaries (2K PNG = 3MB+) always time out the MCP tool |
| Freepik CDN is outbound-blocked — always route via n8n → GitHub → raw.githubusercontent.com | Direct `curl` to `ai-statics.freepik.com` returns 403 |
| Pull `--rebase` before pushing if n8n committed to the same branch | n8n GitHub node commits directly; diverged history breaks the push |
| Logo file is `c_white_claude.png` — always `getbbox()` crop before resize | Transparent padding makes logo appear undersized without crop |
| Always set `executeOnce: true` on the Google Chat node | Without it, the notification fires once per file (3×) |
| `operation: 'create'` on GitHub node fails if file exists — use `'edit'` for reruns | GitHub API 422 on duplicate create |

---

## Workflow & Asset Reference

| Item | ID / Path |
|---|---|
| Read Sheet workflow | `ql2PCnotM9XHrT6O` |
| Download Image workflow | `yAsw8h7U4uB8Gr8e` |
| Google Drive upload workflow | `j5QLzZK1iT96yOql` |
| Google Drive folder | `17lV2MRywwjxbodXo5tnShUTgS0EVplWE` |
| Google Chat webhook space | `AAQAT72CHuU` |
| GitHub credential in n8n | `Gaurav` (type: `githubApi`) |
| Google Drive credential in n8n | `Google Drive Gaurav` (type: `googleDriveOAuth2Api`) |
| Instruction file | `codiste-linkedin-repurpose.md` in repo root |

---