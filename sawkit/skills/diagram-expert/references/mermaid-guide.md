# Mermaid Syntax Guide

## Flowchart

```mermaid
flowchart TD
    A[Rectangle] --> B{Diamond / Decision}
    B -->|Yes| C[Process]
    B -->|No| D[Other Process]
    C --> E((Circle))
    D --> E
    E --> F([Stadium])
    F --> G[[Subroutine]]
```

**Direction:** `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left)

**Node shapes:**

| Syntax     | Shape              |
|------------|--------------------|
| `[text]`   | Rectangle          |
| `(text)`   | Rounded rectangle  |
| `{text}`   | Diamond (decision) |
| `((text))` | Circle             |
| `([text])` | Stadium            |
| `[[text]]` | Subroutine         |
| `[(text)]` | Cylinder           |
| `>text]`   | Asymmetric         |
| `{{text}}` | Hexagon            |

**Edge styles:**

| Syntax      | Style               |
|-------------|---------------------|
| `-->`       | Solid arrow         |
| `---`       | Solid line          |
| `-.->`       | Dotted arrow        |
| `==>`       | Thick arrow         |
| `--text-->` | Arrow with label    |

## Styling Nodes

Use `style` to override individual node appearance:

```mermaid
flowchart TD
    A[Default] --> B[Success]
    A --> C[Error]
    style B fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style C fill:#ffebee,stroke:#f44336,color:#b71c1c
```

Use `classDef` + `:::` for reusable styles across multiple nodes:

```mermaid
flowchart TD
    classDef success fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    classDef danger fill:#ffebee,stroke:#f44336,color:#b71c1c
    classDef warning fill:#fff8e1,stroke:#ff8f00,color:#e65100
    classDef info fill:#e3f2fd,stroke:#1976d2,color:#0d47a1
    classDef muted fill:#f5f5f5,stroke:#9e9e9e,color:#424242

    A[OK]:::success --> B[Failed]:::danger
    A --> C[Warning]:::warning
    A --> D[Info]:::info
    A --> E[Disabled]:::muted
```

### Dark Mode Safety

**Always pin `color:` when using custom `fill:`.** Mermaid renderers in dark mode may flip text to white, making it invisible on light-colored fills.

```text
BAD:  style X fill:#e8f5e9,stroke:#4caf50
GOOD: style X fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
```

**Recommended palette** (light fills with dark text, readable in both modes):

| Purpose  | Fill      | Stroke    | Color (text) |
|----------|-----------|-----------|-------------|
| Success  | `#e8f5e9` | `#4caf50` | `#1b5e20`   |
| Danger   | `#ffebee` | `#f44336` | `#b71c1c`   |
| Warning  | `#fff8e1` | `#ff8f00` | `#e65100`   |
| Info     | `#e3f2fd` | `#1976d2` | `#0d47a1`   |
| Muted    | `#f5f5f5` | `#9e9e9e` | `#424242`   |
| Purple   | `#f3e5f5` | `#9c27b0` | `#4a148c`   |

## Sequence Diagram

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    participant S as Server

    A->>B: Hello
    B->>S: Forward message
    S-->>B: Acknowledgment
    B-->>A: Message delivered

    alt Success
        A->>B: Thanks!
    else Failure
        A->>B: Retry?
    end

    loop Every 5s
        S->>S: Health check
    end

    note over A,B: This is a note
```

**Arrow types:**

| Syntax | Meaning              |
|--------|----------------------|
| `->>`  | Solid with arrow     |
| `-->>` | Dotted with arrow    |
| `->`   | Solid without arrow  |
| `-->`  | Dotted without arrow |
| `-x`   | Solid with cross     |
| `--x`  | Dotted with cross    |

## Entity Relationship

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string name
        string email UK
    }
    ORDER ||--|{ LINE_ITEM : contains
    ORDER {
        int id PK
        int user_id FK
        decimal total
    }
```

**Relationship types:**

| Syntax | Meaning      |
|--------|--------------|
| `\|\|` | Exactly one  |
| `o{`   | Zero or more |
| `\|{`  | One or more  |
| `o\|`  | Zero or one  |

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Success : complete
    Processing --> Error : fail
    Error --> Idle : reset
    Success --> [*]
```

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +fetch() void
    }
    Animal <|-- Dog
```

**Relationships:**

| Syntax  | Meaning     |
|---------|-------------|
| `<\|--` | Inheritance |
| `*--`   | Composition |
| `o--`   | Aggregation |
| `-->`   | Association |
| `..>`   | Dependency  |

## Mind Map

```mermaid
mindmap
    root((Project))
        Frontend
            React
            TypeScript
        Backend
            Python
            FastAPI
        Database
            PostgreSQL
            Redis
```

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
        Design     :done,    p1, 2026-01-01, 14d
        Prototype  :active,  p2, after p1, 10d
    section Phase 2
        Build      :         p3, after p2, 21d
        Test       :         p4, after p3, 14d
```

## Pie Chart

```mermaid
pie title Distribution
    "Category A" : 45
    "Category B" : 30
    "Category C" : 25
```

## C4 Diagram

Model software architecture using the C4 standard (Context, Container, Component):

```mermaid
C4Context
    title System Context Diagram

    Person(user, "User", "A customer of the system")
    System(webapp, "Web Application", "Delivers the web frontend")
    System_Ext(email, "Email System", "Sends emails")
    SystemDb(db, "Database", "Stores user data")

    Rel(user, webapp, "Uses", "HTTPS")
    Rel(webapp, email, "Sends emails", "SMTP")
    Rel(webapp, db, "Reads/writes", "SQL")
