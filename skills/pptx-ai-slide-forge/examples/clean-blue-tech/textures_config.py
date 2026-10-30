"""pptx-ai-slide-forge :: background configs for the 3-slide Clean Blue Tech demo
(LIGHT corporate: white base with VISIBLE pale blue silk waves, dot grids, soft
radial washes - presence without darkness).

Light mode of the liquid engine: same math, inverted luminance logic - NO
vignette crushing, NO darken zones; texture stays light but has definition.
Generate:

    python3 ../../scripts/make_textures.py --config textures_config.py
"""
OUT = "assets"

SLIDES = {
    1: dict(  # cover: white field, DEFINED silk bands sweeping bottom-right,
        #       faint dot grid top-right; headline zone stays near-white
        engine="liquid",
        base=[(0.0, "FFFFFF"), (0.40, "F5F9FE"), (0.72, "E9F1FB"), (1.0, "D8E6F6")],
        glows=[(0.88, 0.88, 0.65, "D2E2F5", 0.75), (0.08, 0.06, 0.5, "F3F8FD", 0.45),
               (0.62, 0.55, 0.95, "E9F1FB", 0.45)],
        ribbons=[
            dict(y0=6.7, slope=-0.22, waves=[(0.75, 5.4, 1.2), (0.28, 2.0, 2.1)], w0=1.25,
                 c1="D2E2F5", c2="BED7F1", alpha=0.75, depth="mid",
                 rim="A6C6EA", rim1a=0.5, rim2a=0.3),
            dict(y0=7.1, slope=-0.20, waves=[(0.95, 6.6, 0.4), (0.22, 1.8, 1.7)], w0=0.5,
                 c1="C6DCF4", c2="AFCCF0", alpha=0.7, rim="92B8E6", rim1a=0.55),
        ],
        layers=[
            dict(type="dots", pitch=30, dot=2.5, focus=[0.9, 0.08], falloff=1.5,
                 alpha=0.20, color="70A3DD",
                 gates=[("x", 8.6, None, 1.6), ("y", None, 3.0, 1.2)]),
        ],
        vignette=0,
        checks={"headline zone": (0.5, 1.9, 6.8, 5.8)},
    ),
    2: dict(  # contents: royal blue field with depth (the slide keeps it as bg)
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
    3: dict(  # network: clean white + soft radial wash behind the diagram + dots
        engine="liquid",
        base=[(0.0, "FFFFFF"), (0.5, "F7FAFD"), (1.0, "E8F1FB")],
        glows=[(0.78, 0.52, 0.7, "DCE8F7", 0.6), (0.06, 0.06, 0.4, "F3F8FD", 0.35)],
        ribbons=[
            dict(y0=7.15, slope=-0.18, waves=[(0.7, 4.6, 1.4)], w0=0.85,
                 c1="E8F1FB", c2="D6E4F5", alpha=0.65, depth="mid",
                 rim="B8D2EF", rim1a=0.4,
                 gates=[("y", 6.1, None, 1.0), ("x", 4.4, None, 1.5)]),
        ],
        layers=[
            dict(type="dots", pitch=30, dot=2.5, focus=[0.92, 0.07], falloff=1.5,
                 alpha=0.16, color="70A3DD",
                 gates=[("x", 9.8, None, 1.5), ("y", None, 2.2, 1.0)]),
        ],
        vignette=0,
        checks={},
    ),
}
