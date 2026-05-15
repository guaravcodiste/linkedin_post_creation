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

## Step 3 — Write the LinkedIn Article

Follow `codiste-linkedin-repurpose.md` Phase 1 exactly:

- **Title:** Short + punchy, 50–65 chars, use `:` not `—`, audience-led (CTO/founder POV)
- **Article:** 700–800 words, strong hook, 3 subheadings with bullets, CTA block at end
- **Caption:** 2 lines — Line 1 in Unicode bold, Line 2 with CTA arrow

Save article to file:
```
/home/user/linkedin_post_creation/articles/{topic-slug}-linkedin-article.txt
```

Also copy to repo root for git tracking:
```
/home/user/linkedin_post_creation/{topic-slug}.txt
```

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

*Documented: May 2026 — based on first successful end-to-end run*
