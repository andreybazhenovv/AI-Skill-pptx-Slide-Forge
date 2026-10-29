# Styles

A **style specification** is a JSON description of a deck's visual language. It is the
single source of truth the agent translates into three artifacts:

| Spec section | Lands in |
|---|---|
| `color_palette`, `typography`, `canvas` | theme tokens at the top of `scripts/build_deck.py` |
| `background_system`, `geometry_and_forms`, `background_variants` | per-slide configs for `scripts/make_textures.py` (`references/background-engine.md`) |
| `glass_card_system`, `card_variants`, `layout_system`, `micro_details` | slide layout recipes (`references/slide-patterns.md`) |
| `design_constraints`, `negative_prompt` | QA checklist items (what a reviewer must reject) |

Four complete specs ship with this skill (below): **Midnight Electric Blue**,
**NovaPay — Liquid Electric Blue** (dark; the second one built the worked example deck
end to end), **Clean Blue Tech** (light corporate — flat backgrounds + vector decor
overlays instead of the texture engine) and **Dark Emerald Strategy** (dark executive
roadmap — emerald glow via the liquid engine with an emerald palette). All were
authored by visual analysis of reference images — treat every HEX/size as a tuned
approximation, not extracted design tokens.

Units: background specs speak **px at 1920x1080**; the PPTX canvas is 13.333 x 7.5 in,
so **1 px at 1920 = 0.5 pt** on the slide (e.g. headline 80 px → 40 pt, radius 18 px →
0.125 in).

---

## Style 1: Midnight Electric Blue

