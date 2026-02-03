#!/usr/bin/env python3
"""
Software Specification Generator Script

This script helps generate software specifications
following the required format for the spec_writer skill.
"""

import argparse
import sys
from datetime import datetime


def create_specification_template():
    """Create a template for software specifications."""
    template = f"""# Software Specification

## 1️⃣ Overview
Brief description of the problem being solved and the goal of the system.

---

## 2️⃣ In-Scope Features
List all features that MUST be implemented.

Each feature should be described in clear, testable language.

---

## 3️⃣ Out-of-Scope
Explicitly list what is NOT included to prevent scope creep.

---

## 4️⃣ Functional Requirements
Numbered, precise requirements describing system behavior.

Example:
- The system SHALL allow users to add a task with a title and description.

---

## 5️⃣ Non-Functional Requirements
Constraints related to:
- Usability
- Performance
- Maintainability
- Platform limitations

---

## 6️⃣ Edge Cases & Constraints
Describe boundary conditions, invalid inputs, and limitations.

---

## 7️⃣ Acceptance Criteria
For each major feature, define clear success conditions.

Each criterion must be verifiable without interpretation.

---
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template


def main():
    parser = argparse.ArgumentParser(description='Generate software specification template')
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('--project-name', '-p', type=str, help='Project name for the specification')

    args = parser.parse_args()

    spec_content = create_specification_template()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print(f"Specification template written to {args.output}")
    else:
        print(spec_content)


if __name__ == "__main__":
    main()