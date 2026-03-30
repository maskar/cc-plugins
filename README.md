# cc-plugins

Claude Code plugin marketplace by [Maskar](https://github.com/Maskar). A collection of generic, reusable skills and extensions.

## Plugins

| Plugin     | Description                                                          |
|------------|----------------------------------------------------------------------|
| **sawkit** | Markdown authoring, diagram generation, and project structure skills |

## Installation

Inside a Claude Code session:

```text
/plugin marketplace add Maskar/cc-plugins
```

Then install any plugin:

```text
/plugin install sawkit@Maskar
```

## Plugin Details

### sawkit

Generic toolkit with three auto-triggering skills:

| Skill                 | Purpose                                                     | Slash Command               |
|-----------------------|-------------------------------------------------------------|-----------------------------|
| **md-expert**         | Markdown authoring, formatting, linting, tables, TOC, links | `/sawkit:md-expert`         |
| **diagram-expert**    | Diagram generation, tier ladder, tool selection, rendering   | `/sawkit:diagram-expert`    |
| **project-structure** | Repo scaffolding, file organization, all project types      | `/sawkit:project-structure` |

See [sawkit/README.md](sawkit/README.md) for full details.
