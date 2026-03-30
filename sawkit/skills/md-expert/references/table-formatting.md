# Table Formatting Reference

## Pipe Tables (GFM Standard)

Always align columns with spaces for readability:

### Correct

| Name    | Age | Role      |
|---------|----:|-----------|
| Alice   |  30 | Engineer  |
| Bob     |  25 | Designer  |
| Charlie |  35 | Manager   |

### Incorrect (unaligned)

|Name|Age|Role|
|---|---|---|
|Alice|30|Engineer|

## Alignment

Use colons in the separator row:

| Syntax  | Result        |
|---------|---------------|
| `---`   | Left-aligned  |
| `:---`  | Left-aligned  |
| `---:`  | Right-aligned |
| `:---:` | Centered      |

Right-align numeric columns. Left-align text. Center short labels.

## Auto-Formatting with format-tables.py

Run the script to auto-fix table alignment in any markdown file:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/md-expert/scripts/format-tables.py input.md
```

The script:

- Reads the file
- Finds all pipe tables
- Re-aligns columns with proper spacing
- Preserves alignment indicators (`:`)
- Writes the result to stdout (pipe to file or use `--in-place`)

## Generating Tables from Data with tabulate

When generating tables from structured data, use Python's `tabulate` library:

```python
from tabulate import tabulate

data = [
    ["Alice", 30, "Engineer"],
    ["Bob", 25, "Designer"],
]
headers = ["Name", "Age", "Role"]

# GFM pipe table (for markdown files)
print(tabulate(data, headers=headers, tablefmt="github"))

# ASCII grid table (for terminal output)
print(tabulate(data, headers=headers, tablefmt="grid"))

# Unicode fancy grid (for styled terminal output)
print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
```

### Output Formats

| Format       | Use Case                  | Example Border |
|--------------|---------------------------|----------------|
| `github`     | Markdown files            | `\| --- \|`   |
| `grid`       | Terminal, plain text      | `+-----+`      |
| `fancy_grid` | Styled terminal           | `╒═════╕`      |
| `pipe`       | Markdown (org-mode style) | `\| --- \|`   |
| `simple`     | Minimal, clean            | `------`       |

## Rules

1. Never leave tables unaligned — always pad with spaces
2. Header separator must match column width
3. Minimum 3 dashes in separator cells (`---`)
4. One space padding inside each cell
5. Keep tables under ~120 characters wide — split wide tables or use lists instead
