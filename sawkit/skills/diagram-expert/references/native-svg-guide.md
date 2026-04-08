# Native SVG Generation Guide (Tier 5b)

## When to Use

**Try Mermaid `block-beta` first (Tier 5).** Only drop to native SVG when `block-beta` isn't sufficient.

Use native SVG via Python when:

1. **Mermaid `block-beta` isn't enough** — need visible layer labels, pixel-perfect spacing, or complex per-item color overrides
2. **Re-runnable generator** — diagram regenerated from data, script lives next to SVG for future updates
3. **Precise positioning** — exact pixel control over element placement
4. **No npm/Mermaid dependency** — pure Python, zero external tools
5. **Universal rendering** — must display identically in browsers, Bitbucket, GitHub, and SVG viewers

## When NOT to Use

- Layered layouts that `block-beta` handles → Tier 5
- Simple flows → Tier 3 (Mermaid fenced blocks)
- Need auto-layout for tangled graphs → Tier 7 (Graphviz)
- Need cloud/UML icons → Tier 6 (PlantUML)
- Data visualization → Tier 8 (Vega-Lite)

## Lessons Learned

### Mermaid `flowchart` vs `block-beta` for Layered Layouts

- **`flowchart` with `direction LR` inside subgraphs is unreliable.** Dagre/elk ignores it when it conflicts with the graph's global direction. Nodes stack vertically. Subgroup labels truncate.
- **`block-beta` with `columns` solves this.** It was designed for grid/block layouts. Use it for horizontal layers.
- **Cross-subgraph edges in `flowchart` cause spaghetti.** Individual node-to-node edges between layers create tangles. Block-to-block edges in `block-beta` are cleaner.
- **`block-beta` limitation:** Block titles may not render as visible labels in all Mermaid versions. This is the main reason to drop to native SVG.
- **The Mermaid Chart MCP tool may prepend `<style>` tags** before the `<svg>` element. Strip them before using the raw SVG output.

### SVG via foreignObject Fails

- **`<foreignObject>` embeds HTML inside SVG** — sounds great, but flexbox, `<br>` tags, and CSS layouts break across viewers.
- **Self-closing tags required.** `<br>` must be `<br/>` in XHTML context. Forgetting this silently breaks rendering.
- **Bitbucket/GitHub strip foreignObject** in some contexts, showing nothing.

### Native SVG Works Everywhere

- `<rect>`, `<text>`, `<line>`, `<polygon>` are universally supported.
- No dependencies, no build tools, no runtime.
- Python `xml.etree.ElementTree` can validate the output.

## File Organization

```
docs/diagrams/
  gen-my-diagram.py     # Python generator script (source of truth)
  my-diagram.svg        # Generated output (referenced from markdown)
```

The generator script is the source of truth. The SVG is a build artifact. To update the diagram, edit the script and re-run it.

## Template: Layered Architecture Diagram

