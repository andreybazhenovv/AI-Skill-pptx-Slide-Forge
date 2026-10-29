"""pptx-ai-slide-forge :: 3-slide EN demo in the Clean Blue Tech style
(light corporate: white backgrounds, royal-blue accents, vector diagrams).

Photorealistic 3D renders are approximated with clean vector compositions
(parallelogram platforms, spherical antenna ovals, radial node network) -
exactly the `graphics.diagrams` vocabulary of the style spec.

Run from this directory:
    python3 build_demo.py
    bash ../../scripts/render_qa.sh "$PWD/clean-blue-tech.pptx" qa
"""
import os

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "clean-blue-tech.pptx")
EMU_IN = 914400


def IN(v):
    return Emu(int(round(v * EMU_IN)))


# ---- Clean Blue Tech tokens ----
PRIMARY, DEEP, ELECTRIC = "2456A0", "173A70", "3474C8"
LIGHT, ICE, WHITE, OFF = "DCE8F7", "EDF3FA", "FFFFFF", "F8FAFD"
TEXT, SEC, DIV = "202733", "7B8797", "DCE2E9"
FONT = "Arial"
ML = 0.6

prs = Presentation()
prs.slide_width, prs.slide_height = IN(13.333), IN(7.5)
BLANK = prs.slide_layouts[6]


def RGB(h):
    return RGBColor.from_string(h)


def style_run(run, text, pt, color, bold=False):
    run.text = text
    f = run.font
    f.name, f.size, f.bold = FONT, Pt(pt), bold
    f.color.rgb = RGB(color)


