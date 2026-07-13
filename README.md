# tldrhc — tldr for Hermes CLI commands

`tldrhc` brings the familiar **tldr** format to [Hermes Agent](https://hermes-agent.nousresearch.com) CLI commands. Quickly look up any `hermes <command>` without leaving the terminal.

```
$ tldrhc
TLDRHC — Hermes CLI Commands
════════════════════════════════════════════════════════════════════════════════

> 14 Hermes CLI commands — tldrhc <command> for details.

hermes auth                Manage credentials — add, list, remove, reset, status,
hermes backup              Create a zip archive of your Hermes configuration, skil
...

$ tldrhc backup
  Create a zip archive of your Hermes configuration, skills, sessions, and data.
  Syntax: hermes backup [options]

  Full backup to default location:

      hermes backup

  Quick snapshot with label:

      hermes backup --quick --label pre-upgrade
```

## Prerequisites

- [tealdeer](https://github.com/dbrgn/tealdeer) (Rust `tldr` client)
- Python 3.9+ with `pyyaml`

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/gentlechills-netizen/tealdhermes/main/install.sh | bash
```

This installs the wrapper to `~/.local/bin/tldrhc`, pages to `~/.local/share/tldrhc/pages/`, and config to `~/.config/tldrhc/config.toml`.

Requires `tldr` (tealdeer) installed on the system.

## Usage

```
tldrhc                    List all 14 Hermes CLI commands
tldrhc <command>           Show help page for any command (e.g. tldrhc backup)
```

## Maintenance

```bash
cd ~/.hermes/tldr-hermes-cli && ./update.sh
```

Regenerates listing, pages, and copies to runtime locations. Run after editing any YAML source.

## How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────────┐
│  inclusions.yaml │     │  generate_*.py   │     │  ~/.local/share/tldrhc   │
│  descriptions   │────▶│                  │────▶│  /pages/hc-*.page.md    │
│  .yaml          │     │  sources.py      │     │  /pages/_listing.md     │
│  examples.yaml  │     │                  │     │                          │
│                 │                               │  tealdeer renders      │
└─────────────────┘                               └──────────────────────────┘
```

All data comes from manual YAML files — zero scraping.

## Project Structure

```
~/.hermes/tldr-hermes-cli/
├── generate_listing.py     Listing generator (2-column)
├── generate_pages.py       Page generator (OG tldr)
├── sources.py              Shared data module (YAML loading)
├── inclusions.yaml          14 commands opt-in
├── descriptions.yaml       Official descriptions + syntax
├── examples.yaml           Manual examples (23 total)
├── config.toml             tealdeer config
├── tldrhc                  Wrapper script
├── install.sh              Installation script
├── update.sh               Regenerate everything
├── README.md               This file
├── project_framework.md    Design decisions
├── data_architecture.md    Data sources & pipeline
├── tldrhc_pages_style_guide.md  Style guide
└── pages/                  Generated output
    ├── _listing.md
    └── hc-*.page.md (×14)
```

## License

MIT
