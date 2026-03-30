---
name: project-structure
description: >-
  This skill should be used when the user is scaffolding a new project, reorganizing
  file structure, or discussing directory layout conventions. It provides
  language-specific best practices for Python, Node/TypeScript, Go, and general
  projects. Enforces the ./tmp/ intermediary workflow and .claude/CLAUDE.md
  convention. Triggers on: project init, directory layout, file organization,
  scaffolding, repo structure, creating new projects, setting up a Python/Node/Go
  project, or organizing code. Also available as /sawkit:project-structure.
argument-hint: "[language/framework] or describe your project"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Project Structure Expert

Follow these conventions when scaffolding or organizing any project.

## Intermediary Workflow

All intermediary scripts, debug files, and work-in-progress files go in `./tmp/` at the project root. This directory is always gitignored.

**Rules:**
- Create `./tmp/` at project root for all temporary work
- Write analysis scripts, test data, debug output to `./tmp/`
- Only move files to their final project location after user approval
- Never commit `./tmp/` contents
- Add `tmp/` to `.gitignore` in every project

**Example workflow:**

```bash
# Write intermediary script
mkdir -p ./tmp
cat > ./tmp/analyze.py << 'EOF'
# analysis script...
EOF
python ./tmp/analyze.py

# After approval, move to final location
mv ./tmp/analyze.py scripts/analyze.py
```

## CLAUDE.md Location

Place `CLAUDE.md` at `.claude/CLAUDE.md`, not at project root.

```bash
mkdir -p .claude
# Write CLAUDE.md to .claude/CLAUDE.md
```

Use the template at `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/templates/claude-md-template.md` as a starter.

## Universal Files

Every project should include:

| File                  | Purpose                        |
|-----------------------|--------------------------------|
| `.gitignore`          | Git ignore patterns            |
| `README.md`           | Project overview and usage     |
| `.claude/CLAUDE.md`   | Claude Code project context    |

## Project Detection

Before suggesting structure, detect the project type from existing files:

| File Present         | Project Type    |
|----------------------|-----------------|
| `pyproject.toml`     | Python          |
| `setup.py`           | Python (legacy) |
| `.python-version`    | Python          |
| `package.json`       | Node/TypeScript |
| `tsconfig.json`      | TypeScript      |
| `go.mod`             | Go              |
| `Cargo.toml`         | Rust            |
| `justfile`           | Any (task runner)|
| `Makefile`           | Any (build)     |

If no files exist, ask the user what they are building.

## Language-Specific Layouts

For detailed layouts per language, read the reference files:

- Python: `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/references/python-layout.md`
- Node/TypeScript: `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/references/node-layout.md`
- Go: `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/references/go-layout.md`
- General: `${CLAUDE_PLUGIN_ROOT}/skills/project-structure/references/general-conventions.md`

## General Principles

1. **Flat for small projects** — do not create deep nesting for projects with < 10 files
2. **Group by feature, not by type** — `auth/models.py` + `auth/routes.py` over `models/auth.py` + `routes/auth.py`
3. **Config at root** — `pyproject.toml`, `package.json`, `go.mod` stay at project root
4. **Docs in `docs/`** — separate documentation from source code
5. **Scripts in `scripts/`** — operational scripts separate from source
6. **Tests mirror source** — `src/auth/login.py` → `tests/auth/test_login.py`