```json
{
  "style_name": "Midnight Electric Blue",
  "style_category": "Premium Tech / Futuristic Digital / Dark Editorial",
  "description": "Premium technological presentation style with a near-black background, saturated electric blue accents, large typography, 3D objects, glow and complex geometric textures.",
  "overall_mood": {
    "keywords": ["futuristic", "technological", "premium", "minimalist", "cinematic", "high-contrast", "dynamic", "intellectual", "experimental"],
    "visual_density": "Medium, alternating minimalist slides and dense information compositions",
    "visual_hierarchy": "Very strong",
    "contrast": "High",
    "atmosphere": "Dark digital environment with controlled bright accents"
  },
  "canvas": {
    "aspect_ratio": "16:9",
    "recommended_resolution": {"width": 1920, "height": 1080},
    "background": {"primary": "#090C14", "secondary": "#0D111C", "tertiary": "#121824",
      "avoid": ["white background", "light pastel fills", "warm colored backgrounds"]},
    "safe_margins": {"horizontal": "3.5-5%", "vertical": "5-7%"},
    "grid": {"columns": 12, "gutter": "20-28 px at 1920px width",
      "alignment": "Asymmetric editorial grid",
      "principle": "Strict modular grid with deliberate asymmetry and large free zones"}
  },
  "color_palette": {
    "primary_colors": [
      {"name": "Midnight Black", "hex": "#090C14", "usage": "Main slide background"},
      {"name": "Deep Navy", "hex": "#0C1730", "usage": "Secondary dark surfaces"},
      {"name": "Electric Blue", "hex": "#0866F5", "usage": "Primary accent, active blocks, buttons, charts"},
      {"name": "Bright Digital Blue", "hex": "#127BFF", "usage": "Glow, gradients, data highlights"},
      {"name": "Ice Blue", "hex": "#A8D8FF", "usage": "Light areas of gradients and 3D textures"}
    ],
    "neutral_colors": [
      {"name": "Pure White", "hex": "#FFFFFF", "usage": "Main headlines"},
      {"name": "Cool Gray", "hex": "#9298A6", "usage": "Secondary headlines"},
      {"name": "Muted Gray", "hex": "#626B7C", "usage": "Captions, metadata"},
      {"name": "Border Gray", "hex": "#222A39", "usage": "Dividers and card borders"}
    ],
    "distribution": {"dark_background": "75-85%", "white_typography": "8-12%",
      "electric_blue": "5-10%", "gray_details": "3-5%"},
    "color_rules": [
      "Use no more than one bright accent color",
      "Build the main contrast on white and near-black",
      "Blue is used mostly for visual accents",
      "Large colored areas must be deep, not flat",
      "Add soft transitions between blue and black"
    ]
  },
  "typography": {
    "style": "Modern Neo-Grotesk / Swiss Editorial",
    "recommended_fonts": ["Inter", "Helvetica Neue", "Arial", "Manrope", "Suisse Intl", "Onest"],
    "font_characteristics": ["Neutral grotesque", "Geometrically clean letterforms",
      "Good Cyrillic readability", "High setting density", "Minimal decorative character"],
    "headline": {"font_weight": "400-500", "font_size": "72-110 px at 1920x1080",
      "line_height": "0.95-1.05", "letter_spacing": "-0.04em to -0.055em", "color": "#FFFFFF",
      "alignment": "Left", "max_width": "75-85% of canvas",
      "characteristics": ["Large setting", "Compact leading", "Strong visual dominance",
        "Breaks at meaningful groups", "No bold weight without need"]},
    "secondary_headline": {"font_weight": "400", "font_size": "42-64 px",
      "line_height": "1.0-1.12", "letter_spacing": "-0.035em", "color": "#FFFFFF"},
    "body_text": {"font_weight": "400", "font_size": "20-28 px", "line_height": "1.25-1.4",
      "color": "#D8DCE5"},
    "micro_text": {"font_weight": "400-500", "font_size": "12-18 px", "line_height": "1.2",
      "color": "#9298A6",
      "usage": ["Navigation", "Chart captions", "Technical labels", "Interface marks", "Section numbers"]},
    "typographic_effects": {"split_headlines": true, "mixed_opacity": true,
      "oversized_type": true, "all_caps": "Only for small labels",
      "outlined_type": false, "gradient_type": false},
    "headline_layout": "Headlines may split into a white dominant part and a gray second line with asymmetric offset"
  },
  "composition": {
    "layout_style": "Asymmetric Minimalist Editorial",
    "key_principles": ["One main visual dominant per slide", "Large negative space zones",
      "Combination of large text and small technical details", "Alignment to an invisible grid",
      "Alternating horizontal and vertical visual rhythms",
      "Contrast of large empty spaces and dense information modules"],
    "headline_positioning": ["Left in the lower half", "Left in the top third",
      "Centered with asymmetric wrap"],
    "visual_positioning": ["Right of the text", "Center as the main object",
      "Full-bleed with partial text overlap"],
    "layering": {"enabled": true,
      "levels": ["Dark base background", "Gradient glow", "Geometric texture",
        "3D object or diagram", "Main text", "Micro-navigation and interface details"]},
    "negative_space": "35-60% of the slide"
  },
  "geometry_and_forms": {
    "dominant_shapes": ["Narrow vertical ribs", "Repeating bands", "Soft semicircular arcs",
      "Concentric circles", "Rectangular panels", "Thin corner frames",
      "Horizontal light lines", "Narrow interface capsules"],
    "vertical_ribbed_texture": {"importance": "Very high for the cover",
      "description": "Frequent narrow vertical volumetric ribs creating architectural louvre or extruded metal plate impressions",
      "orientation": "Vertical", "spacing": "Regular, approximately 8-18 px at 1920px",
      "depth": "Medium to high", "lighting": "Blue directional illumination",
      "material": "Glossy dark metallic / digitally rendered",
      "distortion": "Wave-like diagonal deformation",
      "gradient": ["#061224", "#0654C9", "#073A91", "#A8D8FF"]},
    "corner_brackets": {"enabled": true, "shape": "Four detached L-shaped corners",
      "stroke_width": "3-5 px", "color": "#F2F5FF", "usage": "Framing central 3D objects"},
    "circles_and_arcs": {"style": "Concentric thick arcs", "color": "#0866F5",
      "line_weight": "Medium to thick", "usage": "Diagrams and infographics"},
    "rounded_corners": {"cards": "4-10 px", "pills": "Fully rounded", "large_panels": "0-6 px"}
  },
  "gradients": {
    "primary_blue_glow": {"type": "Radial", "colors": ["#0866F5", "#043B8C", "#090C14"],
      "opacity": "60-100%", "blur": "Large", "usage": "Illumination of objects and background elements"},
    "deep_blue_vertical": {"type": "Linear", "direction": "Bottom to top",
      "colors": ["#0866F5", "#05377E", "#090C14"], "usage": "Active roadmap columns and highlighted panels"},
    "metallic_blue": {"type": "Multi-stop", "colors": ["#050A16", "#0A3B83", "#0976FF", "#061A3D", "#B4E0FF"],
      "usage": "Volumetric ribbed constructions"},
    "gradient_rules": ["Gradients must create depth", "Avoid pastel and warm transitions",
      "Use local blue light sources", "Keep the brightest areas small"]
  },
  "lighting_and_effects": {
    "glow": {"enabled": true, "color": "#0866F5", "intensity": "Medium",
      "blur_radius": "30-100 px", "usage": ["3D objects", "Active panels", "Dividing lines", "Selected chart elements"]},
    "shadows": {"style": "Soft deep shadows", "color": "#000000", "opacity": "35-65%", "blur": "20-60 px"},
    "glassmorphism": {"usage": "Minimal", "transparency": "Low", "border": "Subtle cool gray",
      "background_blur": "Optional"},
    "noise": {"enabled": true, "strength": "Very subtle, 1-3%",
      "purpose": "Remove excessive digital sterility"},
    "reflections": {"enabled": true, "style": "Cold blue specular highlights"}
  },
  "three_dimensional_objects": {
    "style": "Photorealistic CGI / High-end product visualization",
    "materials": ["Polished dark metal", "Glossy glass", "Black anodized aluminum",
      "Blue glowing glass", "Translucent digital particles"],
    "lighting": {"key_light": "Cold blue", "rim_light": "Bright electric blue",
      "ambient_light": "Very dark navy", "background": "#090C14"},
    "camera": {"perspective": "Dynamic three-quarter angle", "lens": "50-85mm equivalent",
      "composition": "Central or slightly offset", "object_scale": "Large"},
    "effects": ["Partial disintegration", "Digital particles", "Fragmentation",
      "Glossy highlights", "Local blue glow", "Physical-to-digital transition"],
    "object_selection": ["Smartphones", "Abstract technological devices",
      "Volumetric digital forms", "Geometric objects", "Technological sculptures"]
  },
  "cards_and_ui": {
    "style": "Dark futuristic dashboard",
    "card_background": "#101521", "card_border": "#222A39", "border_width": "1 px",
    "corner_radius": "4-8 px", "padding": "24-36 px", "spacing": "12-24 px",
    "card_types": [
      {"type": "Metric card", "description": "Large number, small caption, minimal chart"},
      {"type": "Blue highlight card", "description": "Bright blue fill, white text, high visual weight"},
      {"type": "Dark information card", "description": "Dark panel, thin border, small captions"},
      {"type": "Image card", "description": "Large visual with dark background and cold grading"}
    ],
    "navigation_elements": {"pills": true, "micro_labels": true, "thin_separators": true,
      "small_circular_indicators": true, "arrow_buttons": true},
    "buttons": {"shape": "Capsule", "background": "#0D1422", "border": "#2C3548",
      "text_color": "#FFFFFF", "active_color": "#0866F5"}
  },
  "charts_and_infographics": {
    "visual_style": "Minimal dark analytics dashboard",
    "chart_background": "#101521", "axis_color": "#303847", "grid_opacity": "10-20%",
    "primary_data_color": "#0866F5", "secondary_data_color": "#9ECFFF",
    "inactive_data_color": "#3C4658",
    "chart_types": ["Line charts", "Concentric radial diagrams", "Percentage arcs",
      "Dot grids", "Miniature sparklines", "Bar charts", "Roadmap timeline"],
    "line_charts": {"stroke_width": "2-4 px", "line_style": "Smooth", "markers": "Minimal",
      "grid": "Subtle or absent"},
    "radial_charts": {"stroke_width": "12-24 px", "background_track": "#1D2636",
      "active_track": "#0866F5", "labels": "Outside or beneath chart"},
    "data_labels": {"font_size": "14-22 px", "color": "#FFFFFF", "secondary_color": "#9298A6"},
    "rules": ["Avoid standard office charts", "No 3D charts for numeric data",
      "Keep charts thin and minimalist", "Highlight one main metric",
      "Blue for active values, gray for secondary"]
  },
  "roadmap_slides": {
    "layout": "Horizontal timeline with vertical columns", "background": "#090C14",
    "column_dividers": {"color": "#1D2636", "width": "1 px"},
    "month_labels": {"position": "Top", "font_size": "16-20 px", "color": "#9298A6"},
    "milestone_cards": {"background": "#1B2231", "active_background": "#0866F5",
      "text_color": "#D8DCE5", "corner_radius": "2-5 px"},
    "active_period": {"vertical_gradient": true, "blue_glow": true, "highlight_strength": "High"},
    "bottom_labels": {"font_size": "16-20 px", "color": "#9298A6"},
    "composition": "Six or more uniform vertical sections, one highlighted bright blue"
  },
  "slide_archetypes": [
    {"name": "Hero Cover", "description": "Cover with large typography and volumetric ribbed blue-black background",
     "headline_position": "Bottom left", "visual": "Full-bleed abstract ribbed 3D surface",
     "details": ["Logo top left", "Small descriptor top right", "Large 2-4 line headline",
       "Small CTA bottom right"]},
    {"name": "Product Showcase", "description": "Central product presentation as a 3D object",
     "headline_position": "Top left and center", "visual": "Large floating 3D product",
     "details": ["Corner brackets around the object", "Interface component labels",
       "Blue horizontal line", "Dark background", "Digital fragmentation"]},
    {"name": "Analytics Dashboard", "description": "Dense information slide with cards, metrics and charts",
     "headline_position": "Top left", "visual": "Modular collection of dark cards",
     "details": ["One bright blue card", "Several dark analytics panels",
       "Large numeric metrics", "Charts with blue and white lines"]},
    {"name": "Feature Overview", "description": "Overview of product benefits or directions",
     "headline_position": "Top left", "visual": "Structured list with icons and radial diagram",
     "details": ["List blocks left", "Circular diagrams right", "White and gray captions",
       "Small technical typography"]},
    {"name": "Roadmap", "description": "Horizontal calendar plan",
     "headline_position": "Top left", "visual": "Six-column timeline",
     "details": ["Months on top", "Vertical task cards", "One active month highlighted",
       "Large free gap between title and chart"]}
  ],
  "micro_details": {
    "logo": {"position": "Top left", "style": "White monochrome", "scale": "Small"},
    "section_labels": {"style": "Small dark capsule", "indicator": "Electric blue dot",
      "font_size": "12-16 px"},
    "technical_lines": {"color": "#0866F5", "width": "1-3 px"},
    "footer": {"style": "Minimal", "color": "#626B7C", "font_size": "12-16 px"},
    "decorative_elements": ["Micro text", "Small circular indicators", "Guide lines",
      "Technical frames", "Digital textures", "Small interface captions"]
  },
  "animation": {
    "style": "Smooth cinematic technology",
    "transitions": ["Fade", "Slow zoom", "Mask reveal", "Directional wipe", "Subtle parallax"],
    "duration": "0.4-1.0 sec", "easing": "Ease in-out",
    "recommended_effects": ["Sequential text appearance", "Smooth blue glow reveal",
      "Slow background geometry motion", "Slight 3D object rotation", "Line and chart animation"],
    "avoid": ["Sharp rotations", "Springy effects", "Random transitions",
      "Excessive interface motion"]
  },
  "design_constraints": {
    "must_have": ["Near-black background", "Electric blue accent",
      "Large white grotesque typography", "Asymmetric compositions",
      "Clear visual hierarchy", "Thin interface details", "Depth and local glow",
      "Premium technological aesthetics"],
    "avoid": ["Office PowerPoint templates", "Colored gradients with purple and pink",
      "Overly rounded cards", "Decorative and handwritten fonts", "Random illustrations",
      "Stock photos of people", "Many multicolored icons", "Thick frames",
      "Saturated shadows on all elements", "Too much text"]
  },
  "generation_prompt": "Create a premium futuristic technological presentation in the Midnight Electric Blue aesthetic. Use a near-black #090C14 background, electric blue #0866F5, large white grotesque typography in Inter or Helvetica Neue, minimalist Swiss editorial layout, asymmetric composition and generous negative space. For the cover use a volumetric texture of vertical blue metallic ribs with wave geometry, deep shadows and cold light highlights. For product slides use photorealistic 3D objects with blue glow and thin technical frames. For analytics slides build dark modular dashboard cards, minimalist line and radial charts. For roadmaps use a horizontal grid with vertical columns and one bright-blue active section. Keep strict typographic hierarchy, clean alignment and the feel of an expensive digital product. Avoid template corporate design, extra colors and decorative elements.",
  "reference_fidelity": {
    "target": "High",
    "priority_order": ["Overall feel and composition", "Typographic system",
      "Color contrast", "Ribbed 3D textures", "Blue glow", "Cards and infographics",
      "Interface micro-details"],
    "note": "HEX codes, sizes, glow and grid parameters are visually sampled approximations, not extracted from a source Figma file."
  }
}
```

