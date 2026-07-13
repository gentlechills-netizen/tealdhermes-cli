#!/bin/bash
# install.sh — Installs tldrhc (TLDR for Hermes CLI)
# Usage: curl -sSL https://.../install.sh | bash

set -e

TLDRHC_BIN="${TLDRHC_BIN:-$HOME/.local/bin/tldrhc}"
TLDRHC_PAGES="${TLDRHC_PAGES:-$HOME/.local/share/tldrhc/pages}"
TLDRHC_CONFIG="${TLDRHC_CONFIG:-$HOME/.config/tldrhc/config.toml}"

echo "📦 Installing tldrhc..."

# 1. Create directories
mkdir -p "$(dirname "$TLDRHC_BIN")"
mkdir -p "$TLDRHC_PAGES"
mkdir -p "$(dirname "$TLDRHC_CONFIG")"

# 2. Install the wrapper
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/tldrhc" ]; then
    cp "$SCRIPT_DIR/tldrhc" "$TLDRHC_BIN"
else
    echo "⚠ tldrhc script not found. Downloading from GitHub..."
    curl -sSL -o "$TLDRHC_BIN" "https://raw.githubusercontent.com/gentlechills-netizen/tealdhermes-cli/main/tldrhc"
fi
chmod +x "$TLDRHC_BIN"

# 3. Install pages
if [ -d "$SCRIPT_DIR/pages" ]; then
    cp "$SCRIPT_DIR/pages/"*.page.md "$TLDRHC_PAGES/" 2>/dev/null || true
    cp "$SCRIPT_DIR/pages/_listing.md" "$TLDRHC_PAGES/" 2>/dev/null || true
fi

# 4. Config tealdeer
if [ ! -f "$TLDRHC_CONFIG" ]; then
    cat > "$TLDRHC_CONFIG" << EOF
[directories]
custom_pages_dir = "${HOME}/.local/share/tldrhc/pages"
[updates]
auto_update = false
[display]
compact = false
use_pager = false
EOF
fi

# 5. Add ~/.local/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo "→ ~/.local/bin added to PATH in .bashrc"
fi

echo "✅ tldrhc installed in $TLDRHC_BIN"
echo ""
echo "Open a new terminal or source ~/.bashrc:"
echo "  source ~/.bashrc"
echo ""
echo "Usage:"
echo "  tldrhc              List commands"
echo "  tldrhc backup       Help page for hermes backup"
