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
from PIL import Image, ImageDraw, ImageFilter

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


# ------------------------------------------------- v1.1 composable layers

def _path_points(path, n=360):
    """Sample a path to n (x, y) points in inches.

    kinds:
      arc    - circular arc: cx, cy, r, a0, a1 (degrees)
      ring   - closed circle: cx, cy, r
      bezier - cubic swoosh: pts = [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]
    """
    kind = path.get("kind", "arc")
    if kind in ("arc", "ring"):
        cx, cy, r = path["cx"], path["cy"], path["r"]
        a0 = np.deg2rad(path.get("a0", 0.0))
        a1 = np.deg2rad(path.get("a1", 360.0 if kind == "ring" else 270.0))
        th = np.linspace(a0, a1, n)
        return cx + r * np.cos(th), cy + r * np.sin(th), kind == "ring"
    if kind == "bezier":
        p = [np.asarray(pt, dtype=np.float64) for pt in path["pts"]]
        t = np.linspace(0.0, 1.0, n)[:, None]
        xy = ((1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1]
              + 3 * (1 - t) * t ** 2 * p[2] + t ** 3 * p[3])
        return xy[:, 0], xy[:, 1], False
    raise ValueError(f"unknown path kind {kind!r}")


def _ramp(n, c1, c2, skew=1.0):
    s = np.clip(np.linspace(0.0, 1.0, n) ** skew, 0, 1)
    a, b = hx(c1), hx(c2)
    return a[None, :] * (1 - s[:, None]) + b[None, :] * s[:, None]


