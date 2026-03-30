# sawkit

Generic reusable skills for Claude Code — markdown authoring, diagram generation, and project structure.

## Skills

| Skill               | Purpose                                                     | Slash Command              |
|---------------------|-------------------------------------------------------------|----------------------------|
| **md-expert**       | Markdown authoring, formatting, linting, tables, TOC, links | `/sawkit:md-expert`        |
| **diagram-expert**  | Diagram generation, tier ladder, tool selection, rendering   | `/sawkit:diagram-expert`   |
| **project-structure** | Repo scaffolding, file organization, all project types     | `/sawkit:project-structure` |

## Installation

### From GitHub

Inside a Claude Code session:

```text
/plugin marketplace add Maskar/cc-plugins
/plugin install sawkit@Maskar
```

### From local path

```text
/plugin marketplace add /path/to/cc-plugins
/plugin install sawkit@Maskar
```

### Development (single session)

```bash
claude --plugin-dir /path/to/sawkit
```

## Skill Details

### md-expert

Ensures high-quality markdown authoring following universal CommonMark/GFM standards. Auto-triggers when writing or editing `.md` files.

- Space-aligned tables
- Heading hierarchy enforcement
- Fenced code block language tags
- Tools: markdownlint-cli2, vale, mdformat, doctoc, lychee

### diagram-expert

Actively generates diagrams using the right tool for the right complexity level. Auto-triggers when creating diagrams or visualizing architecture.

Tier ladder (simplest first):
1. Unicode/ASCII inline
2. beautiful-mermaid ASCII
3. Mermaid fenced blocks (GitHub-native)
4. Mermaid Chart MCP
5. PlantUML
6. Graphviz/D2
7. Vega-Lite
8. Kroki

### project-structure

Scaffolds and organizes repositories following language-specific best practices. Auto-triggers when scaffolding projects or discussing file organization.

- Uses `./tmp/` for intermediary files (gitignored)
- `CLAUDE.md` at `.claude/CLAUDE.md`
- Supports: Python, Node/TypeScript, Go, Rust, Shell/Infra, mixed
