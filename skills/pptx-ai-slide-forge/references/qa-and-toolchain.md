# QA and toolchain

The QA loop is the part of the skill that makes its output trustworthy. Run every
check for real and report what actually happened.

## 1. Geometry lint

`scripts/qa_check.py` (or `verify()` inside `build_deck.py`):

- every shape within slide bounds (tiny 1000 EMU tolerance);
- no two text-bearing shapes overlapping by more than **0.05 sq in**;
- slide count sanity.

A clean lint is a precondition for render QA, not a substitute for it.

## 2. Text QA

```bash
python3 scripts/qa_check.py deck.pptx --slides 8 \
    --contains "NOT RUN:4" --contains "GAP" --forbid "Спасибо" --forbid "Thank you"
```

- Extraction: markitdown (`pip install "markitdown[pptx]"`), python-pptx fallback.
- Assert: slide count, key strings present (titles, statuses), forbidden strings
  absent (no "Thank you" slide, no invented metrics).
- Honest statuses matter: an evidence matrix with `NOT RUN` rows is correct output;
  replacing them with green checks because "it looks better" is a defect.

## 3. Render QA (visual)

```bash
bash scripts/render_qa.sh /abs/path/deck.pptx qa
# → qa/<basename>.001.png, .002.png, ...
```

Then **open and read every PNG**. Checklist per slide:

- clipped or wrapping text (Russian + tracking wraps earlier than English);
- overlaps (the lint threshold hides small kisses between cards);
- contrast: text zones dark enough on the background;
- style fidelity: one accent family, no random hues, texture in corners only.

Fix the build, re-render, re-inspect. **Max 3 iterations**; report what was fixed in
each round. If a defect survives three rounds, report it honestly instead of shipping.

### Known platform pitfalls (verified 2026-10-29, macOS)

| Pitfall | Reality |
|---|---|
| PowerPoint AppleScript `save as PNG` | exits 0, writes **nothing** (destination and sandbox container stay empty). Do not retry — use Keynote. |
| Keynote render naming | files are named after the **output directory basename**: `qa/qa.001.png`, `qa.002.png`, ... |
| Keynote vs PowerPoint text metrics | Keynote wraps **earlier**. Leave ≥ 15% width buffers on text boxes and test caps+tracking labels at 1 line. |
| LibreOffice / poppler | not installed by default on this pipeline; not required. |
| Fonts | "Helvetica Neue" is native on macOS with full Cyrillic; "Inter" may be absent and silently substituted. |

## 4. Background luminance sanity

`make_textures.py` prints mean luminance for each declared check zone. Targets:
title strip ≤ ~12/255, body zones ≤ ~22/255, texture corners 15–30. With
`STRICT = True` the script fails when a check zone exceeds `MAX_TEXT_ZONE_LUM`.
The report proves darkness; visual inspection proves style. Both are required.

## 5. Toolchain facts

| Tool | Status | Notes |
|---|---|---|
| python-pptx 1.0.2 | ✅ verified | glass alpha, `spc` tracking, table borders via XML |
| Pillow 11.2.1 + numpy | ✅ verified | background engine (LANCZOS, GaussianBlur) |
| markitdown 0.1.9 | ✅ verified | text QA (`markitdown[pptx]`) |
| Keynote | ✅ verified | render QA via AppleScript |
| Microsoft PowerPoint | ⚠️ | installed but its AppleScript export silently fails; fine for manual viewing |
| LibreOffice, poppler | ❌ absent | not required |
| `aggdraw` | ❌ absent | **not needed** — engine is pure numpy + PIL |
| pptxgenjs | optional | found in `~/node_modules`; not used by this skill |

## 6. Installing the skill for agents

| Agent | Path |
|---|---|
| Claude Code (project) | `.claude/skills/pptx-ai-slide-forge/` |
| Claude Code (user) | `~/.claude/skills/pptx-ai-slide-forge/` |
| Codex | `.agents/skills/pptx-ai-slide-forge/` |

```bash
git clone https://github.com/<you>/pptx-AI-Slide-Forge.git
cp -R pptx-AI-Slide-Forge/skills/pptx-ai-slide-forge .claude/skills/
```

Commit `__pycache__`-free: the repo `.gitignore` already excludes `__pycache__/`,
`*.pyc`, `qa/`, `*.pptx`, `*.pdf` (renders and builds are reproducible artifacts,
not sources).
