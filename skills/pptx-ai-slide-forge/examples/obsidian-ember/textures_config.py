"""pptx-ai-slide-forge :: background configs for the 3-slide Obsidian Ember demo.

The liquid engine driven by the ember palette: near-black to burgundy base,
hot-orange glow top-right, copper ribbons with pale-orange rims. Generate:

    python3 ../../scripts/make_textures.py --config textures_config.py
"""
OUT = "assets"

BASE_DARKEN_TITLE = (0.30, 0.25, 12.60, 1.80, 0.45, 0.8)
BASE = [(0.0, "050505"), (0.40, "090708"), (0.72, "300015"), (1.0, "47001D")]

SLIDES = {
    1: dict(  # cover: hot-orange glow top-right, copper swoosh across the canvas
        engine="liquid", base=BASE,
        glows=[(0.86, 0.10, 0.55, "F05A12", 0.22), (0.06, 1.0, 0.5, "8E1015", 0.30),
               (0.45, 0.45, 0.7, "300015", 0.35)],
        ribbons=[
            dict(y0=7.6, slope=-0.32, waves=[(1.15, 5.6, 1.1)], w0=1.2,
                 c1="300015", c2="8E1015", alpha=0.85, depth="mid",
                 rim="FFB380", rim1a=0.45),
            dict(y0=7.0, slope=-0.30, waves=[(1.25, 7.4, 0.2), (0.3, 2.0, 2.4)], w0=0.5,
                 c1="8E1015", c2="F05A12", alpha=0.9, rim="FFC49B", rim1a=0.7),
        ],
        layers=[
            dict(type="path_ribbon", w0=0.12, alpha=0.95, soft=8, blend="screen",
                 rim_alpha=0.0,
                 path=dict(kind="bezier",
                           pts=[[0.3, 6.9], [4.4, 4.5], [8.5, 5.1], [13.0, 1.5]]),
                 c1="E32820", c2="FF6A00"),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 9.6, 5.9, 0.32, 1.1)],
        vignette=0.34,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "body zone": (0.5, 1.9, 12.6, 5.8)},
    ),
    2: dict(  # workflow comparison: ember glow bottom-left, calm center columns
        engine="liquid", base=BASE,
        glows=[(0.05, 0.95, 0.5, "E32820", 0.16), (0.95, 0.06, 0.45, "F05A12", 0.18),
               (0.5, 0.5, 0.8, "300015", 0.35)],
        ribbons=[
            dict(y0=7.9, slope=-0.22, waves=[(0.9, 6.0, 0.9)], w0=1.3,
                 c1="47001D", c2="8E1015", alpha=0.8, depth="back", blur=40,
                 gates=[("y", 6.2, None, 1.0)], rim="FFB380", rim1a=0.3),
        ],
        layers=[
            dict(type="dots", pitch=28, dot=3, focus=[0.94, 0.06], falloff=1.7,
                 alpha=0.10, color="FF6A00",
                 gates=[("x", 9.6, None, 1.5), ("y", None, 2.4, 1.1)]),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 12.9, 6.7, 0.24, 1.1)],
        vignette=0.34,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "columns zone": (0.5, 1.9, 12.6, 6.0)},
    ),
    3: dict(  # KPI metrics: burgundy field, orange glow bottom-left, vertical beams
        engine="liquid", base=BASE,
        glows=[(0.05, 0.95, 0.5, "F05A12", 0.16), (0.95, 0.95, 0.45, "8E1015", 0.22),
               (0.5, 0.45, 0.9, "47001D", 0.30)],
        ribbons=[
            dict(y0=8.0, slope=-0.18, waves=[(0.8, 5.4, 1.3)], w0=1.1,
                 c1="47001D", c2="8E1015", alpha=0.78, depth="back", blur=42,
                 gates=[("y", 6.6, None, 0.9)], rim="FFB380", rim1a=0.28),
        ],
        layers=[
            dict(type="path_ribbon", w0=0.10, alpha=0.9, soft=8, blend="screen",
                 rim_alpha=0.0,
                 path=dict(kind="arc", cx=-1.5, cy=7.8, r=4.6, a0=-55, a1=25),
                 c1="8E1015", c2="FF6A00"),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 12.9, 6.7, 0.24, 1.1)],
        vignette=0.34,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "cards zone": (0.5, 1.9, 12.6, 6.2)},
    ),
}
