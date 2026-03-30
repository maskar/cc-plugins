---
name: md-expert
description: >-
  This skill should be used when the user is writing, editing, or reviewing markdown files.
  It ensures high-quality markdown authoring following universal CommonMark and GitHub
  Flavored Markdown standards. Triggers on: creating .md files, writing READMEs,
  formatting tables, fixing markdown lint errors, structuring documents, generating TOCs,
  checking links, or fixing markdownlint warnings. Also available as /sawkit:md-expert.
argument-hint: "[file.md] or describe what you need help with"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Markdown Expert

Follow these rules when writing or editing any markdown file.

## Formatting Rules

Comply with CommonMark specification and GitHub Flavored Markdown (GFM) extensions. These are universal standards — do not apply project-specific overrides.

### Headings

- One H1 (`#`) per document — the document title
- Never skip heading levels (H2 → H4 is wrong, use H2 → H3)
- Blank line before and after every heading
- Use ATX-style headings (`#`), never Setext (underlines)

### Code Blocks

- Always specify a language identifier on fenced code blocks
- Common identifiers: `python`, `bash`, `json`, `yaml`, `sql`, `text`, `markdown`, `javascript`, `typescript`, `go`, `rust`, `html`, `css`, `toml`, `xml`, `diff`
- Use `text` for plain output that has no specific language
- Use `bash` for shell commands, not `sh` or `shell`

### Tables

- Always space-align columns for readability
- Use pipe tables (GFM standard)
- Align separator row dashes to match column width
- Right-align numeric columns with `:` in separator
- Run `${CLAUDE_PLUGIN_ROOT}/skills/md-expert/scripts/format-tables.py` to auto-fix table alignment
- For reference on table formatting patterns, read `${CLAUDE_PLUGIN_ROOT}/skills/md-expert/references/table-formatting.md`

### Spacing

- Blank line before and after: headings, lists, code blocks, tables, blockquotes
- No trailing whitespace on any line
- Single blank line between sections (never double)
- Files end with a single newline

### Links

- Prefer reference-style links when the same URL appears more than once
- Use relative paths for internal links within the same repository
- Use descriptive link text — never "click here" or bare URLs in prose

### Lists

- Use `-` for unordered lists (consistent, not mixed `*` and `-`)
- Use `1.` for all ordered list items (auto-numbering)
- Indent nested lists by 4 spaces

## Tools

Use these tools to validate and fix markdown quality:

| Tool                  | Command                           | Purpose           |
|-----------------------|-----------------------------------|-------------------|
| **markdownlint-cli2** | `markdownlint-cli2 "**/*.md"`   | Structure linting |
| **vale**              | `vale file.md`                    | Prose quality     |
| **mdformat**          | `mdformat file.md`               | Auto-formatting   |
| **doctoc**            | `doctoc file.md`                 | TOC generation    |
| **lychee**            | `lychee file.md`                 | Link validation   |

Run tools in this order: `mdformat` first to auto-fix formatting, then `markdownlint-cli2` for structural issues, then `vale` for prose quality. Use `lychee` last since it hits the network.

## Document Structure

Follow standard section ordering. For detailed guidance, read `${CLAUDE_PLUGIN_ROOT}/skills/md-expert/references/document-structure.md`.

1. Title (H1)
2. Brief description / overview
3. Table of contents (for documents with 4+ sections)
4. Main content sections (H2)
5. Examples / usage
6. Reference / appendix

## Linting

For the complete set of universal markdownlint rules and vale style configuration, read `${CLAUDE_PLUGIN_ROOT}/skills/md-expert/references/linting-rules.md`.

Key rules enforced:

- MD001: Heading levels increment by one
- MD003: ATX-style headings
- MD009: No trailing spaces
- MD012: No multiple consecutive blank lines
- MD022: Headings surrounded by blank lines
- MD031: Fenced code blocks surrounded by blank lines
- MD040: Fenced code blocks have a language identifier
- MD047: Files end with a single newline
