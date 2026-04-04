#!/usr/bin/env python3
"""Recommend a diagram tier and provide a starter template.

Usage:
    python select-tier.py "simple login flow with 3 steps"
    python select-tier.py "AWS architecture with EC2, RDS, S3"
    python select-tier.py "database schema for users, orders, products"
"""

import sys

TIERS = {
    1: {
        "name": "Unicode/ASCII inline",
        "keywords": [
            "simple", "linear", "trivial", "tree", "directory", "list",
            "small", "3 steps", "4 steps", "5 steps", "quick",
        ],
        "max_nodes": 5,
    },
    2: {
        "name": "beautiful-mermaid ASCII",
        "keywords": [
            "ascii", "terminal", "text", "plain", "console",
            "text-only", "no images", "cli",
        ],
        "max_nodes": 10,
    },
    3: {
        "name": "Mermaid fenced blocks",
        "keywords": [
            "github", "markdown", "readme", "docs", "flowchart", "sequence",
            "state", "class", "er", "gantt", "mindmap", "pie",
            "flow", "process", "workflow", "login", "auth", "api",
            "request", "response", "pipeline", "diagram",
        ],
        "max_nodes": 20,
    },
    4: {
        "name": "Mermaid Chart MCP",
        "keywords": [
            "image", "svg", "png", "export", "render", "validate",
            "download", "file", "output",
        ],
        "max_nodes": 20,
    },
    5: {
        "name": "Native SVG (Python)",
        "keywords": [
            "layered", "layers", "architecture", "precise", "layout",
            "horizontal", "side-by-side", "stacked", "exact",
            "module map", "system overview", "native svg",
            "mermaid broken", "mermaid fails", "pixel",
        ],
        "max_nodes": 30,
    },
    6: {
        "name": "PlantUML",
        "keywords": [
            "aws", "azure", "kubernetes", "k8s", "uml", "deployment",
            "component", "cloud", "icon", "ec2", "rds", "s3", "lambda",
            "gcp", "gke", "ecs", "eks", "infrastructure", "infra",
        ],
        "max_nodes": 30,
    },
    7: {
        "name": "Graphviz/D2",
        "keywords": [
            "large", "dependency", "call graph", "complex", "50+",
            "many nodes", "auto-layout", "dependencies", "modules",
            "packages", "imports", "graph", "network", "topology",
        ],
        "max_nodes": 500,
    },
    8: {
        "name": "Vega-Lite",
        "keywords": [
            "chart", "bar", "line", "scatter", "heatmap", "histogram",
            "data", "visualization", "plot", "trend", "metrics",
            "statistics", "analytics", "numbers", "values", "counts",
        ],
        "max_nodes": 0,
    },
    9: {
        "name": "Kroki",
        "keywords": [
            "bytefield", "protocol", "wavedrom", "timing", "dbml",
            "nomnoml", "pikchr", "railroad", "specialized", "packet",
            "signal", "timing diagram", "byte", "wire",
        ],
        "max_nodes": 0,
    },
}

TEMPLATES = {
    1: """```text
Step 1 → Step 2 → Step 3 → Done
```""",
    2: """```bash
echo '```mermaid
graph TD
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
```' | node ${CLAUDE_PLUGIN_ROOT}/skills/diagram-expert/scripts/render-ascii.mjs
```""",
    3: """```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[Alternative]
    C --> E[End]
    D --> E
```""",
    4: """Use mcp__claude_ai_Mermaid_Chart__validate_and_render_mermaid_diagram tool with:

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[Alternative]
    C --> E[End]
    D --> E
```""",
    5: """Write a Python script that generates native SVG:

```python
#!/usr/bin/env python3
from pathlib import Path
elements = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rect(x, y, w, h, fill, stroke, rx=10):
    elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

def text(x, y, label, size=13, bold=False, color="#1e1e1e"):
    wt = "bold" if bold else "normal"
    elements.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{wt}" fill="{color}" text-anchor="middle" dominant-baseline="middle">{esc(label)}</text>')

# Add layers: rect() for containers, text() for labels
# See native-svg-guide.md for the full layered template

W, H = 1100, 400
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/>{"".join(elements)}</svg>'
out = Path(__file__).parent / "diagram.svg"
out.write_text(svg)
```

Run: `python3 docs/diagrams/gen-diagram.py`""",
    6: """```plantuml
@startuml
!include <awslib/AWSCommon>
!include <awslib/Compute/EC2>
!include <awslib/Database/RDS>

EC2(web, "Web Server", "t3.large")
RDS(db, "Database", "PostgreSQL")

web --> db
@enduml
```

Render: `plantuml -tsvg input.puml`""",
    7: """```dot
digraph G {
    rankdir=LR
    node [shape=box, style=rounded]
    A -> B -> C
    B -> D
    D -> E
}
```

Render: `dot -Tsvg input.dot -o output.svg`""",
    8: """{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": [{"x": "A", "y": 28}, {"x": "B", "y": 55}]},
  "mark": "bar",
  "encoding": {
    "x": {"field": "x", "type": "nominal"},
    "y": {"field": "y", "type": "quantitative"}
  }
}

Render: `vl2svg -i spec.vl.json -o chart.svg`""",
    9: """Use Kroki with the appropriate diagram type:

```bash
kroki convert input.ext -t svg -o output.svg
```

Supported types: bytefield, wavedrom, dbml, nomnoml, pikchr, and 20+ more.""",
}


def recommend_tier(description: str) -> int:
    desc_lower = description.lower()

    # Score each tier by keyword matches
    scores = {}
    for tier, info in TIERS.items():
        score = sum(1 for kw in info["keywords"] if kw in desc_lower)
        scores[tier] = score

    # Find best match
    best_tier = max(scores, key=scores.get)

    # Default to tier 3 (mermaid fenced) if no strong match
    if scores[best_tier] == 0:
        best_tier = 3

    return best_tier


def main():
    if len(sys.argv) < 2:
        print("Usage: select-tier.py <description>", file=sys.stderr)
        print('Example: select-tier.py "simple login flow with 3 steps"', file=sys.stderr)
        sys.exit(1)

    description = " ".join(sys.argv[1:])
    tier = recommend_tier(description)
    info = TIERS[tier]

    print(f"Recommended Tier: {tier} — {info['name']}")
    print()
    print("Starter Template:")
    print()
    print(TEMPLATES[tier])


if __name__ == "__main__":
    main()
