# cc-plugins

Claude Code plugin marketplace by [maskar](https://github.com/maskar). A collection of generic, reusable skills and extensions.

## Plugins

| Plugin     | Description                                                          |
|------------|----------------------------------------------------------------------|
| **sawkit** | Markdown authoring, diagram generation, and project structure skills |

## Installation

### 1. Add the marketplace

Inside a Claude Code session, register this repository as a plugin marketplace:

```text
/plugin marketplace add maskar/cc-plugins
```

### 2. Install a plugin

```text
/plugin install sawkit@maskar
```

### Local development

To use a local clone instead of the GitHub repository:

```text
/plugin marketplace add /path/to/cc-plugins
```

To load a plugin for a single session without installing:

```bash
claude --plugin-dir /path/to/cc-plugins/sawkit
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

## Adding a New Plugin

1. Create a directory at the repo root (e.g. `myplugin/`)
2. Add the plugin structure:

   ```text
   myplugin/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── README.md
   └── skills/
       └── skill-name/
           ├── SKILL.md
           ├── references/
           └── scripts/
   ```

3. Register the plugin in `.claude-plugin/marketplace.json`:

   ```json
   {
     "name": "myplugin",
     "source": "./myplugin",
     "description": "Brief description",
     "version": "0.1.0",
     "author": { "name": "Your Name" },
     "keywords": ["tag1", "tag2"]
   }
   ```

4. Commit and push