```python
#!/usr/bin/env python3
"""Generate native SVG: layered architecture diagram."""
from pathlib import Path

W = 1100          # canvas width
PAD = 30          # outer padding
LW = W - 2 * PAD # layer width
LAYER_PAD = 16    # padding inside layer
ITEM_H = 70       # item box height
ITEM_GAP = 10     # gap between items
LAYER_GAP = 14    # gap between layers
ARROW_GAP = 10    # space for arrow
R = 10            # corner radius

elements = []
y_cursor = PAD


def esc(s):
    """XML-escape text for SVG."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(x, y, w, h, fill, stroke, rx=R, dash=False):
    d = ' stroke-dasharray="8 4"' if dash else ""
    elements.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>')


def text(x, y, lines, size=12, bold=False, color="#1e1e1e"):
    weight = "bold" if bold else "normal"
    for i, line in enumerate(lines):
        ly = y + i * (size + 4)
        elements.append(
            f'<text x="{x}" y="{ly}" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="middle" dominant-baseline="middle">{esc(line)}</text>')


def label(x, y, txt, size=11, color="#868e96"):
    elements.append(
        f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="700" fill="{color}" '
        f'letter-spacing="1.5" text-anchor="start" '
        f'dominant-baseline="middle">{esc(txt)}</text>')


def arrow_down(x, y1, y2):
    elements.append(
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-6}" '
        f'stroke="#adb5bd" stroke-width="2"/>')
    elements.append(
        f'<polygon points="{x-5},{y2-8} {x+5},{y2-8} {x},{y2}" '
        f'fill="#adb5bd"/>')


def draw_layer(label_text, items, layer_fill, layer_stroke,
               item_fill, item_stroke, dash=False, item_overrides=None):
    """Draw a horizontal layer with evenly-spaced items.

    items: list of (title, description) tuples
    item_overrides: dict of {title: (fill, stroke)} for per-item colors
    """
    global y_cursor
    item_overrides = item_overrides or {}
    n = len(items)
    item_w = (LW - 2 * LAYER_PAD - (n - 1) * ITEM_GAP) / n
    layer_h = ITEM_H + 2 * LAYER_PAD + 24

    rect(PAD, y_cursor, LW, layer_h, layer_fill, layer_stroke, dash=dash)
    label(PAD + LAYER_PAD, y_cursor + 18, label_text)

    item_y = y_cursor + 34
    for i, (title, desc) in enumerate(items):
        ix = PAD + LAYER_PAD + i * (item_w + ITEM_GAP)
        if title in item_overrides:
            f, s = item_overrides[title]
            rect(ix, item_y, item_w, ITEM_H, f, s)
        else:
            rect(ix, item_y, item_w, ITEM_H, item_fill, item_stroke)
        cx = ix + item_w / 2
        text(cx, item_y + 18, [title], size=13, bold=True)
        text(cx, item_y + 36, desc.split("\\n"), size=10, color="#555")

    y_cursor += layer_h


def draw_arrow():
    global y_cursor
    arrow_down(W / 2, y_cursor + 2, y_cursor + ARROW_GAP + 14)
    y_cursor += ARROW_GAP + 16


# ── Define your layers here ─────────────────────────────
# draw_layer("LAYER NAME", [...items...], layer_fill, layer_stroke,
#            item_fill, item_stroke)
# draw_arrow()
# ... repeat for each layer ...

# ── Output ──────────────────────────────────────────────
total_h = y_cursor + PAD
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">
<rect width="{W}" height="{total_h}" fill="#ffffff"/>
{"".join(elements)}
</svg>'''

out = Path(__file__).parent / "my-diagram.svg"
with open(out, "w") as f:
    f.write(svg)
print(f"Generated: {out} ({len(svg)} chars, {total_h}px)")
```

## Relationship / Dependency Diagrams

Grid-layout diagrams with boxes and arrows (module dependencies, system maps, data flows) need careful routing to avoid visual clutter.

### Connection Point Rules

Choose entry/exit points based on the direction the arrow travels, not arbitrary box corners:

- **Arrow going down** (same column) → exit bottom center, enter top center
- **Arrow going right** (source left of target) → enter target's **left center**
- **Arrow going left** (source right of target) → enter target's **right center**
- **Diagonal (down-right)** → exit bottom, enter left center (elbow_vh)
- **Diagonal (down-left)** → exit bottom, enter right center (elbow_vh)

**Never** use arbitrary fractional points like "top-left 30%" or "top-right 70%" — they look arbitrary and make connection intent unclear. Use the center of the side the arrow approaches from.

### Gutter Routing (Cross-Row Arrows)

When arrows must cross between rows in a grid:

1. **Route horizontal segments through gutters** (the space between rows), not at box-edge y-coordinates. Horizontal lines at the same y as box tops merge visually with box borders.
2. **Use VHV (vertical-horizontal-vertical) elbows** for multi-column jumps: down from source into gutter → horizontal across gutter → down to target. The horizontal segment stays in empty space.
3. **Stagger mid_y values** when multiple VHV paths share the same gutter. Offset by ~15-20px so horizontal segments don't overlap (e.g., `G12 - 18` for one path, `G12 + 2` for another).
4. **Check vertical segments don't cross boxes.** Before routing, verify the x-coordinate of each vertical segment doesn't fall within any box's x-range in the row it passes through.

### Elbow Patterns

```python
# elbow_vh: Down then across (for 1-column offsets)
# Path: vertical drop → curve → horizontal to target
# Label: on the vertical segment at (x_start, midpoint_y)
elbow_vh(source_bottom_x, source_bottom_y, target_left_x, target_left_y)

# elbow_vhv: Down → across → down (for 2+ column jumps)
# Path: vertical → horizontal in gutter → vertical to target
# Label: on the horizontal segment at (midpoint_x, mid_y - 10)
elbow_vhv(source_x, source_y, target_x, target_y, mid_y=gutter_center)
```

**Label collision avoidance:** Estimate label width as `len(text) * 5.5 + 8` pixels. Check that no two labels' bounding boxes overlap in both x and y.

### Verification

Always export to PNG and visually inspect:

```bash
rsvg-convert -o /tmp/diagram.png docs/diagrams/my-diagram.svg
```

Check for:

