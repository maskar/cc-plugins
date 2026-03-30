#!/usr/bin/env python3
"""Reformat pipe tables in markdown files with proper space alignment.

Usage:
    python format-tables.py input.md              # output to stdout
    python format-tables.py input.md --in-place   # modify file in place
"""

import re
import sys
from pathlib import Path


def parse_table(lines: list[str]) -> list[list[str]]:
    """Parse pipe table lines into a 2D list of cell contents."""
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        cells = [cell.strip() for cell in line.split("|")]
        rows.append(cells)
    return rows


def detect_alignments(separator_row: list[str]) -> list[str]:
    """Detect column alignments from separator row."""
    alignments = []
    for cell in separator_row:
        cell = cell.strip().strip("-")
        if cell.startswith(":") and cell.endswith(":"):
            alignments.append("center")
        elif cell.endswith(":"):
            alignments.append("right")
        else:
            alignments.append("left")
    return alignments


def format_table(lines: list[str]) -> str:
    """Format a pipe table with proper alignment."""
    rows = parse_table(lines)
    if len(rows) < 2:
        return "\n".join(lines)

    header = rows[0]
    separator = rows[1]
    body = rows[2:]
    alignments = detect_alignments(separator)
    num_cols = len(header)

    # Calculate column widths
    col_widths = [0] * num_cols
    for row in [header] + body:
        for i, cell in enumerate(row):
            if i < num_cols:
                col_widths[i] = max(col_widths[i], len(cell))

    # Minimum width of 3 for separator dashes
    col_widths = [max(w, 3) for w in col_widths]

    def pad_cell(text: str, width: int, align: str) -> str:
        if align == "right":
            return text.rjust(width)
        elif align == "center":
            return text.center(width)
        return text.ljust(width)

    def format_separator(widths: list[int], aligns: list[str]) -> str:
        cells = []
        for w, a in zip(widths, aligns):
            if a == "center":
                cells.append(":" + "-" * (w - 2) + ":")
            elif a == "right":
                cells.append("-" * (w - 1) + ":")
            else:
                cells.append("-" * w)
        return "| " + " | ".join(cells) + " |"

    def format_row(row: list[str], widths: list[int], aligns: list[str]) -> str:
        cells = []
        for i in range(num_cols):
            text = row[i] if i < len(row) else ""
            cells.append(pad_cell(text, widths[i], aligns[i]))
        return "| " + " | ".join(cells) + " |"

    result = []
    result.append(format_row(header, col_widths, alignments))
    result.append(format_separator(col_widths, alignments))
    for row in body:
        result.append(format_row(row, col_widths, alignments))

    return "\n".join(result)


def process_markdown(content: str) -> str:
    """Find and reformat all pipe tables in markdown content."""
    lines = content.split("\n")
    result = []
    table_lines = []
    in_table = False
    in_code_block = False

    for line in lines:
        # Track code blocks to skip tables inside them
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            if in_table:
                result.append(format_table(table_lines))
                table_lines = []
                in_table = False
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        is_table_line = bool(re.match(r"\s*\|", line))

        if is_table_line:
            table_lines.append(line)
            in_table = True
        else:
            if in_table:
                result.append(format_table(table_lines))
                table_lines = []
                in_table = False
            result.append(line)

    if in_table:
        result.append(format_table(table_lines))

    return "\n".join(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: format-tables.py <file.md> [--in-place]", file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    in_place = "--in-place" in sys.argv

    if not filepath.exists():
        print(f"Error: {filepath} not found", file=sys.stderr)
        sys.exit(1)

    content = filepath.read_text()
    formatted = process_markdown(content)

    if in_place:
        filepath.write_text(formatted)
        print(f"Formatted tables in {filepath}", file=sys.stderr)
    else:
        print(formatted)


if __name__ == "__main__":
    main()
