---
name: deck-polish
description: >
  Improve an existing .pptx: render + audit (geometry, text, contrast, style
  consistency), propose a batched improvement plan with recommendations, apply
  fixes (python-pptx patch in place, or rebuild via pptx-ai-slide-forge when
  the deck was built by it), re-render and verify. Use when the user has an
  existing deck to improve or restyle. Do not use for from-scratch builds
  (pptx-ai-slide-forge + deck-intake) or for design dialogue (deck-intake).
license: MIT
metadata:
  author: pptx-AI-Slide-Forge contributors
  version: "1.0.0"
---

# deck-polish

## Overview

The improvement half of the deck pipeline: take an existing .pptx, render it,
audit it honestly (geometry, text, contrast, style consistency), propose a
batched improvement plan with recommendations, apply it, and re-verify with the
same QA machinery the forge uses. The deck the user has is the source of truth
for content — polish never invents or deletes content without an explicit user
decision.

## When to Use

- "Улучши эту презентацию" — the user provides an existing .pptx
- Restyle an existing deck into one of the built-in styles
- A deck fails rendering/QA and needs diagnosis + fixes
- Periodic hygiene: overlaps, contrast, consistency before a talk

## Workflow

### 1. Audit (facts first)

- **Render**: every slide to PNG (Keynote via `render_qa.sh` from
  `../pptx-ai-slide-forge/scripts/` — or any available renderer); PowerPoint
  AppleScript export silently fails on macOS — documented pitfall.
- **Geometry + text lint**: `qa_check.py` from
  `../pptx-ai-slide-forge/scripts/` (bounds, overlaps, slide count, key
  strings).
- **Visual inspection**: every slide, full size — wraps, clipping, contrast,
  alignment, style consistency.
- **Style fingerprint** (optional): dominant colors, fonts, accent usage —
  the basis for a restyle estimate.

### 2. Audit report (facts, severity-ranked)

| Severity | Examples |
|---|---|
| blocker | unreadable contrast, clipped text, overlaps |
| should-fix | inconsistent fonts/sizes, misaligned blocks, weak hierarchy |
| should-consider | restyle opportunity, section dividers, roadmap patterns |

No recommendations yet — facts only. This report goes to the user as-is.

### 3. Improvement plan (gate: user approval)

Batched, each item with options and a recommendation:

- **Patch in place** — python-pptx edits that preserve the deck's identity:
  fix overlaps/wraps, align to a grid, unify fonts/sizes, fix contrast,
  add consistent footers. Best when the deck's design is fundamentally fine.
- **Restyle** — map the deck onto one of the five style specs: rebuild
  backgrounds via the liquid engine, re-skin cards/tables/footers, keep the
  content 1:1. Best when the user wants a new look.
- **Rebuild** — for decks originally built by pptx-ai-slide-forge: regenerate
  from the config with fixes folded in. Fastest full-quality path when
  available.

Mixed plans are normal (e.g. patch the content slides, restyle the section
dividers).

### 4. Apply

- Patch in place: python-pptx edits; never edit text content beyond what the
  user approved.
- Restyle/rebuild: follow `pptx-ai-slide-forge` SKILL.md steps 3–6 with the
  deck's content as the outline source.

### 5. Re-render + verify + report

Same QA machinery as the audit. Report: what changed, what was verified, what
remains (honest limitations — e.g. Keynote vs PowerPoint metric differences).

## Hard gates

- The user approves the improvement plan before any edit.
- Content is never invented, deleted, or reworded without an explicit decision.
- Re-verify after every change; report the verification, not intentions.
- Restyles keep the content 1:1 — a restyle is not a rewrite.

## References

- [`references/audit-guide.md`](references/audit-guide.md) — the audit
  checklist, severity rubric, common fixes mapping, restyle recipe.
- `../pptx-ai-slide-forge/references/styles.md` — the five style specs for
  restyles.
- `../pptx-ai-slide-forge/scripts/` — qa_check.py, render_qa.sh, the builder.

## Output Format

1. Audit report (facts, severity-ranked)
2. Improvement plan (batched, recommendations)
3. The improved .pptx + before/after renders + verification report

## Example

Input: a 12-slide corporate deck with overlapping labels, three font families,
and a wall-of-text slide. Plan: patch in place (grid, fonts, split the wall of
text into two slides with the user's approval), restyle the section dividers.
Result: re-rendered, all checks green, before/after renders attached.