- Arrows passing through boxes (routing errors)
- Labels overlapping other labels or box borders
- Connection points — is it clear where each arrow enters/exits?
- Color distinguishability — can all status colors be told apart at a glance?

Include a programmatic verification function in the generator:

```python
# After building SVG, check for box-box overlaps
for i, (x1, y1, w1, h1, n1) in enumerate(all_boxes):
    for j, (x2, y2, w2, h2, n2) in enumerate(all_boxes):
        if i >= j: continue
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            print(f"OVERLAP: {n1} vs {n2}")

# Check label-box and label-label overlaps similarly
```

## Template: Grid / Matrix Diagram

For dependency maps, module grids, or any diagram where items sit on a 2D grid with arrows between them:

```python
#!/usr/bin/env python3
"""Generate native SVG: grid diagram with routed arrows."""
from pathlib import Path

W = 1100
PAD = 40
COLS = 4
ROWS = 3
BOX_W = 200
BOX_H = 60
GAP_X = 50
GAP_Y = 80
R = 8

elements = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(x, y, w, h, fill, stroke, rx=R):
    elements.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')


def text(x, y, label, size=13, bold=False, color="#1e1e1e"):
    wt = "bold" if bold else "normal"
    elements.append(
        f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{wt}" fill="{color}" '
        f'text-anchor="middle" dominant-baseline="middle">{esc(label)}</text>')


def box_pos(row, col):
    """Return (x, y) for top-left of box at grid position."""
    x = PAD + col * (BOX_W + GAP_X)
    y = PAD + row * (BOX_H + GAP_Y)
    return x, y


def box_center(row, col):
    x, y = box_pos(row, col)
    return x + BOX_W / 2, y + BOX_H / 2


def box_bottom(row, col):
    x, y = box_pos(row, col)
    return x + BOX_W / 2, y + BOX_H


def box_top(row, col):
    x, y = box_pos(row, col)
    return x + BOX_W / 2, y


def box_left(row, col):
    x, y = box_pos(row, col)
    return x, y + BOX_H / 2


def box_right(row, col):
    x, y = box_pos(row, col)
    return x + BOX_W, y + BOX_H / 2


def arrow(x1, y1, x2, y2, color="#adb5bd"):
    """Straight arrow with arrowhead."""
    import math
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    ux, uy = dx / length, dy / length
    # Shorten line to leave room for arrowhead
    ex, ey = x2 - ux * 8, y2 - uy * 8
    elements.append(
        f'<line x1="{x1}" y1="{y1}" x2="{ex}" y2="{ey}" '
        f'stroke="{color}" stroke-width="2"/>')
    # Arrowhead
    px, py = -uy * 5, ux * 5
    elements.append(
        f'<polygon points="{ex + px},{ey + py} {ex - px},{ey - py} {x2},{y2}" '
        f'fill="{color}"/>')


def arrow_bidir(x1, y1, x2, y2, color="#adb5bd"):
    """Bidirectional arrow (arrowheads on both ends)."""
    import math
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    ux, uy = dx / length, dy / length
    px, py = -uy * 5, ux * 5
    # Shorten both ends
    sx, sy = x1 + ux * 8, y1 + uy * 8
    ex, ey = x2 - ux * 8, y2 - uy * 8
    elements.append(
        f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" '
        f'stroke="{color}" stroke-width="2"/>')
    # Head at end
    elements.append(
        f'<polygon points="{ex + px},{ey + py} {ex - px},{ey - py} {x2},{y2}" '
        f'fill="{color}"/>')
    # Head at start
    elements.append(
        f'<polygon points="{sx + px},{sy + py} {sx - px},{sy - py} {x1},{y1}" '
        f'fill="{color}"/>')


def elbow_vh(x1, y1, x2, y2, color="#adb5bd"):
    """Vertical then horizontal elbow arrow."""
    elements.append(
        f'<path d="M {x1} {y1} L {x1} {y2} L {x2} {y2}" '
        f'fill="none" stroke="{color}" stroke-width="2"/>')
    dx = 1 if x2 > x1 else -1
    elements.append(
        f'<polygon points="{x2 - dx * 8},{y2 - 5} {x2 - dx * 8},{y2 + 5} {x2},{y2}" '
        f'fill="{color}"/>')


def elbow_vhv(x1, y1, x2, y2, mid_y, color="#adb5bd"):
    """Vertical-horizontal-vertical elbow for cross-row arrows."""
    elements.append(
        f'<path d="M {x1} {y1} L {x1} {mid_y} L {x2} {mid_y} L {x2} {y2}" '
        f'fill="none" stroke="{color}" stroke-width="2"/>')
    dy = 1 if y2 > mid_y else -1
    elements.append(
        f'<polygon points="{x2 - 5},{y2 - dy * 8} {x2 + 5},{y2 - dy * 8} {x2},{y2}" '
        f'fill="{color}"/>')


def curved_arrow(x1, y1, x2, y2, color="#adb5bd", bend=30):
    """Curved arrow using a quadratic bezier."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - bend
    elements.append(
        f'<path d="M {x1} {y1} Q {mx} {my} {x2} {y2}" '
        f'fill="none" stroke="{color}" stroke-width="2" '
        f'marker-end="url(#arrowhead)"/>')


def add_arrowhead_marker(color="#adb5bd"):
    """Add reusable SVG marker for curved arrows."""
    elements.insert(0,
        f'<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" '
        f'refX="10" refY="3.5" orient="auto">'
        f'<polygon points="0 0, 10 3.5, 0 7" fill="{color}"/>'
        f'</marker></defs>')


def legend(x, y, items, title="Legend"):
    """Draw a legend box. items: list of (label, fill, stroke) tuples."""
    swatch = 14
    row_h = 22
    max_label = max(len(l) for l, _, _ in items)
    lw = max_label * 7 + swatch + 30
    lh = len(items) * row_h + 30
    rect(x, y, lw, lh, "#ffffff", "#dee2e6", rx=6)
    text(x + lw / 2, y + 14, title, size=11, bold=True, color="#495057")
    for i, (label, fill, stroke) in enumerate(items):
        iy = y + 28 + i * row_h
        elements.append(
            f'<rect x="{x + 10}" y="{iy}" width="{swatch}" '
            f'height="{swatch}" rx="3" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1"/>')
        elements.append(
            f'<text x="{x + 10 + swatch + 8}" y="{iy + swatch / 2}" '
            f'font-family="Helvetica,Arial,sans-serif" font-size="11" '
            f'fill="#495057" dominant-baseline="middle">{esc(label)}</text>')


# ── Define your grid items here ────────────────────────
# grid = [
#     [("Module A", "#d0ebff", "#1971c2"), ("Module B", "#b2f2bb", "#2f9e44"), ...],
#     [("Module C", "#dbe4ff", "#4263eb"), None, ...],  # None = empty cell
# ]
# for r, row in enumerate(grid):
#     for c, item in enumerate(row):
#         if item is None: continue
#         name, fill, stroke = item
#         x, y = box_pos(r, c)
#         rect(x, y, BOX_W, BOX_H, fill, stroke)
#         cx, cy = box_center(r, c)
#         text(cx, cy, name, bold=True)

# ── Draw arrows between grid items ─────────────────────
# arrow(*box_bottom(0, 0), *box_top(1, 0))
# elbow_vh(*box_bottom(0, 0), *box_left(1, 1))

# ── Output ─────────────────────────────────────────────
total_w = PAD * 2 + COLS * BOX_W + (COLS - 1) * GAP_X
total_h = PAD * 2 + ROWS * BOX_H + (ROWS - 1) * GAP_Y
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">
<rect width="{total_w}" height="{total_h}" fill="#ffffff"/>
{"".join(elements)}
</svg>'''

out = Path(__file__).parent / "grid-diagram.svg"
with open(out, "w") as f:
    f.write(svg)
print(f"Generated: {out} ({len(svg)} chars)")
```

