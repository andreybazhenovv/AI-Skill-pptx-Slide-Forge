# Slide patterns

Layout recipes with production coordinates. Canvas: **13.333 × 7.5 in** (16:9,
1920×1080 px @ 144 dpi; **1 px at 1920 = 0.5 pt**). All numbers below ran in
production and passed render QA.

## Grid

| Zone | Y (in) | Notes |
|---|---|---|
| Section-label chip | 0.40, h 0.30 | glass pill + 0.09 in accent dot |
| Action title | 0.78, h 0.92 | 26 pt, `spc` ≈ −90, width 12.233 in, ≤ 2 lines |
| Content | 1.75 – 6.90 | cards, tables, flows |
| Footer divider | 7.02 | 1 px line, divider color |
| Footer text | 7.08 | 9.5 pt micro, left label + right `NN / 08` |
| Margins | 0.55 in left/right | content width 12.233 in |

## Typography (production scale, pt)

| Element | Size | Tracking (`spc`) | Color role |
|---|---|---|---|
| Cover headline | 46 | `int(-0.04*46*100) = -184` | white |
| Cover subtitle | 30 | −90 | secondary |
| Slide action title | 26 | −90 | white |
| Card header | 17 | −40 | white |
| Body | 14 / 13 / 12.5 | — | body |
| Secondary in cards | 11.5 / 12.5 | — | secondary |
| Micro labels (caps) | 10 / 9.5 | +150 | muted/secondary |

Rules: **no bold for hierarchy** (size + color only), one font family
("Helvetica Neue" — native on macOS, good Cyrillic), body ≥ 12.5 pt, micro ≥ 9.5 pt,
line spacing 1.0 on headlines / 1.15–1.25 on body. Letter-spacing via XML:

```python
run._r.get_or_add_rPr().set("spc", str(int(-0.04 * size_pt * 100)))  # headlines
run._r.get_or_add_rPr().set("spc", "150")   # micro caps labels: +150 (1/100 pt)
```

## XML recipes (python-pptx has no API for these)

```python
def set_fill_alpha(shp, pct):        # pct = visible opacity, e.g. 62
    sf = shp._element.spPr.find(qn("a:solidFill"))
    clr = sf.find(qn("a:srgbClr"))
    clr.append(clr.makeelement(qn("a:alpha"), {"val": str(int(pct * 1000))}))

def set_line_alpha(shp, pct):        # same, on the a:ln solidFill
    ...

# always: shp.shadow.inherit = False  (kills inherited theme shadows)
# text frames: word_wrap True, auto_size NONE, margins 0, explicit size+color+font
```

**Table cell borders** — DrawingML requires `a:lnL, a:lnR, a:lnT, a:lnB` FIRST inside
`tcPr`, before any fill. Insert each at index 0 in reverse order, and set borders
*before* `cell.fill.solid()`. Also `table.first_row = False; table.horz_banding = False`.

## Glass and accent surfaces

- **Glass card**: fill `#20365B` @ 62% opacity, border `#8AB4FF` @ 40%, 1 pt, radius
  0.125 in (18 px). Background shows through — that is the point.
- **Accent card** (highlight): glow backdrop first (rounded rect +0.055 in on each
  side, `#287BFF` @ 20%), then solid `#2438F5`, border `#C6D6FF` 1.25 pt. White text.
- **Pills**: rounded rect, adjustment 0.5 (full capsule); fill `#20365B` @ 55% or
  outlined (`fill.background()`, light border).
- **Chips (section labels)**: glass pill + accent dot + 10 pt caps, tracking +150.
- Radius discipline: cards 18 px everywhere; nested shapes get smaller radii.

## Patterns (coordinates from production)

1. **Hero cover** — bg image full-bleed; glass chip top-left; micro date top-right
   (right-aligned); headline 2×46 pt lines at y 2.95/3.66 (boxes 0.68 in tall, no
   overlap); subtitle 30 pt gray at y 4.46; accent bar (0.04 × 0.78 in) + thesis 16 pt;
   outlined CTA capsule bottom-right (10.05, 6.55, 2.73 × 0.42); page number only.
2. **Action title** — the title states the takeaway ("A correctly implemented guess
   is still a guess"), never a topic label ("Problem").
3. **Case card + numbered rows** — glass card 5.70 × 3.55; micro header; rows:
   number 20 pt accent + text 14 pt, row pitch 0.85.
4. **Pill stack** — 4 question pills 5.70 × 0.50, pitch 0.63, 13 pt.
5. **Accent strip** — full-width accent card h 0.75, 13 pt white + ice continuation.
6. **Three-level cards** — 3 × (3.91 × 4.15 in, gap 0.25): tag 10 pt accent caps →
   header 17 pt → example 12.5 pt secondary → divider → `CONTROL` micro → control
   12.5 pt light-data.
7. **Vertical chain** — 1 px accent line at x+0.165, dots per row, rows at pitch
   0.78: name 14 pt + role 11.5 pt.
8. **Evidence table** — python-pptx table 5×3, header h 0.42 / rows 0.72; header
   caps 10 pt on `#0F1C3E`, rows 11.5 pt on `#142A4D`, borders 0.75 pt; key row
   highlighted with a 0.05 in accent bar on the left edge; honest statuses (`NOT RUN`
   in muted) + micro disclaimer under the table.
9. **Finding card** — rows `CLAIM / EVIDENCE REQUIRED / EVIDENCE FOUND` (label 10 pt
   accent caps + text 11.5 pt) + verdict as a small accent card (`GAP`).
10. **Roadmap timeline** — 6 columns of width `(12.233 − 5×0.12)/6`; caps labels
    10 pt on top (active one white), cards 1.50 in tall; active column: accent fill +
    light border + glow backdrop (fill alpha 18–20%); inactive: glass.
11. **Mode cards 2×2** — 3.49 × 1.15, tag 11 pt accent caps + text 10.5 pt.
12. **Conclusions accent card** — bottom-right, accent fill, thesis 13 pt + micro
    next-steps line. This is the **last slide** — conclusions stay up for Q&A.

## Content discipline (checked at QA)

- Action titles (complete sentences stating the takeaway); ghost deck test: titles
  alone must tell the argument.
- ≤ ~40 words of body text per slide; exhibits/tables don't count, walls of text do.
- One exhibit per slide; the key finding annotated directly on it.
- Never invent facts, statuses, dates, authors. `NOT RUN` is a valid status.
- No "Thank you" slide; no decorative icons; no clip-art; single accent family.
- Geometry lint must pass: everything in bounds, no text overlaps > 0.05 sq in.