---

## Style 2: NovaPay — Liquid Electric Blue

```json
{
  "style_name": "NovaPay — Liquid Electric Blue",
  "style_category": "Premium Fintech / Liquid Glass / Futuristic Web Design",
  "design_philosophy": {
    "core_idea": "A premium tech presentation whose main visual expressiveness comes from dynamic blue 3D backgrounds, volumetric glossy ribbons, soft gradients and translucent interface underlays.",
    "mood": ["premium", "futuristic", "fluid", "immersive", "energetic", "minimal", "high-tech"],
    "visual_priority": ["Complex abstract background compositions", "Blue light flows",
      "Contrast of large white text", "Translucent glass cards",
      "Asymmetric modular composition", "Large numeric metrics"],
    "key_distinction": "The background must feel like an expensive CGI render with smooth glowing curves, not a flat gradient."
  },
  "canvas": {
    "aspect_ratio": "16:9", "resolution": {"width": 1920, "height": 1080},
    "outer_background": "#080B19", "slide_corner_radius": "20-26 px", "safe_padding": "4-6%",
    "composition": "Full-bleed background with content overlays"
  },
  "color_palette": {
    "deep_black_blue": "#03091B", "midnight_navy": "#061232", "dark_royal_blue": "#071D60",
    "royal_blue": "#1738D9", "electric_blue": "#075BFF", "ultra_blue": "#2440FF",
    "luminous_blue": "#287BFF", "sky_blue": "#5BA7FF", "ice_blue": "#B5D7FF",
    "white": "#F8FAFF", "muted_text": "#A5B7D9", "cyan_text": "#56B8EE",
    "glass_border": "#8AB4FF", "glass_fill": "#1A315A",
    "dominant_color_ratio": {"dark_blue": "45%", "medium_blue": "25%", "bright_blue": "15%",
      "translucent_surfaces": "10%", "white_and_light_details": "5%"}
  },
  "background_system": {
    "importance": "Critical",
    "concept": "Deep dark-blue space crossed by volumetric light ribbons and smooth curved surfaces; light moving over liquid metal or glass.",
    "visual_characteristics": ["Continuous smooth lines", "Wide diagonal bends", "Layered depth",
      "Contrast of sharp light highlights and soft shadows", "Glossy reflections",
      "Smooth thickness change of light ribbons", "Alternation of dark and saturated blue areas",
      "Local near-white blue highlights"],
    "base_layer": {"type": "Full-frame gradient", "gradient": "Complex radial and linear blend",
      "colors": ["#03091B", "#061232", "#08266E", "#0A35A2"], "direction": "Diagonal and radial",
      "description": "Very dark blue base with smooth local lightening; never uniform or flat."},
    "secondary_depth_layer": {"type": "Soft atmospheric lighting",
      "colors": ["#0A2D92", "#075BFF", "#061232"], "opacity": "35-65%", "blur_radius": "100-280 px",
      "description": "Large blurred blue light spots creating depth behind the main ribbons."},
    "primary_liquid_ribbons": {"type": "3D curved glossy ribbons",
      "material": "Polished translucent blue glass with metallic reflections",
      "shape": "Wide bending surfaces with smooth wave-like transitions", "curvature": "High",
      "orientation": ["Diagonal", "Curved", "Sweeping", "Wave-like"],
      "colors": ["#02102D", "#0743BC", "#0873FF", "#5DA9FF", "#C1E1FF"],
      "surface_properties": {"glossiness": "Very high", "roughness": "Very low",
        "reflectivity": "High", "transparency": "Low to medium",
        "specular_highlights": "Strong", "metallic_feel": "Medium"},
      "lighting": {"key_light": "Intense cold blue", "rim_light": "Pale icy blue",
        "shadow": "Deep navy", "reflection": "Long smooth light streaks"},
      "depth": {"foreground_ribbons": "Sharp and bright", "middle_ribbons": "Moderately contrasted",
        "background_ribbons": "Dark and slightly blurred"},
      "description": "Ribbons resemble woven glossy surfaces or flowing metallic highways; they must look three-dimensional with thickness, shadows and reflections."},
    "light_streaks": {"type": "Curved luminous trails", "color": "#4DA0FF",
      "highlight_color": "#C1E1FF", "thickness": "Variable", "brightness": "High",
      "glow": "Soft blue",
      "behavior": "Light lines run along the curvature of volumetric surfaces, emphasizing perspective and speed.",
      "avoid": ["Random straight neon lines", "Uniform glow over the whole surface", "Cheap laser effect"]},
    "gradient_blending": {"type": "Multi-layer smooth blending",
      "preferred_transitions": ["Black navy to royal blue", "Electric blue to ice blue",
        "Deep blue to transparent", "Bright blue to dark navy"],
      "rules": ["No sharp color borders outside light highlights", "Keep deep dark zones",
        "Avoid a uniformly bright background", "Keep complex light-flow shapes"]},
    "negative_space": {"principle": "Light structures must bypass main text blocks.",
      "text_area": "Dark, low-detail background", "decorative_area": "Bright, dynamic, high-detail",
      "priority": "Readability over decorative complexity"}
  },
  "background_variants": {
    "hero_background": {"reference": "Slide 1", "composition": "Dynamic diagonal crossing ribbons",
      "description": "Dark navy background with large glossy blue ribbons crossing the slide diagonally. One main light arc starts bottom-left and rises to the upper right. Additional waves form depth at the top and right.",
      "left_side": {"brightness": "Dark to medium", "purpose": "Free space for the headline",
        "details": "Local soft blue glows without active texture directly behind the letters"},
      "center": {"brightness": "Medium to high", "elements": "Intersection of volumetric light ribbons"},
      "right_side": {"brightness": "Mixed", "purpose": "Background for statistical glass cards"},
      "dominant_direction": "Bottom-left to upper-right", "contrast": "High"},
    "feature_background": {"reference": "Slide 2", "composition": "Split layout with liquid wave image",
      "description": "Composition split into a colored text panel on the left and a complex wave 3D background top-right. On the right, light surfaces curve and fan out.",
      "left_panel": {"type": "Solid gradient", "colors": ["#15156A", "#2435F3"],
        "direction": "Top to bottom", "appearance": "Deep indigo on top, saturated ultramarine below"},
      "top_right": {"type": "Full-bleed 3D ribbon artwork",
        "colors": ["#020C27", "#0648D3", "#4292FF", "#C4E3FF"], "direction": "Curved fan-like motion",
        "description": "Large smooth blue waves widening toward the right edge, creating a sense of speed."},
      "bottom_center": {"type": "Dark blue gradient card", "colors": ["#0B0C37", "#252DE3"]},
      "bottom_right": {"type": "Vertical blue gradient card", "colors": ["#050B29", "#1946BA", "#A7CBFF"]}},
    "metrics_background": {"reference": "Slide 3", "composition": "Wide horizontal blue light flows",
      "description": "Deep dark-blue background with powerful horizontal-diagonal light waves. Bright blue surfaces concentrate top-right and bottom-left; the central zone hosts metric cards.",
      "top_left": {"brightness": "Very dark", "purpose": "Readability of the large headline"},
      "top_right": {"brightness": "Bright", "elements": "Broad blue flowing reflections"},
      "middle": {"brightness": "Medium", "elements": "Soft horizontal blue glow"},
      "bottom": {"brightness": "Mixed", "elements": "Flowing blue ribbons and soft diffusion"},
      "direction": "Horizontal with diagonal curvature"}
  },
  "overlay_system": {
    "concept": "Dark and translucent underlays over the bright CGI background keep text readable and create the feel of a digital financial product interface.",
    "layer_order": ["Dark navy base background", "Atmospheric blue radial glows",
      "Glossy liquid 3D ribbons", "Optional dark contrast gradient",
      "Translucent glass cards", "Text, buttons and icons"],
    "contrast_overlay": {"type": "Linear gradient",
      "colors": ["rgba(2,8,25,0.70)", "rgba(2,8,25,0.25)", "rgba(2,8,25,0.00)"],
      "usage": "Over the complex background in large-text zones"}
  },
  "glass_card_system": {
    "style": "Dark blue translucent glassmorphism",
    "description": "Translucent smoked blue glass cards; the blue background partially shows through. Soft light border, local reflections, slight blur.",
    "geometry": {"shape": "Rounded rectangle", "corner_radius": "18-24 px",
      "border_width": "1-2 px", "padding": "26-36 px"},
    "surface": {"base_color": "#20365B", "opacity": "55-75%", "background_blur": "12-30 px",
      "saturation": "120-160%", "material": "Smoked blue glass"},
    "border": {"type": "Subtle luminous border", "color": "rgba(190,218,255,0.40)",
      "opacity": "35-65%", "highlight": "Brighter upper-left edge"},
    "surface_gradient": {"type": "Linear diagonal",
      "colors": ["rgba(120,165,230,0.24)", "rgba(30,65,125,0.20)", "rgba(9,19,53,0.45)"],
      "direction": "Top-left to bottom-right"},
    "shadow": {"color": "rgba(0,0,20,0.40)", "blur": "20-45 px", "y_offset": "8-18 px"},
    "inner_highlight": {"enabled": true, "color": "rgba(220,238,255,0.18)",
      "placement": "Top edge", "thickness": "1 px"},
    "visual_rule": "Underlays must not be fully opaque; keep the sense of depth and interaction with the background."
  },
  "card_variants": {
    "hero_stat_cards": {"layout": "Vertical stack on right", "count": 3,
      "material": "Translucent dark blue glass", "opacity": "60-75%",
      "border": "Thin pale blue", "large_number": "White, lightweight",
      "description_text": "Small light gray", "decorative_icon": "Small luminous turquoise 3D glass object",
      "visual_balance": "Large number left, small volumetric decorative form right"},
    "feature_color_panels": {"material": "Opaque and semi-opaque gradient surfaces",
      "corner_radius": "0-4 px inside modular layout",
      "description": "Large modular colored underlays with deep blue gradients; unlike glass cards they almost fully hide the background and form a strict compositional grid."},
    "metric_cards": {"layout": "Four equal-width cards", "material": "Dark frosted glass",
      "background": "rgba(35,49,75,0.65)", "backdrop_blur": "20 px",
      "border": "rgba(210,225,255,0.24)", "corner_radius": "18 px",
      "number_position": "Top left", "description_position": "Bottom left",
      "vertical_distribution": "Space between",
      "special_card": {"position": 3, "background": "#2438F5", "opacity": "100%",
        "border": "#C6D6FF", "glow": "Soft electric blue",
        "description": "One card is highlighted with a bright solid blue fill to focus attention."}}
  },
  "typography": {
    "style": "Modern neutral sans-serif",
    "recommended_fonts": ["Helvetica Neue", "Inter", "Suisse Intl", "Arial", "Manrope"],
    "headline": {"weight": "300-400", "size": "80-112 px at 1920px", "line_height": "0.98-1.08",
      "letter_spacing": "-0.035em", "color": "#FFFFFF", "appearance": "Very large, light, clean"},
    "subheadline": {"weight": "400", "size": "24-32 px", "color": "#A8BCE2",
      "letter_spacing": "0 to 0.015em"},
    "metric_number": {"weight": "300-400", "size": "68-94 px", "color": "#FFFFFF"},
    "body": {"weight": "400", "size": "22-28 px", "color": "#E2E9FA"},
    "secondary_text": {"weight": "400", "size": "17-22 px", "color": "#A5B7D9"},
    "typography_rules": ["No heavy bold in large headlines", "Keep generous air around text",
      "No text shadows", "Break large headlines into short lines",
      "Maintain maximum contrast with the background"]
  },
  "layout_system": {
    "style": "Premium editorial web presentation",
    "principles": ["Large headlines left", "Content cards right or bottom",
      "Large colored rectangular sections", "Two-part compositions",
      "Minimal decorative UI elements", "Background graphics unify the blocks"],
    "hero_slide": {"left_content_width": "55-60%", "right_cards_width": "26-30%",
      "top_navigation_height": "8%", "headline_alignment": "Left center",
      "stat_cards": "Right vertical stack"},
    "feature_slide": {"columns": 2, "left_width": "45%", "right_width": "55%",
      "right_top_visual_height": "58%", "right_bottom_cards_height": "42%",
      "description": "Asymmetric grid of a large text panel and three adjacent media blocks."},
    "metrics_slide": {"headline_area": "Top 35%", "cards_area": "Middle 40%",
      "cta_area": "Bottom 15%", "card_count": 4, "horizontal_gutter": "16-24 px"}
  },
  "buttons_and_navigation": {
    "navigation": {"shape": "Large horizontal capsule", "background": "rgba(15,28,62,0.75)",
      "corner_radius": "999 px", "height": "72-85 px", "blur": "12 px",
      "logo": "Simple white text", "links": "Small muted white",
      "cta": {"background": "#FFFFFF", "text_color": "#0C1530", "shape": "Pill"}},
    "secondary_cta": {"style": "Outlined transparent pill", "border": "rgba(220,235,255,0.65)",
      "background": "Transparent", "text_color": "#FFFFFF", "arrow": "Small outlined circular icon"}
  },
  "three_dimensional_decor": {"usage": "Small, selective",
    "objects": ["Translucent cyan glass crystals", "Iridescent abstract blobs",
      "Small glowing irregular polyhedrons"],
    "materials": {"transparency": "Medium", "glossiness": "High",
      "color": "Cyan and electric blue", "rim_light": "Bright turquoise", "glow": "Soft"},
    "positioning": "Upper-right corner of statistic cards",
    "purpose": "Add a premium CGI accent without overload"},
  "figma_recreation": {
    "background_approach": {"preferred": "Use high-quality CGI backgrounds as full-size images; build text and cards as separate editable layers.",
      "alternative": "Partially recreate light flows with vector curves, multi-layer gradients, blur and blend modes.",
      "note": "For accurate volumetric ribbons use Blender, Cinema 4D or AI image generation."},
    "layer_stack": ["01_Base dark gradient", "02_Atmospheric blue glow",
      "03_Liquid ribbon background image", "04_Contrast overlay", "05_Glass panels",
      "06_Borders and inner highlights", "07_Typography", "08_Icons and buttons"],
    "glass_effect_recipe": {"fill": "rgba(35,60,105,0.65)", "background_blur": "20 px",
      "stroke": "1 px rgba(190,220,255,0.35)", "inner_shadow": "0 1px 0 rgba(255,255,255,0.15)",
      "drop_shadow": "0 12px 32px rgba(0,0,20,0.35)", "corner_radius": "18 px"},
    "highlight_card_recipe": {"fill": "#2438F5", "stroke": "1.5 px #C6D6FF",
      "shadow": "0 0 40px rgba(40,90,255,0.45)", "corner_radius": "18 px"}
  },
  "critical_visual_rules": [
    "The background must always be layered and volumetric.",
    "Main background shapes are wide smooth glossy ribbons, not thin lines.",
    "Every ribbon has its own light and shadow structure.",
    "Almost-black zones must exist on the background for contrast.",
    "Blue light runs along the curves and emphasizes the form.",
    "Never use a plain radial gradient as the only background.",
    "Never make the whole slide uniformly bright blue.",
    "Glass cards must keep translucency and a soft light border.",
    "For large colored panels use denser opaque gradient underlays.",
    "Keep text readable via dark local zones.",
    "Background composition may differ per slide, but material, color and light must stay the same.",
    "Do not mix this style with purple, pink, orange or green gradients."
  ],
  "negative_prompt": ["flat blue gradient", "generic corporate presentation",
    "purple neon cyberpunk", "pink or magenta lighting", "simple geometric waves",
    "cartoon illustrations", "flat vector background", "excessive glow",
    "plastic-looking ribbons", "low-detail 3D rendering", "random luminous lines",
    "generic stock imagery", "overly rounded UI", "heavy bold typography", "busy text background"],
  "master_generation_prompt": "Create a premium futuristic fintech presentation in the visual style of NovaPay Liquid Electric Blue. Use a deep midnight-navy background with complex high-end CGI blue liquid ribbons flowing diagonally and horizontally across the canvas. The ribbons should resemble polished blue glass and metallic fluid surfaces, with smooth curvature, strong specular highlights, icy-blue reflections, deep black shadows and electric-blue illumination. Build a highly dimensional background with multiple layers of atmospheric glow, overlapping curved ribbons and carefully preserved dark negative space for text. Use large lightweight white Helvetica-style typography and asymmetric editorial layouts. Overlay translucent smoked-blue glass cards with subtle pale-blue borders, backdrop blur, soft reflections and deep shadows. Combine these glass surfaces with occasional solid electric-blue highlight cards and large blue gradient panels. Maintain an immersive, sophisticated, expensive technology aesthetic. Avoid flat gradients, generic waves, purple neon, excessive glow and conventional corporate templates.",
  "fidelity_notes": {"color_accuracy": "Approximate visual sampling",
    "background_priority": "Highest", "surface_priority": "Highest",
    "typography_priority": "High", "geometry_priority": "High",
    "important": "All colors and numeric parameters are recommendations based on visual analysis of the image, not exact properties of a source design file."}
}
```

