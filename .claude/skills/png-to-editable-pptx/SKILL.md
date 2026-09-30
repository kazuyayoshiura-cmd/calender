---
name: png-to-editable-pptx
description: Rebuild a slide image (PNG/JPG screenshot, AI-generated slide draft, exported slide picture, architecture diagram image) as a fully editable PowerPoint .pptx - native text boxes, shapes, arrows, tables, and real vector icons (Azure Architecture Icons, Lucide, Simple Icons brand logos) instead of a flat picture. Use this whenever the user wants to turn a slide image / 画像のスライド / スライドの叩き / 構成図の画像 into PowerPoint or Google Slides, make an image-based slide editable, "pptxにして", "パワポで編集できるようにして", or recreate a diagram from a screenshot - even if they don't say "editable". Not for writing a new deck from scratch with no source image.
---

# PNG → Editable PPTX

Goal: a .pptx that looks like the source image, where every text is a text box, every box/band/line
is a native shape, and every icon is an SVG icon the user can recolor or swap. No flattened
screenshot of the slide, no text baked into pictures — that defeats the purpose.

You (Claude) do the vision work: read the image, measure positions, pick icons. The bundled
scripts do the deterministic work: measuring aids, icon lookup, building, previewing.

Scripts live in `scripts/` next to this file (`SKILL_DIR` below). Setup once per environment:

```bash
pip install python-pptx cairosvg pillow pymupdf lxml   # skip what is already installed
# preview needs LibreOffice Impress: `soffice` + libreoffice-impress
```

## Workflow

### 1. Measure the source

```bash
python3 $SKILL_DIR/scripts/inspect_image.py grid    src.png work/grid.png --step 50   # coordinate grid
python3 $SKILL_DIR/scripts/inspect_image.py palette src.png                           # main colors
python3 $SKILL_DIR/scripts/inspect_image.py crop    src.png work/z1.png 0 0 600 300 --scale 3 --step 10
python3 $SKILL_DIR/scripts/inspect_image.py colors  src.png 120,240 800,300           # exact hex at points
```

Look at `grid.png` to get coordinates of every region, then zoom into dense areas with `crop`
(grid labels are in source pixels, so readings go straight into the spec). Sample colors instead
of eyeballing them — "dark navy" guesses drift visibly.

Write down an inventory before building: title/headers, containers and bands (with corner type:
square / small radius / pill), text blocks by level (same level → same size), arrows (single vs
bent, one or two heads, dashed?), icons (what each depicts), tables, and anything that is truly
a photo/illustration.

### 2. Choose icons

For each icon, decide what it *means* (server, database, shield, document, person, docker…), then search:

```bash
python3 $SKILL_DIR/scripts/icons.py search database --limit 10 --sheet work/cand_db.png
python3 $SKILL_DIR/scripts/icons.py search docker --lib simple
```

Look at the contact sheet and choose the closest visual match. Library choice:

| source icon looks like | use |
|---|---|
| Azure/Microsoft service icon, colorful cloud-service glyph | `azure:` (official, keep colors) |
| generic outline glyph (server, laptop, globe, cpu, ban, search) | `lucide:` + sampled color |
| generic solid/filled glyph (person, shield, document, database, gear) | `material:<name>-fill` + sampled color (`material:<name>` = outline) |
| product/brand logo (Docker, PostgreSQL, NVIDIA, GitHub, Python…) | `simple:` |

If the user asked to prefer Azure icons, try `--lib azure` first and fall back to lucide/simple
only when Azure has no fitting icon. A close icon from a library is the right answer even if not
pixel-identical — it is editable, which a cropped bitmap is not. Crop a bitmap (`type: image`)
only for photos, screenshots, or illustrations no icon can stand for.

### 3. Write the spec and build

Write `work/spec.json` following `references/spec.md` (read it before writing the first spec).
Order elements back-to-front: background panels → bands/cards → lines/arrows → icons → text.

```bash
python3 $SKILL_DIR/scripts/build_pptx.py work/spec.json out.pptx
```

Principles that matter for editability and fidelity:

- One logical object = one PowerPoint object. A bent arrow is one polyline, a label inside a box
  is the box's own text (or a text box exactly on top), a process band is a row of chevrons.
- Text sizes: measure glyph height and convert (`size_px ≈ CJK glyph height × 1.13`). Keep one
  size per text level across the slide. Use `wrap: false` and one paragraph per line for labels,
  so line breaks match the source regardless of font metrics.
- Leave ~5-10% horizontal slack in text boxes for bold Latin/CJK mixed labels: Meiryo and the
  preview's fallback fonts are wider than many fonts used in AI-generated slide images. If a label
  still overflows, shrink that level's size slightly rather than letting it wrap.
- Corners: measure radius on a zoomed crop; small radii stay small.
- Name objects and group per logical unit (a layer row, a badge + label) so the Selection Pane is usable.

### 4. Preview, compare, fix

```bash
python3 $SKILL_DIR/scripts/preview.py out.pptx src.png work/prev
```

Open `work/prev/compare.png` (source | rebuild) and `overlay.png` (blend; misalignment shows as
ghosting). Check: missing items, text overflow or wrong line breaks, size of each text level,
positions, colors, arrow directions, icon choice. Fix the spec and rebuild. Two or three rounds is
normal; stop when differences are only font rendering (the sandbox lacks Office fonts, so glyph
shapes differ slightly — judge size and position, not typeface).

### 5. Deliver

Give the user the .pptx. Report briefly: which icons came from which library, anything
approximated (e.g. "no Azure icon for Docker → Simple Icons logo"), and anything kept as a bitmap.

**Google Slides:** upload the .pptx to Google Drive with conversion to Google Slides (if a Drive
connector is available) or tell the user to open it via Drive → Open with Google Slides. Note that
SVG icons become images there (still movable/resizable, not recolorable).

## Licensing notes (tell the user when relevant)

- Azure Architecture Icons (`assets/icons/azure`, V24, © Microsoft): allowed in architecture
  diagrams, training materials, and documentation; don't modify their shape or colors.
- Lucide (ISC) and Simple Icons (CC0) are free to use; brand logos remain their owners' trademarks.
