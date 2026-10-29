---
name: pptx-ai-slide-forge
description: >
  Forge premium dark-tech PPTX presentations: procedurally generated backgrounds
  (liquid glass ribbons or ribbed metallic surfaces), glassmorphism and electric-accent
  cards, strict content discipline (action titles, ghost deck test, ~40 words per
  slide), and an honest render-based QA loop. Use when the user asks to create,
  redesign, or QA a .pptx presentation, slide backgrounds, or a deck visual style.
  Do not use for web pages, Word documents, or plain text-only slides without
  visual design.
license: MIT
metadata:
  author: pptx-AI-Slide-Forge contributors
  version: "1.0.0"
---

# pptx-ai-slide-forge

## Overview

Builds finished 16:9 PPTX decks the way a design engineer would: a user-approved slide
outline first, then procedurally generated backgrounds with preserved dark text zones,
then a python-pptx build (glass cards, electric accent cards, evidence tables, flows),
then an honest QA loop — every slide rendered to PNG and actually inspected, text
extracted and checked, geometry linted. Everything in `scripts/` ran in production on a
real 8-slide deck before being packaged.

## When to Use

- "Сделай презентацию / build a deck" from notes, a document, or a data file
- Redesign or restyle an existing deck (new visual style, new backgrounds)
- QA an existing .pptx (text extraction, geometry lint, render inspection)
- Generate slide background art (liquid ribbons, ribbed metal) without stock images

## Workflow

Follow all seven steps. Do not skip gates.

### 1. Intake and outline (gate: user approval)

- Read the source material fully. Compress it into 7–10 slides with **action titles**
  (complete sentences stating the takeaway). Run the ghost deck test: reading only the
  titles in sequence must tell the whole argument.
- Present the outline as a table: #, action title, content, visual form.
- Ask remaining decisions **in one batch** (slide count, deck title, author block,
  workspace/commit policy), each with options and your recommendation. The user
  typically approves recommendations as a batch ("ок на все рекомендации").

### 2. Style

- Pick a built-in style from [`references/styles.md`](references/styles.md) or write a
  custom spec using the recipe at the end of that file.
- Extract the style into theme tokens (colors, font, radius, alpha) at the top of the
  build script. Use exact HEX values; approximations break the aesthetic.

### 3. Backgrounds

- Write per-slide background configs (see
  [`references/background-engine.md`](references/background-engine.md) for the full
  parameter reference and tuned values). Choose the engine per slide: `liquid`
  (layered glass ribbons) or `ribbed` (metallic surfaces).
- Run: `python3 scripts/make_textures.py --config <config.py> --out assets`
- Check the printed luminance report: title strips and body zones must stay dark
  (target ≤ ~22/255); texture lives in corners and edges. Iterate visually — open the
  generated PNGs and look at them — before building the deck.

### 4. Build

- Adapt `scripts/build_deck.py` (the reference implementation): theme tokens at the
  top, then one section per slide. Keep the helper library (`txt`, `card`, `pill`,
  `accent_card`, `footer`, `verify`) as is — it encodes the QA-relevant invariants.
- Run the build; `verify()` must print clean (bounds + text overlaps).

### 5. Render QA (gate: every slide inspected)

- `bash scripts/render_qa.sh /abs/path/deck.pptx qa` → PNG per slide (Keynote).
- **Read every render.** Check: clipped or wrapping text, overlaps, contrast, style
  fidelity, background text zones. Collect a fix list, fix the build, re-render.
- Max 3 iterations; report what was fixed each round.

### 6. Text QA

