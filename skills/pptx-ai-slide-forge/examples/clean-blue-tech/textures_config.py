"""pptx-ai-slide-forge :: background configs for the 3-slide Clean Blue Tech demo
(light corporate: white base with pale blue washes, subtle rims, faint dots).

The liquid engine in light mode: same math, inverted luminance logic - no
darken zones, whisper vignette, accents at low alpha. Generate:

    python3 ../../scripts/make_textures.py --config textures_config.py
"""
OUT = "assets"

SLIDES = {
    1: dict(  # cover: pale washes right, white headline zone left
        engine="liquid",
        base=[(0.0, "FFFFFF"), (0.45, "F5F9FE"), (0.75, "EAF2FB"), (1.0, "DCE8F7")],
        glows=[(0.85, 0.12, 0.55, "DCE8F7", 0.55), (0.06, 1.0, 0.45, "EDF3FA", 0.45),
               (0.55, 0.45, 0.8, "E4EEF9", 0.35)],
        ribbons=[
            dict(y0=7.2, slope=-0.26, waves=[(0.9, 5.2, 1.1)], w0=1.0,
                 c1="E4EEF9", c2="CFE2F6", alpha=0.7, depth="mid",
                 rim="B8D2EF", rim1a=0.5),
            dict(y0=6.9, slope=-0.24, waves=[(1.0, 6.8, 0.3), (0.25, 1.9, 2.2)], w0=0.4,
                 c1="D3E3F6", c2="B8D2EF", alpha=0.65, rim="9DBCE8", rim1a=0.55),
        ],
        layers=[
            dict(type="dots", pitch=30, dot=2.5, focus=[0.9, 0.1], falloff=1.5,
                 alpha=0.12, color="70A3DD",
                 gates=[("x", 8.8, None, 1.6), ("y", None, 3.0, 1.2)]),
        ],
        vignette=0.10,
        checks={"headline zone": (0.5, 1.9, 7.2, 5.6)},
    ),
    2: dict(  # contents: royal field with soft radial lift (covered by solid fill)
        engine="liquid",
        base=[(0.0, "2456A0"), (0.55, "1D4A94"), (1.0, "173A70")],
        glows=[(0.85, 0.10, 0.55, "4C79C4", 0.35), (0.05, 1.0, 0.45, "173A70", 0.30)],
        ribbons=[
            dict(y0=7.4, slope=-0.25, waves=[(0.9, 5.4, 1.2)], w0=0.9,
                 c1="1D4A94", c2="3474C8", alpha=0.55, depth="mid",
                 rim="9DBCE8", rim1a=0.35),
        ],
        vignette=0.18,
        checks={},
    ),
    3: dict(  # network: quiet wash + faint grid dots top-right
        engine="liquid",
        base=[(0.0, "FFFFFF"), (0.5, "F5F9FE"), (1.0, "E4EEF9")],
        glows=[(0.90, 0.10, 0.5, "DCE8F7", 0.5), (0.05, 1.0, 0.45, "EDF3FA", 0.4)],
        ribbons=[
            dict(y0=7.3, slope=-0.20, waves=[(0.8, 4.8, 1.3)], w0=0.7,
                 c1="E4EEF9", c2="D3E3F6", alpha=0.6, depth="mid",
                 rim="B8D2EF", rim1a=0.4,
                 gates=[("y", 5.8, None, 1.0), ("x", 4.6, None, 1.6)]),
        ],
        layers=[
            dict(type="dots", pitch=30, dot=2.5, focus=[0.9, 0.08], falloff=1.5,
                 alpha=0.10, color="70A3DD",
                 gates=[("x", 9.6, None, 1.5), ("y", None, 2.2, 1.0)]),
        ],
        vignette=0.08,
        checks={},
    ),
}
