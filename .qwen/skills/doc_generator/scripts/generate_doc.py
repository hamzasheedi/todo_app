#!/usr/bin/env python3
"""
Documentation Generator Script

This script helps generate professional, judge-ready documentation
following the required format for the doc_generator skill.
"""

import argparse
import sys
from datetime import datetime


def create_documentation_template():
    """Create a template for professional documentation."""
    template = f"""# Project Overview

[Provide a clear, concise explanation of what the project does, its purpose, main features, and target audience. This should be accessible to both technical and non-technical readers.]

---

# Setup Instructions

[Detailed steps for setting up the project environment, including prerequisites, dependencies, and installation procedures. Include any configuration requirements.]

---

# How to Run

[Clear instructions for running the project, including command examples, environment variables, and common usage patterns. Provide examples of typical usage scenarios.]

---

# AI Agent Workflow

[Detailed explanation of how AI agents were used in the development process, including which agents were used, what tasks they performed, and the benefits gained from AI-assisted development.]

---

# Project Evolution

[Chronological description of how the project was developed, key milestones, major changes, and evolution of the architecture or implementation approach.]

---
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template


def main():
    parser = argparse.ArgumentParser(description='Generate documentation template')
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('--project-name', '-p', type=str, help='Project name to include in documentation')

    args = parser.parse_args()

    doc_content = create_documentation_template()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        print(f"Documentation template written to {args.output}")
    else:
        print(doc_content)


if __name__ == "__main__":
    main()