```

**C4 diagram types:** `C4Context`, `C4Container`, `C4Component`, `C4Deployment`

**C4 elements:**

| Function         | Description              |
|------------------|--------------------------|
| `Person`         | Human user               |
| `System`         | Internal system          |
| `System_Ext`     | External system          |
| `SystemDb`       | Database system          |
| `Container`      | App/service in a system  |
| `Component`      | Component in a container |
| `Rel`            | Relationship             |
| `Boundary`       | Grouping boundary        |

## Git Graph

Visualize branching strategies and merge history:

```mermaid
gitgraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    branch feature
    checkout feature
    commit
    checkout develop
    merge feature
    checkout main
    merge develop
```

**Options:** `commit id:"msg"`, `commit tag:"v1.0"`, `commit type: HIGHLIGHT`

**Commit types:** `NORMAL`, `REVERSE`, `HIGHLIGHT`

## Timeline

Show events along a time axis:

```mermaid
timeline
    title Project Milestones
    section Q1
        January : Design phase
                : Requirements gathered
        March : Prototype complete
    section Q2
        April : Alpha release
        June : Beta release
    section Q3
        July : GA release
```

## Quadrant Chart

Priority/effort matrices and 2x2 analysis:

```mermaid
quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    Campaign A: [0.3, 0.6]
    Campaign B: [0.45, 0.23]
    Campaign C: [0.57, 0.69]
    Campaign D: [0.78, 0.34]
    Campaign E: [0.40, 0.34]
    Campaign F: [0.35, 0.78]
```

## XY Chart

Data visualization with bar and line marks:

```mermaid
xychart-beta
    title "Revenue vs Expenses"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "Amount (USD)" 0 --> 10000
    bar [5000, 6000, 7500, 8200, 9500, 10500]
    line [4200, 5300, 6100, 7400, 8100, 9200]
```

## Sankey Diagram

Visualize flow quantities between nodes:

```mermaid
sankey-beta
    Source A,Target X,5
    Source A,Target Y,3
    Source B,Target X,2
    Source B,Target Z,4
    Target X,Final,7
    Target Y,Final,3
```

Format: `source,target,value` — one flow per line. Useful for budget flows, data pipelines, energy diagrams.

## Subgraphs and Nesting

Group nodes into named containers:

```mermaid
flowchart TD
    subgraph Frontend["Frontend Layer"]
        direction LR
        A[React App] --> B[Router]
    end

    subgraph Backend["Backend Layer"]
        direction LR
        C[API Server] --> D[Auth]
        C --> E[Workers]
    end

    subgraph Data["Data Layer"]
        F[(PostgreSQL)]
        G[(Redis)]
    end

    Frontend --> Backend
    Backend --> Data

    style Frontend fill:#e7f5ff,stroke:#1971c2
    style Backend fill:#d8f5e0,stroke:#2f9e44
    style Data fill:#f8f9fa,stroke:#495057
```

**Notes:**
- `direction` inside subgraphs works in `flowchart` but can be unreliable — test first
- Subgraph-to-subgraph edges (e.g., `Frontend --> Backend`) work and are cleaner than individual node edges
- Style subgraphs with `style SubgraphId fill:...,stroke:...`

## Theming and Init Directives

Control diagram appearance with `init` frontmatter:

```mermaid
---
config:
  theme: neutral
  themeVariables:
    primaryColor: "#d0ebff"
    primaryTextColor: "#1e1e1e"
    primaryBorderColor: "#1971c2"
    lineColor: "#868e96"
    secondaryColor: "#d8f5e0"
    tertiaryColor: "#f3f0ff"
    fontSize: "14px"
---
flowchart TD
    A[Start] --> B[End]
```

**Built-in themes:** `default`, `neutral`, `dark`, `forest`, `base`

**Key theme variables:**

| Variable              | Controls                        |
|-----------------------|---------------------------------|
| `primaryColor`        | Main node fill                  |
| `primaryTextColor`    | Main node text                  |
| `primaryBorderColor`  | Main node border                |
| `lineColor`           | Arrows and edges                |
| `secondaryColor`      | Secondary node fill             |
| `tertiaryColor`       | Tertiary node fill              |
| `fontSize`            | Global font size                |
| `fontFamily`          | Global font (quote if spaces)   |

## Common Pitfalls

1. **Special characters in labels** — Wrap in quotes: `A["Node with (parens)"]`. Unquoted parens/brackets break parsing.
2. **`direction LR` inside subgraphs** — Unreliable in `flowchart`. Use `block-beta` for grid layouts instead.
3. **Dark mode text** — Always pin `color:` when overriding `fill:`. See Dark Mode Safety above.
4. **Long labels truncate** — Mermaid clips text that overflows node boxes. Keep labels concise or use `<br/>` for line breaks: `A["Line one<br/>Line two"]`.
5. **Mermaid Chart MCP adds `<style>` tags** — The MCP tool may prepend CSS before `<svg>`. Strip the `<style>...</style>` block before using the raw SVG.
6. **Node ID collisions** — IDs like `end`, `start`, `class`, `style` are reserved words. Prefix them: `nodeEnd`, `stepStart`.
7. **Colon in labels** — Colons can be misinterpreted. Use quotes: `A["Key: Value"]`.
8. **Empty subgraphs** — A subgraph with no nodes causes a parse error. Always include at least one node.