### Arrow Types Summary

| Function         | Use case                                            |
|------------------|-----------------------------------------------------|
| `arrow`          | Straight arrow between any two points               |
| `arrow_bidir`    | Bidirectional (arrowheads on both ends)              |
| `arrow_down`     | Vertical downward arrow (from layered template)      |
| `elbow_vh`       | Vertical-then-horizontal L-shaped routing            |
| `elbow_vhv`      | Vertical-horizontal-vertical for cross-row routing   |
| `curved_arrow`   | Quadratic bezier curve (needs `add_arrowhead_marker`) |

### Legend Helper

Use `legend()` to add a color key to any diagram:

```python
legend(x=total_w - 180, y=10, items=[
    ("Production", "#b2f2bb", "#2f9e44"),
    ("Partial", "#dbe4ff", "#4263eb"),
    ("Skeletal", "#fff3bf", "#e8590c"),
    ("Not Started", "#f1f3f5", "#868e96"),
], title="Status")
```

### Responsive SVG

For diagrams that should scale to container width, use `viewBox` without fixed `width`/`height`:

```python
# Fixed size (pixel-precise, no scaling)
svg = f'<svg xmlns="..." width="{W}" height="{H}" viewBox="0 0 {W} {H}">'

# Responsive (scales to container, maintains aspect ratio)
svg = f'<svg xmlns="..." viewBox="0 0 {W} {H}" style="max-width:{W}px;width:100%">'
```