---

## Style 3: Clean Blue Tech (light corporate)

Light styles **skip the texture engine**: backgrounds stay flat/light, decor is
vector overlays (`slide-patterns.md`), and the luminance logic inverts — keep text
zones clean and light, use the accent sparsely (15%).

```json
{
  "style_id": "blue-tech-corporate",
  "name": "Clean Blue Tech",
  "category": "Corporate Technology Presentation",
  "description": "Premium minimalist technology presentation with white backgrounds, royal blue accents, photorealistic 3D product renders, isometric diagrams, clean typography and editorial layouts.",
  "canvas": {
    "aspect_ratio": "16:9", "orientation": "landscape", "background": "#F8FAFD",
    "safe_margin_percent": 5,
    "grid": {"columns": 12, "gutter": "medium", "alignment": "precise"}
  },
  "color_palette": {
    "primary_blue": "#2456A0", "deep_blue": "#173A70", "electric_blue": "#3474C8",
    "light_blue": "#DCE8F7", "ice_blue": "#EDF3FA", "white": "#FFFFFF",
    "off_white": "#F8FAFD", "text_primary": "#202733", "text_secondary": "#7B8797",
    "divider": "#DCE2E9",
    "usage": {"white_and_light_backgrounds": "75%", "blue_accents": "15%",
              "text_and_neutrals": "10%"}
  },
  "typography": {
    "family": "Arial, Aptos or Helvetica Neue", "style": "modern geometric sans-serif",
    "heading": {"size_pt": 28, "weight": "bold", "color": "#202733", "line_height": 1.1},
    "section_number": {"size_pt": 34, "weight": "bold", "color": "#2456A0"},
    "body": {"size_pt": 12, "weight": "regular", "color": "#7B8797", "line_height": 1.4},
    "caption": {"size_pt": 9, "color": "#7B8797"},
    "emphasis": "Bold headings, blue numbers and minimal decorative text"
  },
  "layout": {
    "design_philosophy": ["Minimalist corporate editorial design",
      "Strong asymmetric compositions", "Large negative space", "Precise modular grid",
      "Clear visual hierarchy", "Product-focused storytelling", "Clean technical diagrams"],
    "preferred_compositions": ["Left text with large right-side 3D object",
      "Split-screen photography and information", "Three-column feature descriptions",
      "Four-column product specifications", "Centered isometric technology ecosystem",
      "Large section number with headline", "Full royal-blue table of contents"],
    "whitespace": "high", "density": "low-to-medium", "alignment": "strict",
    "corners": "square or subtly rounded"
  },
  "visual_style": {
    "rendering": "premium photorealistic 3D",
    "objects": ["White technological devices", "Wireless sensors", "Smart hardware",
      "Spherical antenna systems", "Isometric computing modules", "Floating interface panels",
      "Minimal technical platforms"],
    "materials": ["Matte white plastic", "Glossy ceramic", "Brushed aluminum",
      "Transparent glass", "Translucent blue acrylic"],
    "lighting": {"type": "soft studio lighting", "temperature": "cool neutral",
      "shadows": "soft ambient shadows", "highlights": "subtle blue reflections",
      "contrast": "low-to-medium"},
    "camera": {"angles": ["isometric", "three-quarter product view", "front perspective"],
      "background": "white or pale blue gradient"}
  },
  "graphics": {
    "icons": {"style": "thin line or small blue 3D", "color": "#2456A0", "consistency": "uniform"},
    "diagrams": {"style": "minimal futuristic technical",
      "elements": ["Circular wireless network maps", "Radial connection diagrams",
        "Floating platform structures", "Thin connector lines", "Small blue data markers"]},
    "charts": {"style": "clean and flat", "gridlines": "minimal",
      "colors": ["#2456A0", "#70A3DD", "#B8D2EF"]},
    "decorations": {"thin_lines": true, "blue_labels": true, "small_square_markers": true,
      "subtle_gradients": true, "heavy_borders": false}
  },
  "slide_patterns": [
    {"type": "cover", "layout": "left title, right 3D visualization", "background": "white",
     "elements": ["Small blue square brand marker", "Large bold company or product title",
       "Short subtitle", "Hero isometric 3D render", "Subtle technical background lines"]},
    {"type": "table_of_contents", "background": "#2456A0",
     "layout": "vertical title and six-item grid",
     "elements": ["Oversized vertical white Contents title", "Numbered sections 01-06",
       "Small descriptions in white", "Generous spacing"]},
    {"type": "company_profile", "layout": "50/50 photo and text",
     "elements": ["Architectural photography", "Bold headline overlay", "Company description",
       "Small image strip", "Large numerical KPIs"]},
    {"type": "product_overview", "layout": "technical specifications grid",
     "elements": ["Product title", "Short introduction", "Small product renders",
       "Feature descriptions", "Thin horizontal dividers"]},
    {"type": "feature_ecosystem", "layout": "central isometric illustration",
     "elements": ["Large central 3D technology ecosystem", "Floating mini-devices",
       "Four feature descriptions", "Blue section marker"]},
    {"type": "hero_product", "layout": "left text and right product render",
     "elements": ["Large blue section number", "Bold product name", "Four feature icons",
       "Oversized isolated 3D product"]},
    {"type": "technical_hardware", "layout": "horizontal product render",
     "elements": ["Large product title", "Photorealistic device render",
       "Four technical benefit columns", "Small blue line icons"]},
    {"type": "network_visualization", "layout": "left text, right circular diagram",
     "elements": ["Large metric", "Short technical explanation", "Radial node network",
       "Blue status labels"]}
  ],
  "branding": {"top_left": "small solid blue square marker",
    "top_right": "small technical section label", "bottom_right": "tiny blue pagination square",
    "branding_intensity": "subtle"},
  "pptx_requirements": {"editable_text": true, "editable_shapes": true, "editable_charts": true,
    "high_resolution_images": true, "consistent_margins": true,
    "preserve_visual_hierarchy": true, "avoid_text_overflow": true,
    "minimum_body_text_pt": 12},
  "avoid": ["Bright multicolor palettes", "Heavy decorative elements", "Cartoon illustrations",
    "Oversaturated gradients", "Thick borders", "Excessive text", "Inconsistent typography",
    "Random icon styles", "Strong drop shadows", "Crowded compositions"],
  "generation_prompt": "Create a premium futuristic corporate technology PowerPoint presentation. Use clean white backgrounds, royal blue accents, sophisticated asymmetric layouts, large negative space, precise Swiss-inspired typography, realistic isometric 3D hardware renders, translucent blue technical elements, fine dividers, blue numbered sections, modular feature grids and subtle studio lighting. Maintain a highly polished engineering and enterprise technology aesthetic. Every slide must look like part of one coherent professional presentation."
}
```

