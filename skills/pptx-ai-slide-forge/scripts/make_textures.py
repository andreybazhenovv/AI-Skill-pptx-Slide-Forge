"""pptx-ai-slide-forge :: procedural slide background engine.

Generates full-bleed 1920x1080 backgrounds from a Python config module.
Two engines, both battle-tested on a real 8-slide deck:

  liquid  - layered glossy glass ribbons with icy speculars (NovaPay
            Liquid Electric Blue); ribbon fields anchored to corners/edges
            with dark text zones preserved
  ribbed  - vertical ribbed metallic surface with diagonal wave, glow and
            vignette (Midnight Electric Blue cover texture)

Usage:
    python3 make_textures.py --config my_slides.py --out assets

Config module contract (see examples/sdd-deck/textures_config.py):

    SLIDES = {
        1: {"engine": "liquid", "glows": [...], "ribbons": [...],
            "darken": [...], "checks": {...}},
        2: {"engine": "ribbed", "rib_period": 14, ...},
    }
    OUT = "assets"       # optional, overridden by --out
    STRICT = True        # optional: fail if text-zone luminance caps exceeded

Every render prints a luminance report for its declared check zones.
READ the generated PNGs before building the deck - the numbers do not show
whether the art looks premium, only that text zones are dark.
"""
import argparse
import importlib.util
import os

import numpy as np
from PIL import Image, ImageFilter

W, H = 1920, 1080
SS = 2                      # supersample factor
PX_IN = 144 * SS            # pixels per inch at supersample (13.333 in canvas)

rng = np.random.default_rng(7)


def hx(s):
    s = s.lstrip("#")
    return np.array([int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)], dtype=np.float64)


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def gradient_stops(t, stops):
    pos = np.array([p for p, _ in stops])
    cols = np.stack([hx(c) for _, c in stops])
    return np.stack([np.interp(t, pos, cols[:, i]) for i in range(3)], axis=-1)


def radial_glow(shape, cx_in, cy_in, r_in, color, alpha, power=2.2):
    Hs, Ws = shape
    ys, xs = np.mgrid[0:Hs, 0:Ws].astype(np.float64)
    d = np.hypot(xs - cx_in * PX_IN, ys - cy_in * PX_IN) / (r_in * PX_IN)
    return (np.clip(1 - d, 0, 1) ** power * alpha)[..., None] * hx(color)[None, None, :]


def glow(img, cx_in, cy_in, r_in, color, alpha, power=2.2):
    img += radial_glow(img.shape[:2], cx_in, cy_in, r_in, color, alpha, power)


def gate_mask(xs, ys, gates):
    """gates: list of ('x'|'y', lo, hi, feather) in inches -> multiplicative mask.

    lo/hi None = unbounded on that side. Feather is the soft transition width.
    Ribbons are anchored to corners/edges by gating, never by hard clipping.
    """
    m = np.ones(xs.shape, dtype=np.float64)
    x_in, y_in = xs / PX_IN, ys / PX_IN
    for axis, lo, hi, feather in gates:
        v = x_in if axis == "x" else y_in
        if lo is not None:
            m = m * smoothstep((v - lo) / feather)
        if hi is not None:
            m = m * smoothstep((hi - v) / feather)
    return m


# ---------------------------------------------------------------- liquid engine

def ribbon_shape(xs, ys, cfg):
    """(core, rim1, rim2) for one ribbon, multiplied by its gates.

    Centerline: y = y0 + slope*x + sum(A*sin(x/L + p)).
    Tuned on a real deck: width multiplier 1.5, core exp 1.6 (broad bodies),
    narrow rims at +-0.68/+-0.58 of half-width (icy speculars, not neon lines).
    """
    x_in = xs / PX_IN
    y_in = ys / PX_IN
    c = cfg.get("y0", 0.0) + cfg.get("slope", 0.0) * x_in
    for A, L, p in cfg.get("waves", []):
        c = c + A * np.sin(x_in / L + p)
    wpx = cfg.get("w0", 1.0) * (0.78 + 0.45 * np.sin(x_in / cfg.get("Lw", 4.2) + cfg.get("pw", 0.9))) * 1.5
    u = (y_in - c) / np.maximum(wpx, 0.02)
    core = np.exp(-u * u * 1.6)
    rim1 = np.exp(-((u - 0.68) / 0.085) ** 2)
    rim2 = np.exp(-((u + 0.58) / 0.08) ** 2)
    g = gate_mask(xs, ys, cfg.get("gates", []))
    return core * g, rim1 * g, rim2 * g


