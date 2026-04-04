# Diagram Tier Ladder — Decision Matrix

## Quick Reference

| Complexity          | Node Count | Target Format    | Recommended Tier             |
|---------------------|-----------|------------------|------------------------------|
| Trivial             | 1-5       | Any              | 1: Unicode/ASCII inline      |
| Simple structured   | 3-10      | Terminal/text    | 2: beautiful-mermaid ASCII   |
| Simple structured   | 3-10      | GitHub markdown  | 3: Mermaid fenced blocks     |
| Medium              | 5-20      | Image file       | 4: Mermaid Chart MCP         |
| Layered / grid      | 5-30      | SVG/Markdown     | 5: Mermaid block-beta        |
| Pixel-precise       | 5-30      | SVG              | 5b: Native SVG (Python)      |
| Complex UML         | 5-30      | Image with icons | 6: PlantUML                  |
| Large graph         | 20-200+   | SVG/PNG          | 7: Graphviz/D2               |
| Data visualization  | N/A       | SVG/PNG          | 8: Vega-Lite                 |
| Specialized         | Any       | SVG/PNG          | 9: Kroki                     |

## Tier 1: Unicode/ASCII Inline

**Use when:** A simple flow, tree, or state can be drawn in 1-5 lines.

**Characters to use:**

| Character | Unicode   | Purpose           |
|-----------|-----------|-------------------|
| `→`       | U+2192    | Flow direction    |
| `←`       | U+2190    | Reverse flow      |
| `↓`       | U+2193    | Downward flow     |
| `↑`       | U+2191    | Upward flow       |
| `├──`     | U+251C    | Tree branch       |
| `└──`     | U+2514    | Tree leaf         |
| `│`       | U+2502    | Vertical line     |
| `─`       | U+2500    | Horizontal line   |
| `┌` `┐`   | U+250C/10 | Box corners       |
| `└` `┘`   | U+2514/18 | Box corners       |
| `╔` `╗`   | U+2554/57 | Double box        |
| `╚` `╝`   | U+255A/5D | Double box        |
| `▼` `▶`   | U+25BC/B6 | Arrows            |
| `✅` `❌`  | Emoji     | Status indicators |

**Examples:**

Linear flow:

```text
Input → Validate → Process → Store → Response
```

Decision:

```text
                  ┌─ Valid ───→ Process
Input → Validate ─┤
                  └─ Invalid ─→ Reject
```

Tree:

```text
src/
├── components/
│   ├── Header.tsx
│   └── Footer.tsx
├── pages/
│   └── index.tsx
└── utils/
    └── helpers.ts
```

Box diagram:

```text
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Frontend │────→│   API    │────→│ Database │
└──────────┘     └──────────┘     └──────────┘
```

## Tier 2: beautiful-mermaid ASCII

**Use when:** Need structured ASCII with proper layout (branching, parallel paths) that hand-drawing would be tedious.

**How:** Write mermaid syntax, render with `render-ascii.mjs`.

Supports: flowcharts, sequence diagrams, state diagrams, ER diagrams, class diagrams, XY charts.

## Tier 3: Mermaid Fenced Blocks

**Use when:** Diagram goes in a `.md` file that will be viewed on GitHub, GitLab, or any renderer that supports mermaid.

**Supported diagram types:** flowchart, sequence, class, state, ER, gantt, pie, mindmap, timeline, quadrant, sankey, git graph, C4, block.

## Tier 4: Mermaid Chart MCP

**Use when:** Need a rendered image file (SVG/PNG) from mermaid, or need to validate complex mermaid syntax.

**How:** Call the `mcp__claude_ai_Mermaid_Chart__validate_and_render_mermaid_diagram` tool.

## Tier 5: Mermaid block-beta

**Use when:**

- Layered architecture diagrams — horizontal rows of items
- Grid layouts with different column counts per layer
- Need Mermaid's ecosystem (fenced blocks in markdown, mmdc rendering, MCP validation)

**Key insight:** `flowchart` with `direction LR` inside subgraphs is unreliable for layered layouts (nodes stack vertically, labels truncate). Use `block-beta` with `columns` instead — it was designed for grid/block layouts.

