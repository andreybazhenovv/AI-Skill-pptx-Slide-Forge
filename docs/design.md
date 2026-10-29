# Design: pptx-ai-slide-forge

Date: 2026-10-29
Status: implemented (v1.0.0)

## Goal

Package a proven end-to-end pipeline for building premium dark-tech PPTX decks into a
reusable Agent Skill: procedural backgrounds, glass/accent surfaces, content
discipline, and render-based QA. Extracted from a real engagement (8-slide SDD deck,
two full style passes) — everything shipped here ran in production first.

## Decisions

1. **Full Agent Skills layout** (`skills/pptx-ai-slide-forge/` with `scripts/`,
   `references/`, `assets/`, `examples/`) over a minimal single SKILL.md — the
   experience splits naturally into four reference domains, and a single SKILL.md
   holding all of it would be unreadable.
2. **Skill name lowercase** (`pptx-ai-slide-forge`) per the Agent Skills naming rule;
   the repository keeps the author's original name `pptx-AI-Slide-Forge`.
3. **Battle-tested code over a speculative framework.** The scripts are the ones that
   built and QA'd a real deck, lightly refactored for reuse (theme tokens at the top,
   background configs as data). No config-driven deck DSL — that would be new,
   unproven code.
4. **README in English only.** GitHub-facing audience; RU material lives in the docs
   the skill generates.
5. **Two engines, one module.** `make_textures.py` carries both background engines
   proven in the session — liquid ribbons (NovaPay) and ribbed metallic (Midnight
   Electric Blue) — selected per slide via `engine` in the config.
6. **Honest QA is part of the contract.** The skill mandates render-and-look QA
   (Keynote AppleScript on macOS; the PowerPoint save-as-PNG silence is documented as
   a known pitfall), text extraction checks, and geometry lint. Statuses reported by
   the agent must reflect what was actually verified.

## Non-goals

- No deck DSL/YAML schema (YAGNI; revisit only after several more real decks).
- No web/HTML deck output.
- No image-generation API integration; backgrounds are procedural by design
  (deterministic, no external services).