def add_path_ribbon(img, xs, ys, cfg):
    """A glossy ribbon along an arbitrary path (arc / ring / bezier swoosh).

    Same cross-section language as straight ribbons - broad glass body with
    narrow icy edge speculars - implemented as an anti-aliased stroke whose
    mask gradient produces the rims, so it works on any curvature."""
    Hs, Ws = img.shape[:2]
    px_in, py_in, closed = _path_points(cfg["path"], cfg.get("samples", 360))
    pts = list(zip((px_in * PX_IN).tolist(), (py_in * PX_IN).tolist()))
    if closed and pts[0] != pts[-1]:
        pts.append(pts[0])
    wpx = max(2, int(cfg.get("w0", 0.9) * PX_IN))
    soft = cfg.get("soft", 10) * SS * 0.5

    body = Image.new("RGB", (Ws, Hs), (0, 0, 0))
    db = ImageDraw.Draw(body)
    cols = _ramp(len(pts), cfg["c1"], cfg["c2"], cfg.get("skew", 1.0))
    for i in range(len(pts) - 1):
        db.line([pts[i], pts[i + 1]], fill=tuple(int(v) for v in cols[i]),
                width=wpx, joint="curve")

    mask_img = Image.new("L", (Ws, Hs), 0)
    ImageDraw.Draw(mask_img).line(pts, fill=255, width=wpx, joint="curve")
    mask = np.asarray(mask_img.filter(ImageFilter.GaussianBlur(soft * 0.7)),
                      dtype=np.float64) / 255.0
    gy, gx = np.gradient(mask)
    rim = np.clip(np.hypot(gx, gy) * cfg.get("rim_gain", 22.0), 0, 1)

    layer = np.asarray(body.filter(ImageFilter.GaussianBlur(soft)),
                       dtype=np.float64)
    a = np.clip(mask * cfg.get("alpha", 0.85), 0, 0.92)
    if cfg.get("depth") == "back":
        layer = np.asarray(Image.fromarray(
            np.clip(layer, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(cfg.get("blur", 40) * SS * 0.5)),
            dtype=np.float64)
        a = np.clip(a * 0.85, 0, 0.8)
    elif cfg.get("depth") == "mid":
        layer = np.asarray(Image.fromarray(
            np.clip(layer, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(6 * SS)), dtype=np.float64)

    if cfg.get("blend", "normal") == "screen":
        img[:] = 255 - (255 - img) * (255 - np.clip(layer, 0, 255)) / 255
    else:
        img[:] = img * (1 - a[..., None]) + layer * a[..., None]
    if cfg.get("rim_alpha", 0.55) > 0:
        img += (rim * cfg.get("rim_alpha", 0.55))[..., None] * \
            hx(cfg.get("rim", "C1E1FF"))[None, None, :]
    return img


def add_scatter(img, xs, ys, cfg):
    """Dot-grid field with radial falloff - a quiet technological layer."""
    pitch = cfg.get("pitch", 26) * SS
    dsize = max(1, int(cfg.get("dot", 3) * SS * 0.5))
    dots = ((xs % pitch) < dsize * 2) & ((ys % pitch) < dsize * 2)
    g = gate_mask(xs, ys, cfg.get("gates", []))
    if cfg.get("focus"):
        f = cfg["focus"]
        fx, fy = f[0], f[1]
        r_in = f[2] if len(f) > 2 else 6.0
        d = np.hypot(xs - fx * PX_IN, ys - fy * PX_IN) / (r_in * PX_IN)
        g = g * np.clip(1 - d, 0, 1) ** cfg.get("falloff", 1.6)
    a = dots * g * cfg.get("alpha", 0.14)
    img += a[..., None] * hx(cfg.get("color", "5B8AD4"))[None, None, :]
    return img


def add_arc_field(img, xs, ys, cfg):
    """Concentric thin arc field (HUD rings) - quiet radial instrumentation."""
    Hs, Ws = img.shape[:2]
    canvas = Image.new("L", (Ws, Hs), 0)
    d = ImageDraw.Draw(canvas)
    cx, cy = cfg["cx"] * PX_IN, cfg["cy"] * PX_IN
    r0, r1 = cfg["r0"] * PX_IN, cfg["r1"] * PX_IN
    n = cfg.get("count", 6)
    a0, a1 = cfg.get("a0", 160.0), cfg.get("a1", 320.0)
    for i in range(n):
        r = r0 + (r1 - r0) * (i / max(1, n - 1))
        w = max(1, int(cfg.get("width", 1.2) * SS * (1.0 if i % 2 == 0 else 0.6)))
        d.arc([cx - r, cy - r, cx + r, cy + r], start=a0, end=a1,
              fill=int(255 * (0.30 + 0.70 * ((i * 7) % 10) / 10)), width=w)
    field = np.asarray(canvas.filter(
        ImageFilter.GaussianBlur(cfg.get("soft", 3) * SS * 0.5)),
        dtype=np.float64) / 255.0
    g = gate_mask(xs, ys, cfg.get("gates", []))
    img += (field * g * cfg.get("alpha", 0.5))[..., None] * \
        hx(cfg.get("color", "7FB2FF"))[None, None, :]
    return img


def add_wireframe(img, xs, ys, cfg):
    """Projected 3D heightfield wireframe (blueprint/HUD terrain). Fills ride on
    a translucent RGBA overlay - occlusion without burying the strokes; rows are
    drawn far -> near with brighter lines toward the viewer."""
    Hs, Ws = img.shape[:2]
    canvas = Image.new("RGBA", (Ws, Hs), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    cols, rows = cfg.get("cols", 26), cfg.get("rows", 11)
    x0, y0, wd, ht = cfg["x0"], cfg["y0"], cfg["w"], cfg["h"]
    amp, fx, fy = cfg.get("amp", 0.85), cfg.get("fx", 2.2), cfg.get("fy", 1.6)
    lift = cfg.get("lift", 0.42)
    dx, dy = cfg.get("dx", 0.22), cfg.get("dy", 0.10)
    fa = int(255 * cfg.get("fill_alpha", 0.38))
    fill_c = tuple(int(c) for c in hx(cfg.get("fill_color", "0A1E3C")))
    line_c = hx(cfg.get("line_color", "6FBCFF"))

    def zz(u, v):
        return amp * (0.55 * np.sin(u * fx + cfg.get("ph", 0.6))
                      + 0.45 * np.cos(v * fy + u * 1.3))

    grid = []
    for j in range(rows + 1):
        row = []
        for i in range(cols + 1):
            u, v = i / cols, j / rows
            z = float(zz(u, v))
            row.append(((x0 + u * wd + z * dx) * PX_IN,
                        (y0 + v * ht - z * lift * ht * 0.5 + z * dy) * PX_IN))
        grid.append(row)
    for j in range(rows):
        poly = [p for p in grid[j]] + [p for p in grid[j + 1]][::-1]
        d.polygon(poly, fill=fill_c + (fa,))
    # strokes in a second pass - polygon fills would otherwise overwrite the
    # pixel values of lines drawn earlier (ImageDraw replaces, not blends)
    for j in range(1, rows + 1):
        near = (j - 1) / max(1, rows - 1)
        floor = cfg.get("line_floor", 0.45)
        c = tuple(int(v * (floor + (1 - floor) * near)) for v in line_c)
        d.line(grid[j], fill=c + (255,),
               width=max(1, int(cfg.get("line_w", 1.4) * SS)), joint="curve")
    layer = np.asarray(canvas, dtype=np.float64)
    rgb, a = layer[..., :3], layer[..., 3:] / 255.0
    a = a * gate_mask(xs, ys, cfg.get("gates", []))[..., None] * cfg.get("alpha", 0.95)
    img[:] = img * (1 - a) + rgb * a
    return img


def add_layer(img, xs, ys, layer):
    kind = layer.get("type")
    if kind == "path_ribbon":
        return add_path_ribbon(img, xs, ys, layer)
    if kind == "dots":
        return add_scatter(img, xs, ys, layer)
    if kind == "arc_field":
        return add_arc_field(img, xs, ys, layer)
    if kind == "wireframe":
        return add_wireframe(img, xs, ys, layer)
    raise ValueError(f"unknown layer type {kind!r}")


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
    for layer in cfg.get("layers", []):
        img = add_layer(img, xs, ys, layer)
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
