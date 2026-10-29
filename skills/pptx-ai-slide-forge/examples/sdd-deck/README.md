# Worked example: 8-slide SDD deck (NovaPay Liquid Electric Blue)

This is the deck this skill was extracted from: a Russian-language technical talk
«От промпта к инженерному процессу: Spec-Driven Development с AI-агентами» — 8 slides,
built, rendered, visually inspected, fixed, and shipped.

## Files

| File | What it is |
|---|---|
| `textures_config.py` | the exact production background configs (all 8 slides, liquid engine); `SLIDES` dict + `BASE_DARKEN_TITLE` |
| `content_outline.md` | the approved slide outline (action titles, content, visual form per slide) |
| `../../scripts/build_deck.py` | the reference builder that produced the deck (theme tokens + 8 slide sections + `verify()`) |

## Reproduce

All paths are relative to this directory (`examples/sdd-deck/`). Backgrounds go to
the skill-root `assets/`; the built deck lands next to the scripts
(`scripts/spec-driven-development-ai-agents.pptx`).

```bash
# 1. backgrounds → skill-root assets/ (prints a luminance report per text zone)
python3 ../../scripts/make_textures.py --config textures_config.py --out ../../assets

# 2. deck → scripts/spec-driven-development-ai-agents.pptx
#    (adapt the slide sections in build_deck.py for your own content)
python3 ../../scripts/build_deck.py

# 3. render + inspect + text QA
bash ../../scripts/render_qa.sh "$PWD/../../scripts/spec-driven-development-ai-agents.pptx" qa
python3 ../../scripts/qa_check.py ../../scripts/spec-driven-development-ai-agents.pptx \
    --slides 8 --contains "NOT RUN:4" --contains "GAP" --forbid "Спасибо"
```

## QA results from the real run

- geometry lint: clean (bounds + overlaps) after one 0.05 sq-in headline fix;
- text QA: 6/6 (slide count, cover title, `NOT RUN` ×4, no thank-you slide, `GAP`,
  final thesis);
- render QA: all 8 slides inspected; two fix rounds (label-capsule widths for
  tracking+caps, `REFACTOR` pill wrap) — then clean;
- luminance (fresh run): title strips 5.1–11.7/255, content zones 15.3–24.3/255;
  the hero headline zone runs brighter (~30/255) by design — white text keeps
  ~10:1 contrast there.

Use this outline as the pattern: one argument across eight action titles, one visual
idea per slide, honest statuses, conclusions last.