def txt(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", PP_ALIGN.LEFT)
        para.line_spacing = p.get("ls", 1.2)
        for r in p["runs"]:
            style_run(para.add_run(), r[0], r[1], r[2], r[3] if len(r) > 3 else False)
    return box


def rect(slide, x, y, w, h, fill=None, line=None, line_w=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, IN(x), IN(y), IN(w), IN(h))
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGB(fill)
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = RGB(line)
        shp.line.width = Pt(line_w)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def oval(slide, x, y, d, dh=None, fill=WHITE, line=PRIMARY, line_w=1.25):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, IN(x), IN(y), IN(d), IN(dh or d))
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGB(fill)
    if line:
        shp.line.color.rgb = RGB(line)
        shp.line.width = Pt(line_w)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def platform(slide, x, y, w, h, fill=LIGHT):
    shp = slide.shapes.add_shape(MSO_SHAPE.PARALLELOGRAM, IN(x), IN(y), IN(w), IN(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = RGB(fill)
    shp.line.color.rgb = RGB(PRIMARY)
    shp.line.width = Pt(1.0)
    shp.shadow.inherit = False
    return shp


def conn(slide, x1, y1, x2, y2, color=PRIMARY, line_w=0.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, IN(x1), IN(y1), IN(x2), IN(y2))
    c.line.color.rgb = RGB(color)
    c.line.width = Pt(line_w)
    return c


def marker(slide, x, y, d=0.16, color=PRIMARY):
    rect(slide, x, y, d, d, color)


def brand(slide, label, page=None):
    marker(slide, ML, 0.5, 0.18)
    txt(slide, ML + 0.3, 0.46, 2.6, 0.28,
        [{"runs": [(label, 11, TEXT, True)]}], anchor=MSO_ANCHOR.MIDDLE)
    if page:
        rect(slide, 12.55, 7.02, 0.16, 0.16, PRIMARY)
        txt(slide, 12.15, 7.0, 0.35, 0.3,
            [{"runs": [(page, 9, SEC)], "ls": 1.0, "align": PP_ALIGN.RIGHT}])


# ============================ SLIDE 1 — COVER ============================
s = prs.slides.add_slide(BLANK)
s.background.fill.solid()
s.background.fill.fore_color.rgb = RGB(OFF)

brand(s, "AI-SLIDE-FORGE")

# hairline technical background lines (right zone)
for y in (1.35, 6.15):
    conn(s, 7.4, y, 12.73, y, color=DIV, line_w=0.75)

# floating platform composition (right): isometric stacks + spherical antenna
platform(s, 7.9, 4.9, 4.4, 0.85, fill=LIGHT)
platform(s, 8.7, 4.15, 3.0, 0.6, fill=ICE)
oval(s, 9.55, 2.45, 1.15, fill=WHITE, line=PRIMARY, line_w=1.5)
oval(s, 9.9, 2.8, 0.45, fill=ELECTRIC, line=None)
conn(s, 9.3, 3.6, 9.3, 4.15, color=PRIMARY, line_w=1.0)
conn(s, 10.9, 3.6, 10.9, 4.15, color=PRIMARY, line_w=1.0)
marker(s, 8.05, 5.1, 0.1)
marker(s, 11.9, 4.55, 0.1)

txt(s, ML, 2.05, 6.6, 1.85, [
    {"runs": [("Enterprise AI", 34, TEXT, True)], "ls": 1.05},
    {"runs": [("infrastructure", 34, TEXT, True)], "ls": 1.05},
])
txt(s, ML, 4.0, 6.0, 0.9,
    [{"runs": [("A modular platform for edge intelligence -", 16, SEC)], "ls": 1.3},
     {"runs": [("built with a spec-driven engineering process.", 16, SEC)], "ls": 1.3}])
rect(s, ML, 5.15, 2.4, 0.02, DIV)
txt(s, ML, 5.35, 6.0, 0.35,
    [{"runs": [("2026 PRODUCT OVERVIEW", 10, PRIMARY, True)], "ls": 1.0}])

# ============================ SLIDE 2 — CONTENTS ============================
s = prs.slides.add_slide(BLANK)
s.background.fill.solid()
s.background.fill.fore_color.rgb = RGB(PRIMARY)

marker(s, ML, 0.5, 0.18, color=WHITE)
txt(s, ML + 0.3, 0.46, 2.6, 0.28,
    [{"runs": [("AI-SLIDE-FORGE", 11, WHITE, True)]}], anchor=MSO_ANCHOR.MIDDLE)
txt(s, ML, 0.85, 3.2, 1.2, [{"runs": [("Contents", 40, WHITE, True)], "ls": 1.0}])
rect(s, ML, 2.15, 1.6, 0.025, WHITE)

items = [
    ("01", "Platform overview"), ("02", "Network topology"),
    ("03", "Deployment model"), ("04", "Reliability metrics"),
    ("05", "Security boundaries"), ("06", "Roadmap"),
]
for i, (num, desc) in enumerate(items):
    col, row = i % 2, i // 2
    x = 4.3 + col * 4.6
    y = 1.55 + row * 1.75
    txt(s, x, y, 1.0, 0.6, [{"runs": [(num, 24, WHITE, True)], "ls": 1.0}])
    txt(s, x, y + 0.62, 4.0, 0.4,
        [{"runs": [(desc, 12, "DCE8F7")], "ls": 1.2}])
    conn(s, x, y + 1.25, x + 3.9, y + 1.25, color="3D6BB5", line_w=0.75)

rect(s, 12.55, 7.02, 0.16, 0.16, WHITE)
txt(s, 12.15, 7.0, 0.35, 0.3,
    [{"runs": [("02", 9, "DCE8F7")], "ls": 1.0, "align": PP_ALIGN.RIGHT}])

# ============================ SLIDE 3 — NETWORK ============================
s = prs.slides.add_slide(BLANK)
s.background.fill.solid()
s.background.fill.fore_color.rgb = RGB(OFF)

marker(s, ML, 0.5, 0.18)
txt(s, ML + 0.3, 0.46, 2.6, 0.28,
    [{"runs": [("04 · NETWORK", 11, TEXT, True)]}], anchor=MSO_ANCHOR.MIDDLE)

txt(s, ML, 1.6, 1.4, 0.8, [{"runs": [("04", 34, PRIMARY, True)], "ls": 1.0}])
txt(s, ML, 2.45, 5.2, 0.75,
    [{"runs": [("Network at a glance", 26, TEXT, True)], "ls": 1.05}])
rect(s, ML, 3.35, 4.9, 0.02, DIV)

txt(s, ML, 3.7, 5.2, 1.0, [{"runs": [("99.95%", 44, PRIMARY, True)], "ls": 1.0}])
txt(s, ML, 4.75, 5.0, 1.4,
    [{"runs": [("Measured availability across all edge regions for the last "
                "twelve months, verified by the external monitoring probe.",
                12, SEC)], "ls": 1.35}])

# radial node network (right)
cx, cy = 9.9, 3.9
import math
sat_r, orb = 0.34, 1.75
sats = []
for k in range(7):
    ang = math.radians(-90 + k * (360 / 7))
    sx, sy = cx + orb * math.cos(ang) - sat_r / 2, cy + orb * math.sin(ang) - sat_r / 2
    conn(s, cx, cy, sx + sat_r / 2, sy + sat_r / 2, color=PRIMARY, line_w=0.75)
    sats.append((sx, sy))
for sx, sy in sats:
    oval(s, sx, sy, sat_r, fill=WHITE, line=PRIMARY, line_w=1.25)
oval(s, cx - 0.45, cy - 0.45, 0.9, fill=PRIMARY, line=None)

for sx, sy, label in [(sats[1][0] - 1.6, sats[1][1] - 0.05, "REGION A"),
                      (sats[4][0] + 0.5, sats[4][1] - 0.05, "REGION B")]:
    rect(s, sx, sy, 1.1, 0.3, fill=ICE)
    txt(s, sx, sy, 1.1, 0.3, [{"runs": [(label, 8, PRIMARY, True)], "ls": 1.0,
                               "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)

rect(s, 12.55, 7.02, 0.16, 0.16, PRIMARY)
txt(s, 12.15, 7.0, 0.35, 0.3,
    [{"runs": [("03", 9, SEC)], "ls": 1.0, "align": PP_ALIGN.RIGHT}])

prs.core_properties.title = "Enterprise AI infrastructure (Clean Blue Tech demo)"
prs.save(OUT)
print(f"saved {OUT}, slides: {len(prs.slides._sldIdLst)}")

issues, sw, sh = [], prs.slide_width, prs.slide_height
for idx, slide in enumerate(prs.slides, start=1):
    boxes = []
    for shp in slide.shapes:
        if shp.left is None:
            continue
        if shp.left < -1000 or shp.top < -1000 or shp.left + shp.width > sw + 1000 \
                or shp.top + shp.height > sh + 1000:
            issues.append(f"slide {idx}: out of bounds")
        if shp.has_text_frame and shp.text_frame.text.strip():
            boxes.append((shp.left, shp.top, shp.width, shp.height, shp.text_frame.text[:24]))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ix = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
            iy = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
            if (ix / EMU_IN) * (iy / EMU_IN) > 0.05:
                issues.append(f"slide {idx}: overlap \u00ab{a[4]}\u00bb \u00d7 \u00ab{b[4]}\u00bb")
print("geometry:", issues if issues else "clean")
