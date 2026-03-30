# Diagram Tier Ladder — Decision Matrix

## Quick Reference

| Complexity          | Node Count | Target Format    | Recommended Tier             |
|---------------------|-----------|------------------|------------------------------|
| Trivial             | 1-5       | Any              | 1: Unicode/ASCII inline      |
| Simple structured   | 3-10      | Terminal/text    | 2: beautiful-mermaid ASCII   |
| Simple structured   | 3-10      | GitHub markdown  | 3: Mermaid fenced blocks     |
| Medium              | 5-20      | Image file       | 4: Mermaid Chart MCP         |
| Complex UML         | 5-30      | Image with icons | 5: PlantUML                  |
| Large graph         | 20-200+   | SVG/PNG          | 6: Graphviz/D2               |
| Data visualization  | N/A       | SVG/PNG          | 7: Vega-Lite                 |
| Specialized         | Any       | SVG/PNG          | 8: Kroki                     |

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

## Tier 5: PlantUML

**Use when:**

- Need AWS/Azure/Kubernetes icon sets in diagrams
- Complex component or deployment diagrams
- Need ASCII art output (`plantuml -utxt`)
- UML diagram types that mermaid doesn't support well

**Install:** `brew install plantuml` (requires Java)

## Tier 6: Graphviz/D2

**Use when:**

- Graph has 50+ nodes (Graphviz auto-layout shines)
- Need dependency trees, call graphs, state machines at scale
- D2: when visual quality of exported SVG matters most

**Install:** `brew install graphviz` / `brew install d2`

## Tier 7: Vega-Lite

**Use when:** Visualizing data — bar charts, line charts, scatter plots, heatmaps, histograms.

**How:** Write a JSON spec, render with `vl2svg` or `vl-convert`.

## Tier 8: Kroki

**Use when:** Need a specialized diagram type not covered above — bytefield (protocol headers), WaveDrom (timing), DBML (database), Nomnoml, Pikchr, etc.

**How:** Use Kroki API or CLI: `kroki convert input.ext -t svg`
