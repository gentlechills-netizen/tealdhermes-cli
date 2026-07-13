#!/usr/bin/env python3
"""
sources.py — Canonical data sources for the tldrhc generators.

Shared functions used by generate_listing.py and generate_pages.py.
All data comes from manual YAML files — no scraping.
"""

import os
import yaml

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Helpers ────────────────────────────────────────────────────────────

def _path(name):
    return os.path.join(SCRIPT_DIR, name)


def load_yaml(name):
    path = _path(name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Source not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f) or {}


# ═══════════════════════════════════════════════════════════════════════
# INCLUDED COMMANDS
# ═══════════════════════════════════════════════════════════════════════

def get_commands():
    """Returns the list of command names with inclusion=true, in YAML order."""
    incl = load_yaml("inclusions.yaml")
    return [name for name, included in incl.items() if included]


# ═══════════════════════════════════════════════════════════════════════
# DESCRIPTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_descriptions():
    """Returns the dict {command: {short, syntax}}."""
    return load_yaml("descriptions.yaml")


def get_description(cmd):
    """Returns the short description for a command."""
    descs = get_descriptions()
    info = descs.get(cmd, {})
    return info.get("short", "")


# ═══════════════════════════════════════════════════════════════════════
# EXAMPLES
# ═══════════════════════════════════════════════════════════════════════

def load_examples():
    """Returns the dict {command: [{cmd, desc}, ...]}."""
    return load_yaml("examples.yaml")


# ═══════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════

def page_name(name):
    """Filename for a command's .page.md file (e.g., hc-backup.page.md)."""
    return f"hc-{name}.page.md"