---

## Style 4: Dark Emerald Strategy

Dark executive roadmap style; the liquid texture engine drives it with an emerald
palette (base `#050C0F → #0D2424 → #164F3D`, glows `#51E9A0` top-right, rims
`#B7F5D8`).

```json
{
  "style_id": "dark-emerald-strategy",
  "name": "Dark Emerald Strategy",
  "category": "Product Strategy / Executive Roadmap",
  "description": "Premium dark-mode presentation with emerald glow gradients, bold editorial typography, luminous metrics, translucent panels and minimalist strategic diagrams.",
  "canvas": {
    "aspect_ratio": "16:9", "background": "#050C0F", "safe_margin_percent": 5,
    "grid": {"columns": 12, "alignment": "strict"}
  },
  "color_palette": {
    "background": "#050C0F", "deep_teal": "#0D2424", "dark_emerald": "#164F3D",
    "emerald_primary": "#51E9A0", "mint_bright": "#63F5B0", "mint_soft": "#B7F5D8",
    "text_primary": "#F5FAF8", "text_secondary": "#B6C9C4", "surface_glass": "#1E4B42"
  },
  "background_treatment": {
    "base": "near-black to deep teal",
    "gradient": "soft multi-point emerald ambient glow",
    "glow_position": "primarily top-right, sometimes bottom-left",
    "texture": "subtle fine grain", "vignette": "gentle dark edges", "contrast": "high"
  },
  "typography": {
    "family": "Inter, Manrope, Aptos",
    "cover_title": {"size_pt": 44, "weight": "bold", "color": "#63F5B0"},
    "heading": {"size_pt": 27, "weight": "semibold", "color": "#F5FAF8"},
    "statement": {"size_pt": 35, "weight": "light", "color": "#F5FAF8"},
    "body": {"size_pt": 14, "color": "#B6C9C4"},
    "metric": {"size_pt": 30, "weight": "bold", "color": "#63F5B0"}
  },
  "layout": {
    "style": "cinematic editorial minimalism", "whitespace": "high",
    "density": "low-to-medium", "alignment": "precise",
    "cards": "translucent emerald panels", "corners": "slightly rounded",
    "borders": "minimal",
    "preferred_compositions": ["Oversized asymmetric headline", "Three-column KPI cards",
      "Three-step process diagrams", "Centered strategic statements",
      "Three-column comparison matrices", "2x2 benefit grids",
      "Horizontal quarterly roadmaps", "Minimal ownership timelines"]
  },
  "graphics": {
    "icons": "minimal mint outline icons", "charts": "dark high-contrast editable charts",
    "diagrams": "thin connectors and glowing nodes",
    "callouts": "mint highlight strips with dark text",
    "effects": ["diffused emerald glow", "subtle glass transparency", "fine-grain atmosphere",
      "soft gradient card fills", "minimal network patterns"]
  },
  "slide_patterns": ["cover", "agenda", "problem_statement", "market_signals", "current_state",
    "strategic_statement", "competitive_gap", "value_proposition", "business_outcomes",
    "roadmap", "ownership_timeline"],
  "pptx_requirements": {"editable_text": true, "editable_shapes": true, "editable_charts": true,
    "minimum_body_text_pt": 14, "consistent_margins": true, "avoid_text_overflow": true,
    "background_image_allowed_for_glow_only": true},
  "avoid": ["Bright multicolor palettes", "White-dominant backgrounds", "Heavy borders",
    "Dense paragraphs", "Unnecessary 3D illustrations", "Tiny text", "Low-contrast captions",
    "Flattened slide screenshots"]
}
```

