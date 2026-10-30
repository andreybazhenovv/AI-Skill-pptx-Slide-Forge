---
name: deck-intake
description: >
  Dialogue with the user about the design, theme, composition and size of a
  presentation: read the user's material, ask batched questions with
  recommendations, and produce a design brief (style JSON + slide outline +
  build plan) ready for pptx-ai-slide-forge to build. Use when the user
  provides material and wants a presentation designed - before any building.
  Do not use for building itself (pptx-ai-slide-forge builds) or for improving
  existing decks (deck-polish).
license: MIT
metadata:
  author: pptx-AI-Slide-Forge contributors
  version: "1.0.0"
---

# deck-intake

## Overview

The intake half of the deck pipeline: turn the user's material and preferences
into a **design brief** — a style JSON + slide outline + build plan — that the
companion skill `pptx-ai-slide-forge` executes. The value here is the dialogue:
batched questions with recommendations (never one at a time), honest trade-offs,
and a ghost-deck-tested outline before anything is built.

## When to Use

- The user provides material (notes, a doc, a data file) and wants a presentation
- The user asks "how many slides / which style / what composition should I use"
- The user wants a second opinion on a deck plan before building

## Workflow

### 1. Read the material fully

Skimming is not allowed: the outline quality depends on facts only the source
contains. Note the language, the key argument, candidate exhibits (tables,
numbers, diagrams).

### 2. The batched intake round (gate: user answers)

Ask **one message, 3–6 questions**, each with options and your recommendation:

1. **Purpose & audience** — inform / pitch / teach; who watches, what they decide
2. **Size** — slide count range with a recommendation from the material's density
3. **Style** — the five built-in specs (`references/styles.md`) or a custom one
   (author it with the AI recipe in the same file); dark vs light guidance
4. **Composition** — per slide role (hero cover, contents grid, section dividers,
   KPI/exhibit slides, roadmap, conclusions); what the material supports
5. **Language & attribution** — deck language, title, author block, footers

Record accepted answers as binding decisions. The user may approve a batch with
a single "ок на все рекомендации" — that is approval, do not re-ask.

### 3. Style selection or authoring

- Built-in: pick from the five specs, show the user a one-line mood summary each
- Custom: draft the style JSON per the authoring recipe in
  [`references/styles.md`](../../pptx-ai-slide-forge/references/styles.md) and
  validate it on one test slide before committing to it

### 4. Produce the design brief

```json
{
  "style": {"style_id": "novapay-liquid-electric-blue", "custom": false},
  "deck": {"title": "", "language": "ru", "slides": 8, "aspect": "16:9",
           "author_block": null, "footer": true},
  "outline": [
    {"n": 1, "title": "action title", "content": "what goes on the slide",
     "visual": "background / composition / exhibit"}
  ],
  "qa": {"contains": ["key strings"], "forbid": ["Thank you"]}
}
```

Run the ghost deck test on the outline (titles alone must tell the argument).
Fix the outline until it passes — then, and only then, hand off.

### 5. Handoff (gate: user approves the brief)

Pass the brief to `pptx-ai-slide-forge` (its SKILL.md steps 3–6 consume it:
backgrounds → build → render QA → text QA). Stay in the loop: review the
renders and report to the user.

## Hard gates

- Never build before the outline is user-approved.
- Questions in batches with recommendations; never one at a time.
- Never invent facts for the outline — the material is the only source.
- Language: the deck language follows the material unless the user says otherwise.

## References

- [`references/intake-catalog.md`](references/intake-catalog.md) — the full
  question catalog, style selector guide, outline patterns, brief schema

## Output Format

The design brief (JSON) + the outline table + the build command line. No deck.

## Example

Input: a RU conспект (data.md) + "сделай презентацию в стиле NovaPay".
Brief: 8 slides, NovaPay Liquid Electric Blue, outline with action titles,
qa plan ("NOT RUN:4", forbid "Спасибо"). Handoff to pptx-ai-slide-forge →
8-slide deck rendered and verified.
