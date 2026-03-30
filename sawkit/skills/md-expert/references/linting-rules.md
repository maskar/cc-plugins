# Linting Rules Reference

## markdownlint-cli2 (Structure)

Universal rules — apply to all projects without modification.

### Critical Rules (always enforce)

| Rule  | Name                       | What It Checks                        |
|-------|----------------------------|---------------------------------------|
| MD001 | heading-increment          | Heading levels increment by one       |
| MD003 | heading-style              | ATX-style headings (`#`)              |
| MD009 | no-trailing-spaces         | No trailing whitespace                |
| MD010 | no-hard-tabs               | No tab characters                     |
| MD012 | no-multiple-blanks         | No consecutive blank lines            |
| MD018 | no-missing-space-atx       | Space after `#` in headings           |
| MD022 | blanks-around-headings     | Blank lines around headings           |
| MD023 | heading-start-left         | Headings start at beginning of line   |
| MD025 | single-title               | Single H1 per document                |
| MD031 | blanks-around-fences       | Blank lines around fenced code blocks |
| MD032 | blanks-around-lists        | Blank lines around lists              |
| MD034 | no-bare-urls               | No bare URLs in prose                 |
| MD037 | no-space-in-emphasis       | No spaces inside emphasis markers     |
| MD040 | fenced-code-language       | Language specified on code blocks     |
| MD047 | single-trailing-newline    | File ends with single newline         |
| MD049 | emphasis-style             | Consistent emphasis style (`*`)       |
| MD050 | strong-style               | Consistent strong style (`**`)        |

### Commonly Relaxed Rules

These rules may be disabled depending on project needs. The defaults above are strict.

| Rule  | Why Sometimes Disabled                                   |
|-------|----------------------------------------------------------|
| MD007 | Projects using 4-space indent for nested lists           |
| MD013 | Line length limits hurt readability in documentation     |
| MD024 | Duplicate headings are natural in structured docs        |
| MD033 | Inline HTML needed for badges, details/summary, etc.     |
| MD051 | Cross-file anchor links can't be validated locally       |

### Running

```bash
# Lint all markdown files
markdownlint-cli2 "**/*.md"

# Lint specific file
markdownlint-cli2 README.md

# Fix auto-fixable issues
markdownlint-cli2 --fix "**/*.md"
```

## vale (Prose Quality)

vale catches writing quality issues that markdownlint ignores: passive voice, weasel words, jargon, readability.

### Style Packages

| Package       | Focus                                 |
|---------------|---------------------------------------|
| `Microsoft`   | Clear, professional technical writing |
| `Google`      | Developer documentation style         |
| `write-good`  | Plain English, no weasel words        |
| `Readability` | Flesch-Kincaid, grade level scoring   |

### Configuration (.vale.ini)

```ini
StylesPath = styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Vale, Microsoft
```

### Running

```bash
# Lint a file
vale file.md

# Lint a directory
vale docs/

# Show specific alert levels
vale --minAlertLevel error file.md
```

## mdformat (Auto-Formatting)

Opinionated auto-formatter — like `ruff format` for markdown. Normalizes style without configuration.

### Plugins

| Plugin              | What It Formats                     |
|---------------------|-------------------------------------|
| `mdformat-gfm`      | GFM extensions (task lists, tables) |
| `mdformat-tables`   | Table column alignment              |
| `mdformat-footnote` | Footnote syntax                     |

### Running

```bash
# Format in place
mdformat file.md

# Check only (no changes)
mdformat --check file.md

# Format all markdown
mdformat .
```

## Workflow

Run tools in this order:

1. `mdformat file.md` — auto-fix formatting
2. `markdownlint-cli2 file.md` — catch remaining structural issues
3. `vale file.md` — check prose quality
4. `lychee file.md` — validate links (last, since it hits network)