- `python3 scripts/qa_check.py deck.pptx --slides N --contains "KEY TEXT" --forbid "Спасибо"`
- Verify slide count, key strings (titles, statuses), forbidden strings (no "Thank
  you" slide, no invented facts).

### 7. Deliver

Report: deck path, QA results (what was verified and how), files created, known
limitations (e.g., render interpreter differs from the user's PowerPoint). Never claim
checks passed that were not run.

## Generating styles and backgrounds

How to produce *different* styles and backgrounds — the two generative acts of this
skill. Full details live in the references; this section is the working instruction.

### A new style = a JSON specification

1. Collect inputs: 1–3 reference screenshots, brand HEX colors (or permission to
   derive), mood words, audience, deck language (the font must render Cyrillic if
   the deck is Russian).
2. Have the AI draft the style JSON per the recipe in
   [`references/styles.md`](references/styles.md) → *"Authoring a new style JSON with
   AI"* (prompt template included). Required fields: canvas + palette with
   `dominant_color_ratio` (one accent family!), layered `background_system`
   (base gradient + atmospheric glows + volumetric forms — never a flat gradient),
   `glass_card_system` with explicit opacities, single-font `typography` (headline
   weight ≤ 500), `critical_visual_rules` and `negative_prompt` naming the banned
   failure modes.
3. Convert px → pt: **1 px at 1920 = 0.5 pt** on the 13.333 × 7.5 in slide.
4. Validate the spec before mass production: fill every field (an empty field is
   style drift), build **one dense test slide**, render it, compare against the
   references, refine the JSON — not the slide.

### New backgrounds = per-slide configs for `make_textures.py`

- Pick the engine per slide: `liquid` (layered glossy ribbons — the default for
  content and heroes) or `ribbed` (vertical metallic surface — covers).
- A liquid slide config is: base gradient stops + 2 corner glows + 3–5 ribbons
  anchored by `gates` to corners/edges + `darken` zones over the title strip and
  body + vignette. Ribbon fields: `y0/slope/waves` shape the centerline, `w0` the
  thickness (a ×1.5 factor is applied inside the engine), `c1→c2` the color
  progression along the slide, `depth: back|mid|front` the pre-blur layering, `rim`
  the icy specular color.
- Hard constraints: darken the title strip (strength ≥ 0.4); body text zones stay
  ≤ ~22/255 luminance (the script prints the report); bright elements only in
  corners/edges, never behind body text; ribbons are wide glass bodies with narrow
  icy rims — thin neon lines are a rejected failure mode.
- After generating: **open the PNGs and look at them**, then iterate the config.
  Numbers prove darkness; only eyes prove style.

## Hard Rules

- Never invent facts, numbers, dates, authors, or verification statuses. An evidence
  matrix with honest `NOT RUN` statuses is better than a fabricated green report.
- One accent color family per style; exact HEX from the spec; hierarchy via size and
  color, never bold; no icons or clip-art; no slide borders; body text ≥ 12.5pt,
  micro labels ≥ 9.5pt.
- Backgrounds must keep text zones dark (luminance sanity); texture is concentrated
  in corners and edges; negative space 35–60%.
- Letter-spacing is set via DrawingML XML (`spc`), see
  [`references/slide-patterns.md`](references/slide-patterns.md).
- Keynote wraps text earlier than PowerPoint — leave width buffers on every text box.
- Fix loops: reviewer findings go back to the builder, then re-render. Reviewer
  findings = not done.

## References

| File | Read when |
|---|---|
| [`references/styles.md`](references/styles.md) | choosing or writing a visual style (two full specs + recipe) |
| [`references/background-engine.md`](references/background-engine.md) | writing background configs; tuning ribbons/ribs; luminance targets |
| [`references/slide-patterns.md`](references/slide-patterns.md) | laying out slides; glass/accent recipes; tables; XML tricks |
| [`references/qa-and-toolchain.md`](references/qa-and-toolchain.md) | rendering, text QA, lint, dependencies, platform pitfalls |

## Scripts

```bash
# backgrounds from a config module
python3 scripts/make_textures.py --config examples/sdd-deck/textures_config.py --out assets

# render slides to PNG (Keynote; PowerPoint pitfall documented inside)
bash scripts/render_qa.sh /abs/path/deck.pptx qa

# text QA + geometry lint
python3 scripts/qa_check.py deck.pptx --slides 8 --contains "NOT RUN:4" --forbid "Спасибо"
```

## Output Format

- `<name>.pptx` (16:9, 13.333 × 7.5 in)
- `qa/<name>.001.png …` renders used for visual QA
- A QA report: geometry lint result, text check results, render inspection findings
  and fixes, luminance report

## Example

[`examples/sdd-deck/`](examples/sdd-deck/) — the worked extraction source: an
8-slide technical deck ("Spec-Driven Development with AI agents", NovaPay Liquid
Electric Blue), with per-slide background configs and the content outline.
