"""Background configs for the 3-slide English demo (NovaPay Liquid Electric Blue).

Slides 1-3 of the full 8-slide SDD deck config (see ../sdd-deck/textures_config.py).
Generate with:
    python3 ../../scripts/make_textures.py --config textures_config.py --out ../../assets
"""
OUT = "../../assets"

SLIDES = {
    1: dict(  # hero: main arc bottom-left -> upper-right, depth waves top/right
        engine="liquid",
        glows=[(0.74, 0.28, 0.55, "075BFF", 0.30), (0.12, 0.98, 0.5, "0A2D92", 0.35),
               (0.98, 0.06, 0.45, "1738D9", 0.22)],
        ribbons=[
            dict(y0=6.6, slope=-0.36, waves=[(1.0, 6.4, 0.4), (0.35, 2.4, 1.9)], w0=1.9,
                 c1="02102D", c2="0743BC", alpha=0.9, depth="back", blur=55, rim="5DA9FF",
                 rim1a=0.28, rim2a=0.16),
            dict(y0=7.4, slope=-0.33, waves=[(1.15, 5.4, 1.1)], w0=1.25,
                 c1="071D60", c2="0873FF", alpha=0.88, depth="mid", rim="8FC5FF", rim1a=0.5),
            dict(y0=7.05, slope=-0.31, waves=[(1.25, 7.6, 0.2), (0.3, 2.1, 2.4)], w0=0.78,
                 c1="0743BC", c2="5DA9FF", alpha=0.9, rim="C1E1FF", rim1a=0.75, rim2a=0.5),
            dict(y0=6.55, slope=-0.29, waves=[(1.25, 7.6, 0.24), (0.3, 2.1, 2.44)], w0=0.16,
                 c1="0873FF", c2="B5D7FF", alpha=0.95, rim="E8F4FF", rim1a=0.9, rim2a=0.0),
            dict(y0=-0.6, slope=0.24, waves=[(0.8, 4.6, 1.7)], w0=1.4,
                 c1="02102D", c2="0A35A2", alpha=0.75, depth="back", blur=45,
                 gates=[("y", None, 2.4, 0.9)], rim="5DA9FF", rim1a=0.3),
            dict(y0=1.1, slope=0.10, waves=[(0.5, 3.4, 0.6)], w0=0.85,
                 c1="071D60", c2="0873FF", alpha=0.8, depth="mid",
                 gates=[("x", 8.6, None, 1.6)], rim="C1E1FF", rim1a=0.55),
        ],
        darken=[(0.35, 2.55, 8.9, 6.45, 0.52, 1.1), (0.0, 0.0, 6.5, 1.4, 0.4, 0.9)],
        vignette=0.3,
        checks={"headline zone": (0.8, 2.9, 8.4, 6.2), "top-right": (10.5, 0.2, 13.0, 1.6)},
    ),
    2: dict(  # feature: fan top-right, calm left
        engine="liquid",
        glows=[(0.92, 0.10, 0.5, "075BFF", 0.30), (0.05, 1.02, 0.45, "0A2D92", 0.30)],
        ribbons=[
            dict(y0=0.4, slope=0.16, waves=[(0.9, 3.8, 0.4)], w0=1.05,
                 c1="071D60", c2="5DA9FF", alpha=0.85, depth="mid",
                 gates=[("x", 7.2, None, 2.2), ("y", None, 2.9, 1.2)], rim="C1E1FF", rim1a=0.7),
            dict(y0=1.4, slope=0.12, waves=[(0.7, 4.4, 1.5)], w0=0.8,
                 c1="0743BC", c2="0873FF", alpha=0.85,
                 gates=[("x", 8.4, None, 2.0), ("y", None, 3.4, 1.2)], rim="C1E1FF", rim1a=0.6),
            dict(y0=8.1, slope=-0.24, waves=[(0.9, 6.2, 0.9)], w0=1.35,
                 c1="02102D", c2="0743BC", alpha=0.8, depth="back", blur=40,
                 gates=[("y", 5.4, None, 1.2)], rim="5DA9FF", rim1a=0.3),
            dict(y0=7.6, slope=-0.22, waves=[(0.8, 5.0, 1.8)], w0=0.5,
                 c1="0743BC", c2="5DA9FF", alpha=0.85,
                 gates=[("x", None, 6.4, 2.0), ("y", 5.8, None, 1.0)], rim="C1E1FF", rim1a=0.6),
        ],
        darken=[(0.30, 0.25, 12.60, 1.80, 0.42, 0.8), (0.4, 2.0, 6.6, 6.4, 0.30, 1.0),
                (6.6, 3.2, 12.9, 5.6, 0.28, 1.0)],
        vignette=0.32,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "cards zone": (0.5, 2.0, 12.6, 5.6)},
    ),
    3: dict(  # three levels: corner accents, quiet middle band
        engine="liquid",
        glows=[(1.0, 0.0, 0.45, "075BFF", 0.28), (0.0, 1.05, 0.5, "0A35A2", 0.30)],
        ribbons=[
            dict(y0=-0.4, slope=0.34, waves=[(0.7, 3.6, 0.8)], w0=1.0,
                 c1="071D60", c2="4DA0FF", alpha=0.85,
                 gates=[("x", 9.0, None, 1.8), ("y", None, 2.2, 1.0)], rim="C1E1FF", rim1a=0.65),
            dict(y0=7.9, slope=-0.30, waves=[(0.9, 5.8, 1.2)], w0=1.25,
                 c1="02102D", c2="0A35A2", alpha=0.82, depth="back", blur=42,
                 gates=[("y", 5.2, None, 1.2), ("x", None, 8.4, 2.4)], rim="5DA9FF", rim1a=0.3),
            dict(y0=7.7, slope=-0.28, waves=[(0.7, 4.2, 2.1)], w0=0.45,
                 c1="0743BC", c2="5DA9FF", alpha=0.85,
                 gates=[("y", 5.6, None, 1.0), ("x", None, 7.0, 1.8)], rim="C1E1FF", rim1a=0.6),
        ],
        darken=[(0.30, 0.25, 12.60, 1.80, 0.42, 0.8), (0.4, 1.85, 12.9, 6.9, 0.26, 1.2)],
        vignette=0.32,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "cards zone": (0.5, 1.9, 12.6, 5.9)},
    ),
}