**Pattern:**

```
block-beta
    columns 1                          # layers stack vertically

    block:layer1["Label"]:1            # first layer
        columns 4                      # 4 items side-by-side
        A["Item A"] B["Item B"] C["Item C"] D["Item D"]
    end

    space                              # visual gap between layers

    block:layer2["Label"]:1            # second layer
        columns 3
        E["Item E"] F["Item F"] G["Item G"]
    end

    layer1 --> layer2                  # connect layers with arrows

    style layer1 fill:#e7f5ff,stroke:#1971c2
    style A fill:#d0ebff,stroke:#1971c2
```

**Render:** `mmdc -i diagram.mmd -o diagram.svg -b transparent`

**Limitation:** Block titles (`block:name["Title"]`) may not render as visible labels in all Mermaid versions. If you need visible layer labels, drop to Tier 5b (Native SVG).

## Tier 5b: Native SVG (Python)

**Use when:**

- Mermaid `block-beta` isn't enough — need visible layer labels, pixel-perfect spacing, or complex per-item styling
- Need a re-runnable generator script that lives alongside the SVG output
- No Mermaid/npm dependency desired — pure Python, zero external tools

**When NOT to use:**

- Simple flows that Mermaid handles fine (use Tier 3/4)
- Layered layout that `block-beta` handles (use Tier 5)
- Need auto-layout for complex graphs (use Tier 7: Graphviz)
- Need UML icons (use Tier 6: PlantUML)

**Why not foreignObject SVG?** Embedding HTML/CSS inside SVG via `<foreignObject>` is fragile — flexbox, `<br>` tags break across viewers. Native SVG primitives (`<rect>`, `<text>`, `<line>`) render identically everywhere.

**Pattern:**

```
docs/diagrams/
  gen-my-diagram.py     # source — edit and re-run
  my-diagram.svg        # output — reference from docs
```

**Layered architecture template:** Define layers as data, loop to generate SVG elements. Each layer is a rounded rect containing item rects with centered text. Arrows between layers are simple vertical lines with polygon arrowheads.

**Color palette for architecture diagrams:**

| Purpose        | Fill      | Stroke    |
|----------------|-----------|-----------|
| External       | `#e9ecef` | `#868e96` |
| HTTP/API       | `#d0ebff` | `#1971c2` |
| Business logic | `#b2f2bb` | `#2f9e44` |
| Orchestration  | `#e5dbff` | `#7048e8` |
| Fallback/warn  | `#fff3bf` | `#e8590c` |
| Data stores    | `#ffffff` | `#495057` |
| Admin/internal | `#fff4e6` | `#e8590c` |

**Key rules:**

- XML-escape all text: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`
- Font: `font-family="Helvetica,Arial,sans-serif"` (cross-platform)
- Center text: `text-anchor="middle"` + `dominant-baseline="middle"`
- Validate: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg'); print('Valid')"`
- Use `pathlib.Path(__file__).parent` for output path so script works from any directory

## Tier 6: PlantUML

(Previously Tier 5)

**Use when:**

- Need AWS/Azure/Kubernetes icon sets in diagrams
- Complex component or deployment diagrams
- Need ASCII art output (`plantuml -utxt`)
- UML diagram types that mermaid doesn't support well

**Install:** `brew install plantuml` (requires Java)

## Tier 7: Graphviz/D2

**Use when:**

- Graph has 50+ nodes (Graphviz auto-layout shines)
- Need dependency trees, call graphs, state machines at scale
- D2: when visual quality of exported SVG matters most

**Install:** `brew install graphviz` / `brew install d2`

## Tier 8: Vega-Lite

**Use when:** Visualizing data — bar charts, line charts, scatter plots, heatmaps, histograms.

**How:** Write a JSON spec, render with `vl2svg` or `vl-convert`.

## Tier 9: Kroki

**Use when:** Need a specialized diagram type not covered above — bytefield (protocol headers), WaveDrom (timing), DBML (database), Nomnoml, Pikchr, etc.

**How:** Use Kroki API or CLI: `kroki convert input.ext -t svg`
