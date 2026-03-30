# Python Project Layout

## Standard Layout

```text
project-name/
├── .claude/
│   └── CLAUDE.md
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── cli.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── docs/
├── scripts/
├── tmp/                    # gitignored
├── .gitignore
├── .python-version
├── justfile
├── pyproject.toml
└── README.md
```

## Package Management

Use `uv` for all Python package management:

```bash
uv init                    # Initialize project
uv add <package>           # Add dependency
uv add --dev <package>     # Add dev dependency
uv run <command>           # Run in virtual environment
uv sync                    # Sync dependencies
```

## pyproject.toml

Single source of truth for all project configuration:

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Brief description"
requires-python = ">=3.13"
dependencies = []

[project.scripts]
project-name = "project_name.cli:main"

[tool.ruff]
line-length = 120
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

## Linting

Use `ruff` exclusively (not pylint, flake8, black, autopep8, isort):

```bash
ruff check .         # Lint
ruff check --fix .   # Auto-fix
ruff format .        # Format
```

## CLI Pattern

Use `pyproject.toml` scripts entry point or a direct script:

```python
#!/usr/bin/env python3
"""CLI entry point."""
from project_name.core import main

if __name__ == "__main__":
    main()
```

Never use `pip install -e .` — use `uv run` instead.

## justfile

```just
# Run the project
run *ARGS:
    uv run project-name {{ARGS}}

# Lint
lint:
    ruff check . && ruff format --check .

# Format
fmt:
    ruff check --fix . && ruff format .

# Test
test *ARGS:
    uv run pytest {{ARGS}}
```

## Conventions

- Python >= 3.13
- Use `pathlib.Path` over `os.path`
- Use `loguru` for logging
- Use `pydantic` for config/models
- Use `httpx` for HTTP requests
- Use `orjson` for JSON
- Use `typer` for CLI