def add_ribbon(img, xs, ys, cfg):
    core, rim1, rim2 = ribbon_shape(xs, ys, cfg)
    x_in = xs / PX_IN
    s = np.clip(x_in / 13.333, 0, 1) ** cfg.get("skew", 1.0)
    c1, c2 = hx(cfg["c1"]), hx(cfg["c2"])
    col = c1[None, None, :] * (1 - s[..., None]) + c2[None, None, :] * s[..., None]
    layer = col * (0.62 + 0.38 * core)[..., None]   # saturated blue bodies
    a = np.clip(core * cfg.get("alpha", 0.85), 0, 0.93)
    depth = cfg.get("depth")
    if depth == "back":                              # far layer: blurred, dimmer
        blurred = Image.fromarray(np.clip(layer, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(cfg.get("blur", 40) * SS * 0.5))
        layer = np.asarray(blurred, dtype=np.float64)
        a = np.clip(a * 0.85, 0, 0.8)
    elif depth == "mid":
        blurred = Image.fromarray(np.clip(layer, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(6 * SS))
        layer = np.asarray(blurred, dtype=np.float64)
    img *= (1 - a[..., None])
    img += layer * a[..., None]
    rim = hx(cfg.get("rim", "A9D2FF"))[None, None, :]
    img += (rim1 * cfg.get("rim1a", 0.40) + rim2 * cfg.get("rim2a", 0.26))[..., None] * rim * 1.25
    return img


def darken(img, xs, ys, zone):
    """zone = (x0, y0, x1, y1, strength, feather), inches. Smooth darkening box
    for text zones - keeps the layered background visible but subdued."""
    x0, y0, x1, y1, strength, feather = zone
    x_in, y_in = xs / PX_IN, ys / PX_IN
    fx = smoothstep((x_in - (x0 - feather)) / feather) * smoothstep(((x1 + feather) - x_in) / feather)
    fy = smoothstep((y_in - (y0 - feather)) / feather) * smoothstep(((y1 + feather) - y_in) / feather)
    img *= (1 - strength * fx * fy)[..., None]
    return img


def vignette(img, xs, ys, strength=0.35):
    Hs, Ws = img.shape[:2]
    d = np.minimum(np.minimum(xs, ys), np.minimum(Ws - xs, Hs - ys)) / (0.16 * Ws)
    img *= (0.42 + 0.58 * np.clip(d, 0, 1) ** 1.1)[..., None] ** (2 - strength)
    return img


def render_liquid(cfg, out_path):
    Hs, Ws = H * SS, W * SS
    ys, xs = np.mgrid[0:Hs, 0:Ws].astype(np.float64)
    t = np.clip((xs / Ws) * 0.42 + (ys / Hs) * 0.58, 0, 1)
    img = gradient_stops(t, cfg.get("base", [(0.0, "03091B"), (0.40, "061232"),
                                             (0.72, "08266E"), (1.0, "0B3EC0")]))
    img *= 0.98
    for g in cfg.get("glows", []):
        glow(img, *g)
    for rcfg in cfg.get("ribbons", []):
        img = add_ribbon(img, xs, ys, rcfg)
    for zone in cfg.get("darken", []):
        img = darken(img, xs, ys, zone)
    if cfg.get("vignette", 0.35) > 0:
        vignette(img, xs, ys, cfg.get("vignette", 0.35))
    img += rng.normal(0, 255 * 0.008, img.shape)
    return _finish(img, out_path)


# ---------------------------------------------------------------- ribbed engine

def render_ribbed(cfg, out_path):
    """Vertical ribbed metallic surface with diagonal wave (cover texture).

    Rib crests carry ice-blue speculars; the bottom-left quadrant is darkened
    with a smooth ramp so the headline zone stays quiet."""
    Hs, Ws = H * SS, W * SS
    ys, xs = np.mgrid[0:Hs, 0:Ws].astype(np.float64)

    period = cfg.get("rib_period", 14) * SS
    rib = 0.5 + 0.5 * np.cos(2 * np.pi * xs / period)
    wave = (cfg.get("wave_amp", 170) * SS) * np.sin(
        ys / (cfg.get("wave_y", 260) * SS) + xs / (cfg.get("wave_x", 850) * SS))
    t = np.clip(((xs + wave) * 0.35 + ys * 0.65) / (0.35 * Ws + 0.65 * Hs), 0, 1)
    img = gradient_stops(t, cfg.get("stops", [(0.00, "061224"), (0.42, "0654C9"),
                                              (0.72, "073A91"), (1.00, "A8D8FF")]))
    img *= (0.30 + 0.70 * rib)[..., None]
    spec = rib ** 12
    img += (spec * 0.60)[..., None] * (hx("A8D8FF")[None, None, :] - img)

    g = cfg.get("glow", [0.72, 0.38, 0.55, "127BFF", 0.35])
    glow(img, *g)

    d_edge = np.minimum(np.minimum(xs, ys), np.minimum(Ws - xs, Hs - ys))
    vig = 0.30 + 0.70 * np.clip(d_edge / (0.20 * Ws), 0, 1) ** 1.2
    img *= vig[..., None]

    bl = (1 - xs / Ws) * (ys / Hs)
    wbl = np.clip((bl - cfg.get("text_ramp_lo", 0.18)) / (1 - cfg.get("text_ramp_lo", 0.18)), 0, 1) \
        ** cfg.get("text_ramp_exp", 1.7)
    img *= (1 - cfg.get("text_dark", 0.55) * wbl)[..., None]

    img += rng.normal(0, 255 * cfg.get("noise", 0.015), img.shape)
    return _finish(img, out_path)


# ---------------------------------------------------------------- plumbing

def _finish(arr, out_path):
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGB").resize((W, H), Image.LANCZOS)
    img.save(out_path, optimize=True)
    return img


def _report(img, checks):
    a = np.asarray(img, dtype=np.float64)
    out = {}
    for name, (x0, y0, x1, y1) in (checks or {}).items():
        crop = a[int(y0 * 144):int(y1 * 144), int(x0 * 144):int(x1 * 144)]
        out[name] = round(float(crop.mean()), 1)
    return out


def render(num, cfg, out_dir):
    cfg = dict(cfg)
    engine = cfg.pop("engine", "liquid")
    path = os.path.join(out_dir, f"bg_{num:02d}.png")
    if engine == "liquid":
        img = render_liquid(cfg, path)
    elif engine == "ribbed":
        img = render_ribbed(cfg, path)
    else:
        raise ValueError(f"unknown engine {engine!r} for slide {num}")
    print(f"bg_{num:02d} ({engine}): {_report(img, cfg.get('checks'))}")
    return path


def load_config(path):
    spec = importlib.util.spec_from_file_location("sf_textures_config", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True, help="Python config module with SLIDES dict")
    ap.add_argument("--out", default=None, help="output dir (default: config OUT or 'assets')")
    args = ap.parse_args()

    mod = load_config(args.config)
    out_dir = args.out or getattr(mod, "OUT", "assets")
    os.makedirs(out_dir, exist_ok=True)
    strict = getattr(mod, "STRICT", False)
    max_lum = getattr(mod, "MAX_TEXT_ZONE_LUM", 30.0)

    for num in sorted(mod.SLIDES):
        cfg = mod.SLIDES[num]
        path = render(num, cfg, out_dir)
        if strict:
            for name, lum in _report(Image.open(path), cfg.get("checks")).items():
                assert lum < max_lum, f"bg_{num:02d} [{name}] luminance {lum} >= {max_lum}"
    print("textures OK")


if __name__ == "__main__":
    main()
