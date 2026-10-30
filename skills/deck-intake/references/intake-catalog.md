# Intake catalog

The question catalog, style selector, outline patterns and the brief schema
for the deck-intake dialogue. Everything here feeds the design brief that
`pptx-ai-slide-forge` executes.

## 1. The batched intake round

One message, 3–6 questions, each with options and a recommendation. The user
approves a batch with one reply ("ок на все рекомендации") — record decisions,
do not re-ask.

### Q1. Purpose & audience

| Option | Recommendation when |
|---|---|
| Inform (status, overview) | internal material, factual density |
| Pitch (sell, convince) | product/business content, decision-makers |
| Teach (workshop, course) | process/method content, step-heavy |
| Report (results, metrics) | KPI-heavy material, executive audience |

Ask: who watches, what do they decide after the talk?

### Q2. Size

| Material density | Recommendation |
|---|---|
| < 2 pages of notes | 5–8 slides |
| 3–10 pages / a structured plan | 8–14 slides |
| a full talk / course segment | 14–24 slides (consider splitting the deck) |

State the trade-off: more slides = lighter per slide; fewer = denser.

### Q3. Style

Present the five built-ins as one-liners, then recommend:

| Style | Mood | Use when |
|---|---|---|
| Midnight Electric Blue | premium tech, dark editorial | tech/product talks |
| NovaPay — Liquid Electric Blue | premium fintech, liquid glass | fintech, SaaS |
| Clean Blue Tech | light corporate, editorial | enterprise, light rooms |
| Dark Emerald Strategy | executive roadmap, emerald | strategy, exec reviews |
| Obsidian Ember | industrial editorial, ember | industrial, hardware, bold |

Custom: offer the AI-authoring recipe (`styles.md` → "Authoring a new style
JSON with AI") — draft the JSON, validate on one test slide.

### Q4. Composition

Per slide role, from the material:

| Role | Pattern | When the material supports it |
|---|---|---|
| Hero cover | full art + title + thesis | always (slide 1) |
| Contents grid | numbered cards | decks > 6 slides |
| Section dividers | oversized number + statement | decks > 10 slides |
| KPI / exhibit | metric cards, evidence matrix | numbers, statuses, comparisons |
| Process / roadmap | flow, quarterly timeline | steps, plans |
| Conclusions | accent statement slide | always (last, no "thank you") |

### Q5. Language & attribution

Deck language (follows the material unless told otherwise), title, author
block (or none), footers (page numbers on/off), forbidden strings (e.g.
"Thank you").

## 2. Outline discipline

- **Action titles**: complete sentences stating the takeaway — never topic
  labels.
- **Ghost deck test**: titles alone must tell the argument. Run it on every
  outline draft; fix before presenting.
- **≤ ~40 words** of body text per slide; exhibits excluded.
- **One exhibit per slide**; annotate the key finding on it.
- **Honest statuses**: `NOT RUN`, `GAP` are valid; never decorate them.
- **Conclusions last**; no "Thank you" slide.

## 3. The brief schema

```json
{
  "style": {"style_id": "<built-in id>", "name": "", "custom": false,
            "custom_spec": null},
  "deck": {"title": "", "language": "ru", "slides": 8, "aspect": "16:9",
           "author_block": null, "footer": true,
           "forbid": ["Thank you"], "key_strings": ["NOT RUN"]},
  "outline": [
    {"n": 1, "title": "", "content": "", "visual": ""}
  ],
  "handoff": {"skill": "pptx-ai-slide-forge", "steps": "SKILL.md 3-6"}
}
```

`custom_spec` carries the full style JSON when the style is authored, not
picked. `key_strings` feed qa_check's `--contains`.

## 4. Handoff

The forge consumes: backgrounds (per-slide configs from the outline's
`visual` column), the builder (slide sections from `content`), QA (from
`key_strings`/`forbid`). Stay in the loop: review renders, report to the
user, keep the intake decisions as the source of truth.
