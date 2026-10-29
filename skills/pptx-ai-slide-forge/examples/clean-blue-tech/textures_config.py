"""pptx-ai-slide-forge :: background configs for the 3-slide Clean Blue Tech demo
(LIGHT corporate: white base, pale blue washes, silk ribbon bands, faint dots).

Light mode of the liquid engine: same math as dark styles, inverted luminance
logic - NO vignette crushing, NO darken zones; texture stays subtle so the
slides read as clean white corporate pages. Generate:

    python3 ../../scripts/make_textures.py --config textures_config.py
"""
OUT = "assets"

SLIDES = {
    1: dict(  # cover: white field, pale blue silk bands sweeping bottom-right,
        #       faint dot grid top-right; headline zone stays pure white
        engine="liquid",
        base=[(0.0, "FFFFFF"), (0.45, "F7FAFD"), (0.75, "EDF3FA"), (1.0, "DCE8F7")],
        glows=[(0.88, 0.85, 0.6, "DCE8F7", 0.55), (0.10, 0.08, 0.5, "F3F8FD", 0.40),
               (0.60, 0.55, 0.9, "EDF3FA", 0.35)],
        ribbons=[
            dict(y0=6.6, slope=-0.22, waves=[(0.7, 5.6, 1.2), (0.25, 2.0, 2.1)], w0=1.1,
                 c1="D6E4F5", c2="C3D9F0", alpha=0.6, depth="mid",
                 rim="AFC9EA", rim1a=0.35, rim2a=0.2),
            dict(y0=7.0, slope=-0.20, waves=[(0.9, 6.6, 0.4), (0.2, 1.8, 1.7)], w0=0.45,
                 c1="CBDFF4", c2="B9D1EF", alpha=0.55, rim="9FBFE6", rim1a=0.4),
        ],
        layers=[
            dict(type="dots", pitch=30, dot=2.5, focus=[0.9, 0.08], falloff=1.5,
                 alpha=0.16, color="70A3DD",
                 gates=[("x", 8.6, None, 1.6), ("y", None, 3.0, 1.2)]),
        ],
        vignette=0.05,
        checks={"headline zone": (0.5, 1.9, 6.8, 5.8)},
    ),
    2: dict(  # contents: royal blue field (the slide covers it with solid PRIMARY;
        #       texture only adds depth where visible at edges)
        engine="liquid",
        base=[(0.0, "2456A0"), (0.55, "1D4A94"), (1.0, "173A70")],
        glows=[(0.88, 0.10, 0.6, "4C79C4", 0.40), (0.05, 1.0, 0.45, "173A70", 0.35)],
        ribbons=[
            dict(y0=7.5, slope=-0.24, waves=[(0.9, 5.6, 1.2)], w0=1.0,
                 c1="1D4A94", c2="3474C8", alpha=0.55, depth="mid",
                 rim="9DBCE8", rim1a=0.35),
        ],
        vignette=0.16,
        checks={},
    ),
    3: dict(  # network: clean white + soft glow behind the diagram + faint dots
        engine="liquid",
        base=[(0.0, "FFFFFF"), (0.5, "F7FAFD"), (1.0, "E8F1FB")],
        glows=[(0.78, 0.52, 0.65, "DCE8F7", 0.5), (0.06, 0.06, 0.4, "F3F8FD", 0.35)],
        ribbons=[
            dict(y0=7.15, slope=-0.18, waves=[(0.7, 4.6, 1.4)], w0=0.8,
                 c1="E8F1FB", c2="D6E4F5", alpha=0.6, depth="mid",
                 rim="B8D2EF", rim1a=0.35,
                 gates=[("y", 6.1, None, 1.0), ("x", 4.4, None, 1.5)]),
        ],
        layers=[
            dict(type="dots", pitch=30, dot=2.5, focus=[0.92, 0.07], falloff=1.5,
                 alpha=0.14, color="70A3DD",
                 gates=[("x", 9.8, None, 1.5), ("y", None, 2.2, 1.0)]),
        ],
        vignette=0.06,
        checks={},
    ),
}
