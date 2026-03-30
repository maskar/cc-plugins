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
