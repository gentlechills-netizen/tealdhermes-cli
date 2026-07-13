#!/usr/bin/env python3
"""
generate_pages.py — Section 2: Individual pages for Hermes CLI commands

Generates .page.md files in OG tldr format.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sources import (
    get_commands, get_descriptions, load_examples,
    page_name, SCRIPT_DIR
)

PAGES_DIR = os.path.join(SCRIPT_DIR, "pages")


DOCS_URL = "https://hermes-agent.nousresearch.com/docs/reference/cli-commands"
WRAP = 78  # wrap description lines at this width


def wrap_text(text, width=WRAP):
    """Wrap text into multiple > lines at word boundaries."""
    import textwrap
    return textwrap.fill(text, width=width)


def generate_page(name, info, examples):
    """Generate .page.md content in OG tldr format."""
    lines = []
    desc = info.get("long") or info.get("short", "")
    lines.append(f"# hc-{name}")
    lines.append("")
    for line in wrap_text(desc).split("\n"):
        lines.append(f"> {line}")
    lines.append(f"> Syntax: {info.get('syntax', f'hermes {name} [options]')}")
    lines.append("")

    cmd_examples = examples.get(name, [])
    for ex in cmd_examples[:5]:
        desc = ex.get("desc", "")
        cmd = ex.get("cmd", "")
        if desc:
            lines.append(f"- {desc}")
            lines.append("")
            lines.append(f"`{cmd}`")
        else:
            lines.append(f"- `{cmd}`")
        lines.append("")

    lines.append("---")
    lines.append(f"See [hermes {name}]({DOCS_URL}#hermes-{name}) in the Hermes documentation.")
    lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(PAGES_DIR, exist_ok=True)
    commands = get_commands()
    if not commands:
        print("❌ No commands found in inclusions.yaml")
        sys.exit(1)
    descs = get_descriptions()
    examples = load_examples()

    count = 0
    for name in commands:
        info = descs.get(name, {"short": "", "syntax": f"hermes {name} [options]"})
        page = generate_page(name, info, examples)
        filepath = os.path.join(PAGES_DIR, page_name(name))
        with open(filepath, "w") as f:
            f.write(page)
        count += 1

    # Clean up orphan pages
    kept_names = {page_name(name) for name in commands}
    removed = 0
    for f in os.listdir(PAGES_DIR):
        if f.endswith(".page.md") and f not in kept_names:
            os.remove(os.path.join(PAGES_DIR, f))
            removed += 1
    if removed:
        print(f"   → {removed} orphan page(s) deleted")

    print(f"✅ {count} pages generated in {PAGES_DIR}/")


if __name__ == "__main__":
    main()