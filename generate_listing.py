#!/usr/bin/env python3
"""
generate_listing.py — Listing tldrhc Section 1

Generates _listing.md from manual YAML sources.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sources import get_commands, get_descriptions, SCRIPT_DIR

OUTPUT = os.path.join(SCRIPT_DIR, "pages", "_listing.md")

def build_listing():
    commands = sorted(get_commands())
    if not commands:
        print("❌ No commands found in inclusions.yaml")
        sys.exit(1)
    descs = get_descriptions()

    lines = [
        "TLDRHC — Hermes CLI Commands",
        "═" * 80,
        "",
        f">{len(commands)} Hermes CLI commands — tldrhc <command> for details.",
        "",
    ]

    for name in commands:
        info = descs.get(name, {})
        short = info.get("short", "")[:95]
        lines.append(f"hermes {name:<15} {short:<95}")

    lines.append("")
    lines.append("Usage: `tldrhc <command>` to show the help page for a command.")
    lines.append("")
    lines.append("Examples:")
    lines.append("  tldrhc status")
    lines.append("  tldrhc backup")
    lines.append("")

    return "\n".join(lines)

def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    listing = build_listing()
    with open(OUTPUT, "w") as f:
        f.write(listing)
    count = len(get_commands())
    print(f"✅ Listing generated — {count} command(s) listed")
    print(f"   File: {OUTPUT}")

if __name__ == "__main__":
    main()