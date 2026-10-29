# Background engine

`scripts/make_textures.py` renders full-bleed 1920x1080 backgrounds from per-slide
configs. Canvas: 13.333 x 7.5 in = **144 px/inch** (288 at supersample `SS=2`; all
renders are computed at 3840x2160 and downscaled with LANCZOS).

Everything here was tuned on a real deck. Copy the values, then iterate visually.

## The one rule that matters

**Texture lives in corners and edges; text zones stay dark.** Declare `checks`
(zones in inches) for every slide — the script prints mean luminance per zone.
Targets, tuned on production:

| Zone | Target |
|---|---|
| Title strip (y 0.3–1.8) | ≤ ~12/255 |
| Body/cards zone | ≤ ~22/255 |
| Texture corners | 15–30/255 mean is plenty; peaks may be brighter |

Numbers prove darkness. Only your eyes prove style — always open the PNGs.

## Liquid engine (`"engine": "liquid"`)

Layered glossy glass ribbons over a dark diagonal base, plus atmospheric glows,
darkening zones, vignette and fine noise.

### Slide config fields

| Field | Meaning |
|---|---|
| `base` | gradient stops `[(pos, "HEX"), ...]` along a diagonal axis `t = 0.42x + 0.58y` |
| `glows` | list of `[cx, cy, r, "HEX", alpha]` (inches; inches; inches of radius) |
| `ribbons` | list of ribbon dicts (below) |
| `darken` | list of `(x0, y0, x1, y1, strength, feather)` smooth boxes over text zones |
| `vignette` | 0–1 edge darkening strength |
| `checks` | `{"name": (x0, y0, x1, y1), ...}` printed as luminance report |

### Ribbon fields

| Field | Meaning |
|---|---|
| `y0`, `slope` | centerline start and tilt: `y = y0 + slope * x` |
| `waves` | `[(amp, length, phase), ...]` sine terms added to the centerline |
| `w0` | base half-width in inches (**× 1.5 applied inside the engine**; production hero used `w0: 0.78` → ~1.2 in rendered) |
| `Lw`, `pw` | thickness modulation (sin along the length) |
| `c1` → `c2` | color progression along the x axis (deep → bright) |
| `alpha` | core opacity cap (0.85 default; clip 0.93) |
| `depth` | `"back"` (heavy pre-blur ≈ 55, dimmer) / `"mid"` (blur 6) / front (sharp) |
| `rim`, `rim1a`, `rim2a` | icy specular color and its intensities (narrow rims at ±0.68/±0.58 of half-width) |
| `gates` | `[("x"|"y", lo, hi, feather), ...]` — smooth anchor masks; this is how ribbons attach to corners/edges |
| `skew` | exponent on the color-progress axis |

### Tuned production values (do not regress)

- Ribbon bodies: `core = exp(-u² * 1.6)` (broad), body brightness floor `0.62 + 0.38*core`
  — saturated blue bodies, not gray.
- Rims: `exp(-((u∓0.68)/0.085)²)` — **narrow** icy speculars. Wide rims = "neon
  lines" = rejected failure mode.
- Width multiplier ×1.5 is inside the engine; an early iteration without it looked
  like thin laser streaks (see the style's `negative_prompt`).
- Glows multiplied ×1.35; base gradient ×0.98 with stops
  `#03091B → #061232 → #08266E → #0B3EC0`.
- Hero front ribbon: two sine waves for an S-curve, plus a separate thin (`w0≈0.16`)
  near-white streak ribbon offset by phase — the "almost white blue highlight".

### Composition recipes (from production)

- **Hero**: 3–4 crossing ribbons bottom-left → upper-right, deep blurred layers
  behind, one thin bright streak; `darken` the headline zone (strength ~0.5) and
  top-left.
- **Content slides**: 2–4 ribbons gated to the **top-right corner**, **bottom-left
  corner** and **bottom-right corner**; a standard darken box over the title strip —
  `BASE_DARKEN_TITLE = (0.30, 0.25, 12.60, 1.80, 0.42, 0.8)` — plus mild body-zone
  darkening (0.22–0.30). Vary ribbon angles per slide; keep material/color/light
  identical.
- Bright elements only where no body text sits. Slides with bottom text lines keep
  the bottom strip gated (`("y", 6.6, None, 0.8)` on bottom ribbons).

## Ribbed engine (`"engine": "ribbed"`)

Vertical ribbed metallic surface — cover texture for Midnight Electric Blue.

| Field | Default | Meaning |
|---|---|---|
| `rib_period` | 14 px | rib period |
| `wave_amp` / `wave_y` / `wave_x` | 170 / 260 / 850 | diagonal wave: `170·sin(y/260 + x/850)` (px at 1920) |
| `stops` | `#061224 → #0654C9 → #073A91 → #A8D8FF` | diagonal gradient blended by the warped axis |
| `glow` | `[0.72, 0.38, 0.55, "127BFF", 0.35]` | large soft glow |
| `text_dark` / `text_ramp_lo` / `text_ramp_exp` | 0.55 / 0.18 / 1.7 | smooth ramp darkening the bottom-left headline quadrant |
| `noise` | 0.015 | monochrome grain (σ fraction of 255) |

Rib shading: troughs `×0.30`, crests `×1.0`, plus `rib**12` ice speculars. Vignette
to near-black toward all edges (floor 0.30 at 20% of width).

## Sanity and iteration workflow

1. Write configs; run `make_textures.py --config ... --out ...`; read the printed
   luminance report (add `STRICT = True` to fail builds over caps).
2. **Open every PNG.** Look for: thin neon lines (widen `w0` / raise body floor),
   mud (too many overlapping back layers — reduce alphas), flat background (add a
   corner glow or one more back ribbon), texture behind text (extend `darken`).
3. Regenerate; re-look. Only then build the deck.
