# Document Structure Reference

## Standard Section Ordering

For technical documentation, follow this section order:

1. **Title** (H1) — one per document
2. **Overview** — 1-3 sentences explaining purpose
3. **Table of Contents** — auto-generated for documents with 4+ sections
4. **Prerequisites / Requirements** — what the reader needs before starting
5. **Main Content** (H2 sections) — the core information
6. **Examples / Usage** — practical demonstrations
7. **Troubleshooting** — common issues and solutions
8. **Reference / API** — detailed specifications
9. **Changelog / History** — if applicable

Not every document needs all sections. Use what fits.

## Heading Hierarchy

```text
# Document Title (H1) — exactly one
## Major Section (H2) — primary divisions
### Subsection (H3) — subdivisions of H2
#### Detail (H4) — rarely needed, signals too much nesting
```

Rules:

- Never skip levels: H2 → H4 is wrong
- If you need H5+, the document structure is too deep — restructure
- Use H2 for top-level sections, H3 for subsections
- Heading text should be concise and scannable

## Table of Contents

Use `doctoc` to auto-generate and maintain TOC:

```bash
doctoc file.md --github --maxlevel 3
```

This inserts a TOC between markers:

```markdown
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Section One](#section-one)
- [Section Two](#section-two)
  - [Subsection](#subsection)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
```

Add TOC when a document has 4 or more H2 sections.

## Frontmatter

Use YAML frontmatter for metadata when needed:

```yaml
---
title: Document Title
description: Brief description
date: 2026-03-27
---
```

Frontmatter is optional. Use it for:

- Static site generators (MkDocs, Docusaurus)
- Document metadata (author, date, status)
- Tool configuration

## README Structure

Every repository README should follow this template:

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature one
- Feature two

## Installation

Instructions to install.

## Usage

How to use after installation.

## Configuration

Configuration options, if any.

## Contributing

How to contribute, if open source.

## License

License information.
```

## Link Conventions

### Internal Links (within repo)

Use relative paths:

```markdown
See [configuration](docs/config.md) for details.
See [the API section](docs/api.md#authentication) for auth info.
```

### External Links

Use reference-style when a URL appears more than once:

```markdown
Read the [CommonMark spec][commonmark] for details.
The [GFM extensions][gfm] add tables and task lists.

[commonmark]: https://spec.commonmark.org/
[gfm]: https://github.github.com/gfm/
```

### Link Validation

Run `lychee` to check all links:

```bash
lychee file.md           # single file
lychee .                 # all files
lychee --format json .   # JSON output for programmatic use
```