---

## Authoring a new style JSON with AI

A style spec is small enough to be written by an AI agent from references. The recipe:

### 1. Collect inputs

- 1–3 reference screenshots of the target look (deck, website, brand page)
- Brand colors if they exist (HEX), or permission to derive from screenshots
- Mood words and the audience ("fintech investors", "dev conference")
- Constraints: language (check Cyrillic rendering of the font!), dark/light, 16:9

### 2. Prompt the AI (copy-paste template)

```text
You are a presentation art director. Analyze the attached reference images and
produce a style specification as a single JSON object following this exact schema:
{ canvas, color_palette, background_system, overlay_system, glass_card_system,
  card_variants, typography, layout_system, buttons_and_navigation,
  critical_visual_rules, negative_prompt, generation_prompt }

Rules:
- Every color as HEX. Include a dominant_color_ratio so the palette stays disciplined.
- Backgrounds must be layered: base gradient + atmospheric glows + volumetric forms.
  "background_system.importance": "Critical".
- typography: ONE font family (must render Cyrillic if the deck is Russian),
  weights capped at 400-500 for headlines, sizes in px at 1920x1080.
- glass_card_system with explicit opacity and border rgba values.
- critical_visual_rules and negative_prompt must include the failure modes you
  want banned (e.g. "flat gradient background", "thin neon lines instead of
  wide ribbons", "purple/pink drift").
- generation_prompt: one paragraph an image agent or designer could execute.

Then wait for my confirmation before I build a test slide.
```