### Text Wrapping

SVG has no native text wrapping. For multi-line text in boxes, split manually:

```python
def wrapped_text(x, y, content, max_chars=25, size=12, color="#1e1e1e"):
    """Split text into lines that fit within max_chars."""
    words = content.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current = f"{current} {word}" if current else word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    # Center vertically
    total_h = len(lines) * (size + 4)
    start_y = y - total_h / 2 + size / 2
    text(x, start_y, lines, size=size, color=color)
```

## Color Palette

### Architecture Diagrams

| Purpose         | Layer Fill | Layer Stroke | Item Fill  | Item Stroke |
|-----------------|-----------|-------------|-----------|------------|
| External        | `#f1f3f5` | `#868e96`   | `#e9ecef` | `#868e96`  |
| HTTP / API      | `#e7f5ff` | `#1971c2`   | `#d0ebff` | `#1971c2`  |
| Business logic  | `#d8f5e0` | `#2f9e44`   | `#b2f2bb` | `#2f9e44`  |
| Orchestration   | `#f3f0ff` | `#7048e8`   | `#e5dbff` | `#7048e8`  |
| Fallback / warn | —         | —           | `#fff3bf` | `#e8590c`  |
| Data / infra    | `#f8f9fa` | `#495057`   | `#ffffff` | `#495057`  |
| Admin / internal| —         | —           | `#fff4e6` | `#e8590c`  |

### Status / Build Progress

For diagrams that show module maturity or build progress, use colors from **different hue families** so they're distinguishable at a glance. Avoid teal/cyan for "partial" — it blends with green ("production") in most renderers.

| Status       | Fill      | Stroke    | Hue family |
|-------------|-----------|-----------|------------|
| Production  | `#b2f2bb` | `#2f9e44` | Green      |
| Partial     | `#dbe4ff` | `#4263eb` | Indigo     |
| Skeletal    | `#fff3bf` | `#e8590c` | Yellow     |
| Not started | `#f1f3f5` | `#868e96` | Gray       |

**Why indigo for Partial?** Teal (`#c3fae8`) and cyan (`#c5f6fa`) both blend with green on screen and in print. Indigo (`#dbe4ff`) is purple-tinted, clearly distinct from green and yellow.

**Why gray for Not Started?** Light blue (`#e7f5ff`) is too close to indigo (`#dbe4ff`) — both are in the blue family. Gray conveys "absence of work" and is visually distinct from all three active-status colors.

### General Purpose

| Color    | Fill      | Stroke    | Use for                    |
|----------|-----------|-----------|----------------------------|
| Gray     | `#e9ecef` | `#868e96` | External, inactive, labels |
| Blue     | `#d0ebff` | `#1971c2` | Primary, active, HTTP      |
| Green    | `#b2f2bb` | `#2f9e44` | Success, engine, logic     |
| Indigo   | `#dbe4ff` | `#4263eb` | In-progress, partial       |
| Purple   | `#e5dbff` | `#7048e8` | Orchestration, decisions   |
| Yellow   | `#fff3bf` | `#e8590c` | Warning, fallback          |
| Red      | `#ffc9c9` | `#e03131` | Error, failure             |
| Orange   | `#fff4e6` | `#e8590c` | Admin, internal            |

## SVG Primitives Reference

### Rounded Rectangle

```xml
<rect x="10" y="10" width="200" height="60" rx="10"
      fill="#d0ebff" stroke="#1971c2" stroke-width="1.5"/>
```

### Centered Text

```xml
<text x="110" y="40" font-family="Helvetica,Arial,sans-serif"
      font-size="14" font-weight="bold" fill="#1e1e1e"
      text-anchor="middle" dominant-baseline="middle">Label</text>
```

### Down Arrow (line + polygon arrowhead)

```xml
<line x1="100" y1="80" x2="100" y2="114" stroke="#adb5bd" stroke-width="2"/>
<polygon points="95,112 105,112 100,120" fill="#adb5bd"/>
```

### Dashed Border (for optional/infrastructure layers)

```xml
<rect ... stroke-dasharray="8 4"/>
```

## Validation

Always validate before committing:

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('diagram.svg'); print('Valid XML')"
```

Common issues:

- `&` in text → must be `&amp;`
- `<` or `>` in text → must be `&lt;` / `&gt;`
- Unclosed tags
- Missing `xmlns` attribute on root `<svg>`
