"""pptx-ai-slide-forge :: background configs for the 3-slide Dark Emerald demo.

The liquid engine driven by the Dark Emerald Strategy palette: near-black to
deep teal base, emerald glow top-right, mint rims. Generate:

    python3 ../../scripts/make_textures.py --config textures_config.py
"""
OUT = "assets"

BASE_DARKEN_TITLE = (0.30, 0.25, 12.60, 1.80, 0.40, 0.8)
BASE = [(0.0, "050C0F"), (0.45, "0D2424"), (0.80, "0F332B"), (1.0, "164F3D")]

SLIDES = {
    1: dict(  # cover: emerald glow top-right, mint swoosh
        engine="liquid", base=BASE,
        glows=[(0.85, 0.10, 0.55, "51E9A0", 0.16), (0.05, 1.0, 0.5, "0D2424", 0.32)],
        ribbons=[
            dict(y0=7.5, slope=-0.30, waves=[(1.1, 5.6, 1.2)], w0=1.2,
                 c1="0D2424", c2="164F3D", alpha=0.85, depth="mid",
                 rim="B7F5D8", rim1a=0.35),
            dict(y0=7.0, slope=-0.28, waves=[(1.2, 7.4, 0.3), (0.3, 2.0, 2.3)], w0=0.5,
                 c1="0F332B", c2="2E8B6B", alpha=0.9, rim="B7F5D8", rim1a=0.6),
        ],
        layers=[
            dict(type="path_ribbon", w0=0.12, alpha=0.95, soft=8, blend="screen",
                 rim_alpha=0.0,
                 path=dict(kind="bezier",
                           pts=[[0.3, 6.8], [4.4, 4.4], [8.6, 5.1], [13.0, 1.5]]),
                 c1="164F3D", c2="63F5B0"),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 9.6, 5.9, 0.30, 1.1)],
        vignette=0.32,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "body zone": (0.5, 1.9, 12.6, 5.8)},
    ),
    2: dict(  # KPI outcomes: emerald ambient + quiet dots
        engine="liquid", base=BASE,
        glows=[(0.92, 0.08, 0.5, "51E9A0", 0.15), (0.05, 1.02, 0.45, "0D2424", 0.32)],
        ribbons=[
            dict(y0=7.8, slope=-0.24, waves=[(0.9, 6.2, 0.9)], w0=1.3,
                 c1="0D2424", c2="164F3D", alpha=0.8, depth="back", blur=40,
                 gates=[("y", 5.6, None, 1.2)], rim="B7F5D8", rim1a=0.25),
        ],
        layers=[
            dict(type="dots", pitch=28, dot=3, focus=[0.94, 0.06], falloff=1.7,
                 alpha=0.10, color="63F5B0",
                 gates=[("x", 9.4, None, 1.5), ("y", None, 2.6, 1.1)]),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.85, 12.9, 6.7, 0.24, 1.1)],
        vignette=0.32,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "cards zone": (0.5, 1.9, 12.6, 6.0)},
    ),
    3: dict(  # roadmap: quarterly columns, emerald ambient bottom-left
        engine="liquid", base=BASE,
        glows=[(0.06, 0.95, 0.5, "51E9A0", 0.14), (0.95, 0.95, 0.45, "0D2424", 0.30)],
        ribbons=[
            dict(y0=7.9, slope=-0.20, waves=[(0.9, 5.8, 1.0)], w0=1.2,
                 c1="0D2424", c2="164F3D", alpha=0.8, depth="back", blur=40,
                 gates=[("y", 6.4, None, 1.0)], rim="B7F5D8", rim1a=0.25),
        ],
        layers=[
            dict(type="dots", pitch=28, dot=3, focus=[0.06, 0.06], falloff=1.7,
                 alpha=0.10, color="63F5B0", gates=[("x", None, 3.4, 1.2), ("y", None, 2.0, 1.0)]),
        ],
        darken=[BASE_DARKEN_TITLE, (0.4, 1.6, 12.9, 4.0, 0.26, 1.0), (0.4, 4.2, 12.9, 6.6, 0.20, 1.0)],
        vignette=0.32,
        checks={"title strip": (0.4, 0.3, 10.4, 1.75), "roadmap band": (0.5, 1.7, 12.6, 6.2)},
    ),
}
