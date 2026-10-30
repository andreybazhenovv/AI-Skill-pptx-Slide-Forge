# Audit guide

The audit checklist, severity rubric, common fixes and the restyle recipe for
deck-polish. Audit facts first, recommendations second — never merged.

## 1. The audit pipeline

```bash
# render every slide (Keynote; files named <outdir-basename>.NNN.png)
../pptx-ai-slide-forge/scripts/render_qa.sh /abs/path/deck.pptx qa

# geometry + text lint (bounds, overlaps, slide count, key strings)
python3 ../pptx-ai-slide-forge/scripts/qa_check.py deck.pptx --slides N \
    --contains "key string" --forbid "Thank you"
```

Then **visual inspection of every slide, full size**: wraps, clipping,
contrast, alignment, hierarchy, style consistency. The lint is a filter, not
a verdict.

## 2. Checklist

### Geometry
- shapes fully in bounds (text boxes strictly; decorative bleed ≤ 1 in)
- no text overlaps (> 0.05 sq in)
- consistent margins; a visible grid

### Typography
- ≤ 2 font families; sizes from a scale (not arbitrary)
- body ≥ 12.5 pt on dark themes (light corporate styles may use 12 pt per their spec — the style spec wins); captions ≥ 9.5 pt
- hierarchy by size/weight, not by random emphasis
- typographic dashes/quotes (— «» “”), no hyphens as dashes

### Contrast & color
- text/background contrast ≥ ~7:1 for body, ~4.5:1 minimum
- one accent family; accent share 5–15%
- consistent accent semantics (one color = one meaning)

### Content integrity
- no invented/deleted content (polish never rewrites without a decision)
- statuses honest (NOT RUN / GAP are valid)
- no "Thank you" slide; conclusions last

### Style consistency
- consistent card/table/divider treatments
- backgrounds: texture in corners/edges, text zones quiet
- footers/labels consistent across slides

## 3. Severity rubric

| Severity | Bar |
|---|---|
| blocker | unreadable contrast; clipped/overlapping text; wrong facts |
| should-fix | hierarchy failures; inconsistency; misalignment |
| should-consider | restyle opportunities; missing patterns (roadmap, dividers) |

## 4. Common fixes

| Symptom | Fix |
|---|---|
| labels wrap to two lines | widen ≥ 15% or shorten; caps+tracking need buffers |
| overlapping labels | move to grid; shrink to content |
| dark text on dark fill | invert or lighten the fill; re-check contrast |
| wall of text | split into two slides (with the user) or convert to exhibit |
| three font families | unify to the deck's primary family |
| flat empty background | liquid engine light/dark washes; texture to corners |

## 5. Restyle recipe (map onto a built-in style)

1. Extract content 1:1: every slide's text/tables/numbers (never rewrite).
2. Pick the style; read its spec (`../pptx-ai-slide-forge/references/styles.md`).
3. Map each slide to a pattern (cover / cards / exhibit / roadmap / conclusions).
4. Rebuild via `pptx-ai-slide-forge` SKILL.md steps 3–6 with the outline as
   the source; keep `--contains` strings from the original deck.
5. Before/after renders to the user; the content diff must be empty.

## 6. Patch recipes (python-pptx, in place)

- **Grid**: snap left edges to a common x; snap widths to a common column.
- **Fonts**: walk `slide.shapes`, set `run.font.name/size` per the deck scale.
- **Contrast**: darken fills under light text / lighten under dark text;
  re-render and re-check.
- **Footers**: add consistent page labels (`NN / total`) + a thin divider.
- **Overlaps**: nudge to the nearest free lane; re-run the lint.

## 7. Reporting

Before/after renders + a verification report: every check re-run, every fix
evidenced, remaining issues listed honestly. "Should be fine" is not a status.
