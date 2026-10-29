---
name: pptx-ai-slide-forge
description: >
  Forge premium dark-tech PPTX presentations: procedurally generated backgrounds
  (liquid glass ribbons, ribbed metal), composable shape layers (HUD rings, dot
  fields, wireframe terrain), glassmorphism and electric-accent cards, strict
  content discipline (action titles, ghost deck test, ~40 words per slide), and an
  honest render-based QA loop. Use when the user asks to create, redesign, or QA a
  .pptx presentation, slide backgrounds, or a deck visual style. Do not use for web
  pages, Word documents, or plain text-only slides without visual design.
license: MIT
metadata:
  author: pptx-AI-Slide-Forge contributors
  version: "1.1.0"
---

# pptx-ai-slide-forge

## Overview

Builds finished 16:9 PPTX decks the way a design engineer would: a user-approved
slide outline first, then procedurally generated backgrounds with preserved dark text
zones, then a python-pptx build (glass cards, electric accent cards, evidence tables,
flows, composable shape layers), then an honest QA loop — every slide rendered to PNG
and actually inspected, text extracted and checked, geometry linted. Everything in
`scripts/` ran in production on a real 8-slide deck before being packaged.

The skill ships **four complete style specifications** (`references/styles.md`):
Midnight Electric Blue, NovaPay — Liquid Electric Blue, Clean Blue Tech (light
corporate), Dark Emerald Strategy — plus a recipe for authoring new styles with AI.

## When to Use

- "Сделай презентацию / build a deck" from notes, a document, or a data file
- Redesign or restyle an existing deck (new visual style, new backgrounds)
- QA an existing .pptx (text extraction, geometry lint, render inspection)
- Generate slide background art (liquid ribbons, ribbed metal, HUD rings,
  wireframe terrain) without stock images

## Workflow

Follow all seven steps. Do not skip gates.

### 1. Intake and outline (gate: user approval)

- Read the source material **fully** (do not skim: the outline quality depends on
  facts only the source contains).
- Compress into 7–10 slides with **action titles** — complete sentences stating the
  takeaway ("A correctly implemented guess is still a guess"), never topic labels
  ("Problem"). Run the ghost deck test: reading only the titles in sequence must
  tell the whole argument. If it does not, fix the outline — do not build.
