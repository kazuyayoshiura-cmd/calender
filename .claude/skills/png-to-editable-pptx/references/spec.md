# Layout spec (input to `scripts/build_pptx.py`)

All coordinates and sizes are **source-image pixels** (origin top-left). The builder
scales them onto the slide, so you never convert to inches/EMU yourself.

```json
{
  "source_size": [1672, 941],        // required: width, height of the PNG
  "slide_width_in": 13.333,           // optional (default 13.333 = 16:9 widescreen)
  "font": "Meiryo",                   // East Asian font (default Meiryo)
  "font_latin": "Meiryo",             // Latin font (default = font)
  "background": "#FFFFFF",            // slide background (solid)
  "elements": [ ... ]                 // drawn in order: first = back, last = front
}
```

Multi-slide: replace `elements`/`background` with
`"slides": [{"background": "#FFF", "elements": [...], "notes": "speaker notes"}, ...]`.

Colors are `#RRGGBB`, or `#RRGGBBAA` for transparency.

## Common fields

| field | meaning |
|---|---|
| `box` | `[x, y, w, h]` bounding box |
| `name` | object name shown in PowerPoint's Selection Pane (use meaningful names: `layer3-label`) |

## Shapes

`type`: `rect`, `roundRect`, `ellipse`, `chevron`, `homePlate` (arrow-tipped box, first step of a
process band), `triangle`, `diamond`, `hexagon`, `parallelogram`, `can` (cylinder/DB),
`rightArrow`/`leftArrow`/`upArrow`/`downArrow`/`leftRightArrow`/`upDownArrow` (block arrows),
`cloud`, `snip1Rect`, `round2SameRect`, `flowProcess`, `flowDecision`, `noSmoking`.

```json
{"type": "roundRect", "box": [30, 205, 1410, 600], "radius_px": 10,
 "fill": "#FFFFFF", "line": {"color": "#1F4E8C", "width_px": 3, "dash": "solid"},
 "shadow": {"blur_px": 6, "dist_px": 2, "alpha": 0.2}}
```

- `shadow`: **omit by default** — the builder emits no shadow (theme effects are stripped from every
  object). Add it only when the source uses a shadow on purpose (see SKILL.md "Shadows").

- `fill`: `"#hex"`, `null` (no fill), or gradient `{"gradient": [["#DCE9F8", 0], ["#FFFFFF", 100]], "angle": 0}` (angle 0 = left→right, 90 = top→bottom).
- `line`: omit or `null` for no outline. `dash`: `solid | dash | dot | sysDash | lgDash | dashDot`.
- `radius_px` (roundRect): measured corner radius in pixels. Measure it — do not guess big.
- `point_px` (chevron/homePlate): horizontal depth of the arrow tip in pixels.
- `adj`: raw PowerPoint adjustment values for other shapes. `rotation` (degrees), `flip_h`.
- Text inside a shape: add `text` (or `paras`) plus any text fields below; default alignment is centered.

## Text

```json
{"type": "text", "box": [40, 45, 380, 55], "text": "図2-1 全体構成図",
 "size_px": 44, "bold": true, "color": "#0B1F3A", "align": "l", "valign": "m"}
```

| field | default | meaning |
|---|---|---|
| `text` | | plain text; `\n` = new paragraph |
| `paras` | | rich text: `[[{"text": "検索API ", "bold": true}, {"text": "(Docker)", "size_px": 20}], [...]]` — one inner list per paragraph |
| `size_px` | 16 | font em-size in source pixels (see sizing below) |
| `bold`, `italic`, `color` | false, false, `#000000` | |
| `align` | `l` | `l c r j` |
| `valign` | `m` | `t m b` |
| `wrap` | false | true = wrap inside box width; false = one line per paragraph (safer for labels) |
| `inset_px` | 0 | inner padding, number or `[l, t, r, b]` |
| `line_spacing` | | multiplier, e.g. 1.0 |
| `vertical` | false | vertical (tategaki) text |
| `font`, `font_latin` | spec font | per-element override |

