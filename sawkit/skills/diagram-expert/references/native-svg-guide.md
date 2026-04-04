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

### General Purpose

| Color    | Fill      | Stroke    | Use for                    |
|----------|-----------|-----------|----------------------------|
| Gray     | `#e9ecef` | `#868e96` | External, inactive, labels |
| Blue     | `#d0ebff` | `#1971c2` | Primary, active, HTTP      |
| Green    | `#b2f2bb` | `#2f9e44` | Success, engine, logic     |
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