- Present the outline as a table: `# | action title | content | visual form`, plus
  the source-to-outline mapping (what was cut and why — "one argument, not the whole
  paper").
- Ask remaining decisions **in one batch** (slide count, deck title, author block,
  language, workspace/commit policy), each with options and your recommendation.
  Record which recommendations were accepted — they are binding decisions, not
  suggestions.

### 2. Style

- Pick a built-in style from [`references/styles.md`](references/styles.md) or write
  a custom spec using the recipe at the end of that file.
- Light styles (e.g. Clean Blue Tech) skip the texture engine: flat backgrounds +
  vector decor overlays; the luminance logic inverts (keep text zones clean-light,
  accents sparse at ~15%).
- Extract the style into theme tokens (colors, font, radius, alpha) at the top of
  the build script. Use exact HEX values; approximations break the aesthetic.
- Convert px → pt: **1 px at 1920 = 0.5 pt** on the 13.333 × 7.5 in slide; radius
  18 px = 0.125 in; `spc` = 1/100 pt (`int(-0.04 * size_pt * 100)` for headlines).

### 3. Backgrounds

- Write per-slide background configs (full parameter reference:
  [`references/background-engine.md`](references/background-engine.md)). Choose the
  engine per slide: `liquid` (layered glass ribbons; default) or `ribbed` (metallic
  surfaces), and compose `layers` for shapes (HUD rings, dot fields, wireframe
  terrain — see the matrix below).
- Run: `python3 scripts/make_textures.py --config <config.py> --out <dir>`
- Check the printed luminance report: title strips ≤ ~12/255, body zones ≤ ~22/255;
  texture lives in corners and edges.
- **Open the generated PNGs and look at them** before building the deck. Numbers
  prove darkness; only eyes prove style.

### 4. Build

- Adapt `scripts/build_deck.py` (the reference implementation): theme tokens at the
  top, one clearly-marked section per slide. Keep the helper library (`txt`, `card`,
  `accent_card`, `pill`, `dot`, `rect`, `footer`, `verify`) as is — it encodes the
  QA-relevant invariants (glass alpha XML, letter-spacing, cell-border order,
  geometry lint).
- Run the build; `verify()` must print clean (bounds + text overlaps ≤ 0.05 sq in).

### 5. Render QA (gate: every slide inspected)

- `bash scripts/render_qa.sh /abs/path/deck.pptx qa` → PNG per slide (Keynote).
- **Read every render.** Collect a numbered fix list (slide + defect), fix the
  build, re-render. Max 3 iterations; report what was fixed in each round.
- Typical first-pass defects: label capsules wrapping (caps + tracking need ~15%
  width buffer), pill labels wrapping (drop tracking or widen), text boxes kissing
  (0.05 in overlaps the lint tolerates visually).

### 6. Text QA

- `python3 scripts/qa_check.py deck.pptx --slides N --contains "KEY" --forbid "…"`
- Verify: slide count, key strings (titles, statuses), forbidden strings (no
  "Thank you" slide, no invented facts).

### 7. Deliver

Report: deck path, QA results (what was verified and how), files created, known
limitations (e.g., render interpreter differs from the user's PowerPoint). Never
claim checks passed that were not run.

## Design decision guide

Map content to visual treatment; one idea per slide.

| Content | Visual treatment |
|---|---|
| Numbers, KPIs, targets | Metric cards, 3 columns, large accent numbers |
| Comparison (A vs B) | Two-panel split or comparison matrix |
| Process / lifecycle | Three-step flow, vertical chain with dots, quarterly roadmap |
| Status / verification | Evidence matrix table + finding card (CLAIM → GAP) |
| Case / narrative | Case card with numbered rows + question pill stack |
| Concept hierarchy | Level cards: tag → header → example → control |
| Knowledge classification | Fact-card grid (2×3), tags FACT/UNKNOWN/… |
| Roles / responsibilities | Role cards + capsule row |
| Section break | Divider: centered ring emblem or arc field |

Background per slide role:

| Slide | Background treatment |
|---|---|
| Hero cover | full liquid/ribbed art; dark headline zone (left-bottom) |
| Content | corner-anchored ribbons/layers; darken title strip + body |
| Section divider | centered emblem (ring + arc field), quiet everywhere else |
| Data slide | quiet base, one wireframe/mesh corner band |

## Generating styles and backgrounds

How to produce *different* styles and backgrounds — the two generative acts of this
skill. Full details live in the references; this section is the working instruction.

### A new style = a JSON specification

1. Collect inputs: 1–3 reference screenshots, brand HEX colors (or permission to
   derive), mood words, audience, deck language (the font must render Cyrillic if
   the deck is Russian).
2. Have the AI draft the style JSON per the recipe in
   [`references/styles.md`](references/styles.md) → *"Authoring a new style JSON
   with AI"* (prompt template included). Required fields: canvas + palette with
   `dominant_color_ratio` (one accent family!), layered `background_system`
   (base gradient + atmospheric glows + volumetric forms — never a flat gradient),
   `glass_card_system` with explicit opacities, single-font `typography` (headline
   weight ≤ 500), `critical_visual_rules` and `negative_prompt` naming the banned
   failure modes.
3. Convert px → pt (1 px at 1920 = 0.5 pt) and validate the spec before mass
   production: fill every field (an empty field is style drift), build **one dense
   test slide**, render it, compare against the references, refine the JSON — not
   the slide.

### New backgrounds = per-slide configs for `make_textures.py`

- Pick the engine per slide: `liquid` (layered glossy ribbons — the default for
  content and heroes) or `ribbed` (metallic surfaces — covers). The palette is
  data: the same engine produced blue (NovaPay) and emerald (Dark Emerald) decks.
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

### Composable shape layers (v1.1)

A slide-level `layers` list is drawn over the liquid base and **under** the text
darken pass. Vocabulary: `path_ribbon` (arc / ring / bezier swoosh — glossy body with
icy edge speculars on any curvature), `dots` (radial-falloff dot grid), `arc_field`
(concentric HUD arcs), `wireframe` (projected 3D heightfield terrain). Blend modes:
`normal` or `screen` (luminous overlay).

Decision matrix:

| Slide type | Layers |
|---|---|
| Hero cover | one `path_ribbon` swoosh or 1–2 rings, plus liquid ribbons |
| Section divider | centered ring emblem (`path_ribbon` ring + `arc_field`) |
| Content slide | `dots` field in one corner (+ optional quiet `arc_field`) |
| Data / terrain slide | `wireframe` heightfield in a corner band |

Restraint rules: ≤ 2 shape families per slide; the hero shape is singular; layers
must not sit behind body text (the darken pass helps, but do not rely on it); quiet
layers at `alpha` ≤ 0.5. Full parameter reference:
[`references/background-engine.md`](references/background-engine.md).

## Failure modes and fixes

Every row below shipped once. Symptom → cause → fix.

| Symptom | Cause | Fix |
|---|---|---|
| Thin neon "laser" lines | ribbon width too small; rims too wide | `w0` ≥ 0.5 in; rim sigma ≤ 0.09; body floor 0.62 |
| Flat, cheap background | no base gradient stops; missing corner glows | 4-stop diagonal base + 2 corner glows + one back ribbon |
| Text unreadable over art | darken zones missing or weak | title strip strength ≥ 0.4, body ≥ 0.2; re-check luminance |
| Hue drift (purple/pink) | palette outside the accent family | clamp to style spec; extend `negative_prompt` |
| Wireframe mesh invisible | strokes drawn before polygon fills (`ImageDraw` replaces pixels) | two passes: all polygons first, then all strokes (RGBA overlay) |
| Ellipse instead of rounded rect | capsule adjustment 0.5 on a near-square shape | `adjustment = radius / min(w, h)` |
| Labels wrap to two lines | no width buffer for caps + tracking | ≥ 15% width buffer; test every caps label at 1 line |
| Boxes flagged as overlapping | generous boxes touching | shrink heights to content; keep ≥ 0.15 in gaps |
| Low-contrast captions on colored slides | dark text on accent fill | invert: white/light text on accent, muted only on base |

## Content discipline

- **Action titles** — complete sentences stating the takeaway; ghost deck test must
  pass before building.
- **≤ ~40 words** of body text per slide (exhibits/tables excluded). Telegraphic
  phrasing is fine; walls of text are not.
- **One exhibit per slide**; annotate the key finding directly on it.
- **Honest statuses**: `NOT RUN` and `GAP` are valid, valuable statuses. Never
  replace them with green because "it looks better".
- **Never invent** facts, numbers, dates, authors, or verification results.
- **Typography**: typographic quotes («», “”), em dashes (—), middots (·) — copy
  text exactly; do not straighten quotes or hyphenate dashes.
- **Conclusions last**; no "Thank you" slide. The final slide stays up for Q&A.
- **Citations**: source lines under tables/charts in muted 9–10 pt.

## Hard Rules

- Content discipline rules above are gates, not suggestions.
- One accent color family per style; exact HEX from the spec; no icons or clip-art;
  no slide borders.
- Body text ≥ 12.5 pt, micro labels ≥ 9.5 pt.
- Fix loops: reviewer findings go back to the builder, then re-render. Reviewer
  findings = not done.
- Git: make intermediate commits per completed unit (engine, example, docs) — the
  user reviews the history.

## References

| File | Read when |
|---|---|
| [`references/styles.md`](references/styles.md) | choosing or writing a visual style (four full specs + AI-authoring recipe) |
| [`references/background-engine.md`](references/background-engine.md) | writing background configs; tuning ribbons/layers; luminance targets |
| [`references/slide-patterns.md`](references/slide-patterns.md) | laying out slides; glass/accent recipes; tables; vector decor; XML tricks |
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
  and fixes per round, luminance report

## Example

[`examples/sdd-deck/`](examples/sdd-deck/) — the worked extraction source: an
8-slide technical deck ("Spec-Driven Development with AI agents", NovaPay Liquid
Electric Blue), with per-slide background configs and the content outline.
[`examples/english-demo/`](examples/english-demo/),
[`examples/clean-blue-tech/`](examples/clean-blue-tech/) and
[`examples/dark-emerald-strategy/`](examples/dark-emerald-strategy/) are compact
3-slide demos per style; [`examples/shape-gallery/`](examples/shape-gallery/)
showcases the v1.1 shape layers.
