"""pptx-ai-slide-forge :: shape gallery - v1.1 composable layer configs.

Four showcase slides for the v1.1 layer vocabulary (path_ribbon, dots,
arc_field, wireframe) over the liquid base. Generate:

    python3 ../../scripts/make_textures.py --config textures_config.py --out out

Then READ out/bg_01..04.png - numbers prove darkness, eyes prove style.
"""
OUT = "out"

BASE_DARKEN_TITLE = (0.30, 0.25, 12.60, 1.80, 0.42, 0.8)

SLIDES = {
    1: dict(  # HUD hero: liquid base + arc field + orbital ring + dots, top-right
        engine="liquid",
        glows=[(0.78, 0.24, 0.5, "075BFF", 0.30), (0.10, 1.0, 0.45, "0A2D92", 0.32)],
        ribbons=[
            dict(y0=7.4, slope=-0.33, waves=[(1.15, 5.4, 1.1)], w0=1.25,
                 c1="071D60", c2="0873FF", alpha=0.88, depth="mid", rim="8FC5FF", rim1a=0.5),
            dict(y0=7.05, slope=-0.31, waves=[(1.25, 7.6, 0.2), (0.3, 2.1, 2.4)], w0=0.78,
                 c1="0743BC", c2="5DA9FF", alpha=0.9, rim="C1E1FF", rim1a=0.75, rim2a=0.5),
        ],
        layers=[
            dict(type="arc_field", cx=12.1, cy=1.2, r0=1.0, r1=3.4, count=7,
                 a0=150, a1=330, width=1.3, alpha=0.55, color="7FB2FF",
                 gates=[("x", 8.6, None, 1.6), ("y", None, 3.4, 1.2)]),
            dict(type="path_ribbon", w0=0.10, alpha=0.95, rim="E8F4FF", rim_alpha=0.9,
                 path=dict(kind="arc", cx=12.0, cy=3.6, r=3.0, a0=-70, a1=110),
                 c1="0873FF", c2="B5D7FF"),
            dict(type="dots", pitch=26, dot=3, focus=[0.86, 0.12], falloff=1.5,
                 alpha=0.12, color="5B8AD4",
                 gates=[("x", 9.0, None, 1.5), ("y", None, 3.2, 1.2)]),
        ],
        darken=[(0.35, 2.55, 8.9, 6.45, 0.5, 1.1), BASE_DARKEN_TITLE],
        vignette=0.3,
        checks={"headline zone": (0.8, 2.9, 8.4, 6.2)},
    ),
    2: dict(  # swoosh: two bezier light trails across the canvas
        engine="liquid",
        glows=[(0.30, 0.90, 0.5, "0A2D92", 0.35), (0.85, 0.16, 0.5, "075BFF", 0.28)],
        ribbons=[],
        layers=[
            dict(type="path_ribbon", w0=0.62, alpha=0.9, soft=14,
                 path=dict(kind="bezier",
                           pts=[[0.2, 6.9], [4.2, 4.6], [8.4, 5.2], [13.1, 1.6]]),
                 c1="071D60", c2="5DA9FF", rim="C1E1FF", rim_alpha=0.75),
            dict(type="path_ribbon", w0=0.14, alpha=0.95, soft=8,
                 path=dict(kind="bezier",
                           pts=[[0.4, 6.7], [4.3, 4.4], [8.5, 5.0], [13.0, 1.4]]),
                 c1="0873FF", c2="C1E1FF", rim="E8F4FF", rim_alpha=0.8),
            dict(type="dots", pitch=30, dot=3, focus=[0.06, 0.94], falloff=1.8,
                 alpha=0.10, color="5B8AD4", gates=[("x", None, 5.2, 1.4), ("y", 5.6, None, 1.2)]),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 9.6, 5.9, 0.30, 1.1)],
        vignette=0.32,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "body zone": (0.5, 1.9, 12.6, 5.8)},
    ),
    3: dict(  # wireframe terrain content slide: quiet base + mesh bottom-right
        engine="liquid",
        glows=[(0.05, 1.0, 0.45, "0A2D92", 0.32), (1.0, 0.05, 0.4, "075BFF", 0.26),
               (0.72, 0.55, 0.6, "08266E", 0.35)],
        ribbons=[],
        layers=[
            dict(type="wireframe", x0=5.3, y0=4.05, w=7.6, h=2.9, cols=30, rows=12,
                 amp=0.85, fx=2.4, fy=1.7, lift=0.40, ph=0.8,
                 line_color="6FBCFF", fill_color="0A1E3C", fill_alpha=0.35, alpha=0.95,
                 line_w=1.7, line_floor=0.62),
            dict(type="dots", pitch=26, dot=3, focus=[0.95, 0.05], falloff=1.6,
                 alpha=0.10, color="5B8AD4", gates=[("x", 10.2, None, 1.4), ("y", None, 1.9, 1.0)]),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 5.2, 6.9, 0.18, 1.0), (5.4, 1.9, 12.9, 3.9, 0.14, 0.9)],
        vignette=0.28,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "left body": (0.5, 1.9, 5.2, 6.8)},
    ),
    4: dict(  # ring emblem section divider: centered orbital composition
        engine="liquid",
        glows=[(0.62, 0.42, 0.6, "075BFF", 0.30), (0.05, 0.05, 0.4, "0A35A2", 0.25)],
        ribbons=[],
        layers=[
            dict(type="path_ribbon", w0=0.12, alpha=0.95, rim="C1E1FF", rim_alpha=0.85,
                 path=dict(kind="ring", cx=6.67, cy=3.75, r=2.1),
                 c1="0873FF", c2="B5D7FF"),
            dict(type="arc_field", cx=6.67, cy=3.75, r0=2.5, r1=3.6, count=5,
                 a0=200, a1=340, width=1.2, alpha=0.6, color="7FB2FF"),
            dict(type="dots", pitch=28, dot=3, focus=[0.5, 0.5], falloff=2.2,
                 alpha=0.12, color="5B8AD4", gates=[("x", 3.2, 10.1, 1.6), ("y", 1.2, 6.3, 1.2)]),
        ],
        darken=[(0.30, 0.25, 12.60, 1.80, 0.42, 0.8), (0.6, 5.4, 12.8, 6.9, 0.30, 1.0)],
        vignette=0.34,
        checks={"center emblem": (4.0, 1.2, 9.3, 6.3)},
    ),
}
