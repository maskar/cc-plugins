# cc-plugins

Claude Code plugin marketplace repository.

## Structure

```text
cc-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace registry (lists all plugins)
└── <plugin-name>/
    ├── .claude-plugin/
    │   └── plugin.json        # Plugin metadata
    ├── README.md
    └── skills/
        └── <skill-name>/
            ├── SKILL.md       # Skill definition with frontmatter
            ├── references/    # Reference documents
            └── scripts/       # Helper scripts
```

## Adding a Plugin

1. Create the plugin directory at repo root
2. Add `.claude-plugin/plugin.json` with name, version, description, author
3. Add skills under `skills/<skill-name>/SKILL.md`
4. Register in `.claude-plugin/marketplace.json` under the `plugins` array
5. Update root `README.md` plugins table

## Marketplace Usage

```text
/plugin marketplace add Maskar/cc-plugins
/plugin install <plugin-name>@Maskar
```

## Conventions

- Each plugin is self-contained in its own directory
- Skills auto-trigger based on their `description` field in SKILL.md frontmatter
- Temporary files go in `./tmp/` (gitignored)
- No Python tooling — this is a docs/config-only repository