Attach the references to the same message. If the AI invents a palette that drifts
(purple/pink, low contrast), re-run with the `negative_prompt` list extended.

### 3. Validate the spec before mass production

1. **Field checklist** — the JSON must define: base background colors, one accent
   family, text colors for title/body/secondary/muted on dark, glass fill + border
   (with opacity), accent-card fill + border, radius, font family, title/body/micro
   sizes, background engine choice and 2–3 background variant descriptions.
2. **Build ONE test slide** (a content slide with the densest layout) before the
   whole deck.
3. **Render and compare** against the reference images side by side. Check: is the
   text zone dark? Is the accent discipline kept (one family)? Do wraps fit?
4. **Refine the JSON**, not the slide: if contrast fails, raise the darken overlay in
   `overlay_system`; if it looks cheap, extend `negative_prompt` and re-tune the
   background config (usually: ribbons too thin, or a flat base gradient).

### 4. Convert px → pt when implementing

PPTX canvas is 13.333 × 7.5 in. At 1920 × 1080: **1 px = 0.5 pt**, radius 18 px =
0.125 in = adjustment `radius / min(w, h)` on a rounded rectangle. Letter-spacing in
em → the `spc` XML attribute takes 1/100 pt: `spc = int(-0.04 * size_pt * 100)`.

### 5. Minimal template

```json
{
  "style_name": "",
  "style_category": "",
  "canvas": {"aspect_ratio": "16:9", "resolution": {"width": 1920, "height": 1080},
             "outer_background": ""},
  "color_palette": {"deep_black_blue": "", "midnight_navy": "", "electric_blue": "",
                    "ice_blue": "", "white": "", "muted_text": "", "glass_border": "",
                    "glass_fill": "", "dominant_color_ratio": {}},
  "background_system": {"concept": "", "base_layer": {}, "primary_forms": {},
                        "negative_space": {}},
  "glass_card_system": {"geometry": {}, "surface": {}, "border": {}},
  "typography": {"recommended_fonts": [], "headline": {}, "body": {}, "secondary_text": {}},
  "critical_visual_rules": [],
  "negative_prompt": [],
  "generation_prompt": ""
}
```

Fill every empty string — an empty field is a decision the AI will make for you,
and it is exactly where style drift starts.
