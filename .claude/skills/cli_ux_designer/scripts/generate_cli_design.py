#!/usr/bin/env python3
"""
CLI UX Design Generator Script

This script helps generate CLI UX designs
following the required format for the cli_ux_designer skill.
"""

import argparse
import sys
from datetime import datetime


def create_cli_design_template():
    """Create a template for CLI UX designs."""
    template = f"""# CLI UX Design Specification

## 1️⃣ CLI Command Structure
Describe the main command and all subcommands.

Example format:
- app <command> [options]

---

## 2️⃣ Commands & Arguments

### Command: <command-name>
- Description: [Clear, concise description of what the command does]
- Required Arguments: [List of required parameters]
- Optional Flags: [List of optional parameters with defaults]
- Example Usage: [Practical example of how to use the command]

[Repeat for each command]

---

## 3️⃣ Help & Discoverability
Define:
- Global help output: [What users see with --help or -h]
- Command-level help text: [What users see with <command> --help]
- Error hints for incorrect usage: [How the CLI helps users recover from mistakes]

---

## 4️⃣ Output Formatting Rules
Describe how output should appear:
- Lists: [How multiple items are displayed]
- Single items: [How individual items are presented]
- Status indicators: [How progress or states are shown]
- Empty results: [How the CLI handles no results]

Include formatting conventions (symbols, alignment, clarity).

---

## 5️⃣ Error Message UX Guidelines
Define:
- Tone: [Clear, neutral, actionable language guidelines]
- Structure: [What information appears in error messages]
- Consistency rules: [Standards for error message format]

---

## 6️⃣ UX Principles Applied
Briefly explain the usability principles guiding this design
(e.g., clarity, minimal typing, predictability).

---
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template


def main():
    parser = argparse.ArgumentParser(description='Generate CLI UX design template')
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('--app-name', '-a', type=str, help='Application name to use as base command')

    args = parser.parse_args()

    cli_design_content = create_cli_design_template()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(cli_design_content)
        print(f"CLI UX design template written to {args.output}")
    else:
        print(cli_design_content)


if __name__ == "__main__":
    main()