**Font size:** `size_px` is the em-size. For Japanese, the visible height of a full-width
glyph (e.g. 図, 検) is ≈ 0.88 × em, so `size_px ≈ measured_glyph_height × 1.13`. For Latin text
use cap height (H, D) ≈ 0.72 × em → `size_px ≈ cap_height × 1.4`. Text boxes have zero inset by
default, so make the box the text's line box (glyph box plus ~15% top/bottom).

## Lines and arrows

```json
{"type": "arrow", "points": [[715, 322], [715, 352]], "color": "#1F6FD1", "width_px": 4}
{"type": "arrow", "points": [[640, 715], [640, 703], [1265, 703], [1265, 720]], "color": "#1F6FD1", "width_px": 3, "head": "both"}
{"type": "line", "points": [[x1, y1], [x2, y2]], "color": "#999999", "width_px": 1, "dash": "dash"}
```

- `type: arrow` defaults `head: "end"`; `type: line` defaults `head: "none"`. `head`: `none | start | end | both`. `head_size`: `sm | med | lg`.
- 2 points → native connector; 3+ points → one open polyline (keeps a bent arrow a single editable object).
- `elbow: "h" | "v"` with 2 points auto-inserts one bend (horizontal-first / vertical-first).
- Fat block arrows (filled, with thickness) are shapes (`rightArrow` etc.), not lines.

## Icons

```json
{"type": "icon", "icon": "lucide:server", "box": [68, 216, 44, 44], "color": "#1F4E8C", "stroke_width": 2}
{"type": "icon", "icon": "azure:azure-database-postgresql-server", "box": [340, 725, 50, 50]}
{"type": "icon", "icon": "material:person-fill", "box": [36, 128, 42, 44], "color": "#2A4A7A"}
{"type": "icon", "icon": "simple:docker", "box": [318, 370, 44, 30], "color": "#2496ED"}
```

- `lucide:*` recolors via `color` (stroke) and `stroke_width` (in 24-unit icon space; 2 = default, 1.5 = thinner).
- `material:*` (Google Material Symbols, rounded) recolors via `color`; names end in `-fill` for the solid variant.
- `simple:*` uses `color`, else the brand color.
- `azure:*` keeps Microsoft's colors (recoloring/altering Azure icons is not permitted by their terms).
- The icon is inserted as SVG (PNG fallback embedded) → in PowerPoint it can be recolored, and
  lucide/simple icons can be turned into shapes via right-click → Convert to Shape.
- Icon on a colored disc/tile: put a native `ellipse`/`roundRect` behind it, then group them.

## Tables

```json
{"type": "table", "box": [400, 450, 600, 150],
 "col_widths_px": [200, 400], "row_heights_px": [50, 50, 50],
 "cells": [["項目", "値"], ["A", {"text": "1", "align": "r"}], [{"text": "合計", "span": [1, 2]}, null]],
 "header_fill": "#1F4E8C", "header_color": "#FFFFFF", "fill": null,
 "size_px": 18, "align": "c", "border": {"color": "#999999", "width_px": 1}, "cell_pad_px": 4}
```

A cell is a string or an object with any text field plus `fill` and `span: [rows, cols]`. Cells
covered by a span are `null`.

## Images (non-icon raster content)

```json
{"type": "image", "path": "crops/photo1.png", "box": [x, y, w, h]}
```

Use only for photos, screenshots, or illustrations that no icon library can represent. Crop
them from the source with `inspect_image.py crop ... --scale 1 --step 100000` (or PIL) and
reference the crop — relative paths resolve against the spec file's folder.

## Groups

```json
{"type": "group", "name": "layer-1", "children": [ {...}, {...} ]}
```

Children use the same element types. Group things a user would move together (number badge +
label, icon + disc, a whole layer row).
