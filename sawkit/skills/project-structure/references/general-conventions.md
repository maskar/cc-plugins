# General Project Conventions

## Universal Directory Structure

These directories are language-agnostic and apply to all projects:

| Directory       | Purpose                                  |
|----------------|------------------------------------------|
| `.claude/`      | Claude Code configuration                |
| `docs/`         | Documentation                            |
| `scripts/`      | Operational/utility scripts              |
| `tmp/`          | Intermediary files (gitignored)          |

## .claude/ Directory

```text
.claude/
└── CLAUDE.md          # Project context for Claude Code
```

The `CLAUDE.md` file should contain:
- Project purpose and overview
- Key conventions and decisions
- Build/run/test commands
- Important file locations
- Team conventions

## Config Files at Root

Configuration files live at project root:

| File              | Tool/Purpose           |
|-------------------|------------------------|
| `.gitignore`      | Git ignore patterns    |
| `justfile`        | Task runner            |
| `pyproject.toml`  | Python config          |
| `package.json`    | Node config            |
| `go.mod`          | Go module              |
| `Cargo.toml`      | Rust config            |
| `.env.example`    | Environment template   |
| `Dockerfile`      | Container build        |

## .gitignore Essentials

Every `.gitignore` must include:

```text
# Intermediary files
tmp/

# OS
.DS_Store
Thumbs.db

# Editor
*.swp
*.swo
*~
.idea/
.vscode/

# Environment
.env
.env.local
```

Language-specific patterns are added on top. Use templates from:
- `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/templates/gitignore-python.txt`
- `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/templates/gitignore-node.txt`

## README Structure

Every project needs a README.md with at minimum:

1. Project name and one-line description
2. How to install/set up
3. How to run
4. How to test

## CI/CD

Common CI/CD patterns:

```text
.github/
└── workflows/
    ├── ci.yml          # Lint + test on PR
    └── deploy.yml      # Deploy on merge to main
```

Or for GitLab: `.gitlab-ci.yml` at root.

## Flat vs Nested

**Flat** (< 10 source files):

```text
project/
├── main.py
├── config.py
├── utils.py
└── tests/
    └── test_main.py
```

**Nested** (10+ source files):

```text
project/
├── src/
│   └── project_name/
│       ├── auth/
│       ├── api/
│       └── models/
└── tests/
    ├── auth/
    ├── api/
    └── models/
```

## Naming Conventions

| Item              | Convention         | Example              |
|-------------------|--------------------|----------------------|
| Directories       | kebab-case         | `my-feature/`        |
| Python files      | snake_case         | `my_module.py`       |
| TypeScript files  | camelCase or kebab | `myModule.ts`        |
| Go files          | snake_case         | `my_handler.go`      |
| Config files      | lowercase          | `pyproject.toml`     |
| Environment files | UPPER_SNAKE        | `.env`               |
