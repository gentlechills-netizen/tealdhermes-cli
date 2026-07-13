# tldrhc — Data Architecture

## Principles

- **No categories** — the listing is a flat list sorted alphabetically.
- **No scraping** — all data comes from manual YAML files. No HTTP requests, no HTML/BS4 parsers. The official doc cache file is a reference for descriptions, not a runtime source.
- **No static cache** — each function in `sources.py` reads the YAML file on every call. Adding a command in `inclusions.yaml` = immediate effect.
- **FLEXIBLE** — the system supports adding YAML sources to enrich content without modifying the pipeline.

## Canonical sources

3 sources de données YAML, toutes manuelles.

| Source | Contenu | Entrées |
|--------|---------|---------|
| `inclusions.yaml` | Opt-in des commandes documentées. 14 entrées, valeur `true`/`false`. Contrôle ce qui apparaît dans le listing et les pages. | 14 |
| `descriptions.yaml` | Descriptions officielles + syntaxe. Clé = nom commande, valeur = `{short, syntax}`. Les `short` sont extraites du `hermes <cmd> --help` (priorité) ou du cache docs officiel (colonne Purpose), validées par Patrick. | 14 |
| `examples.yaml` | Exemples au format OG tldr. Clé = nom commande, valeur = liste de `{desc, cmd}`. `desc` vide = format compact sans ligne de description. Max 5 exemples par commande. | 14 |

## Pipeline de génération

```
YAML manuels
├── inclusions.yaml
├── descriptions.yaml
└── examples.yaml
       │
       ▼
   sources.py (module partagé — lit les YAML à chaque appel)
       │
       ├──▶ generate_listing.py ──▶ pages/_listing.md
       │
       └──▶ generate_pages.py ──▶ pages/hc-*.page.md (×14)
                                    │
                                    ▼
                              update.sh
                              ├── regénère listing + pages
                              ├── copie vers ~/.local/share/tldrhc/pages/
                              └── copie wrapper ~/.local/bin/tldrhc
                                    │
                                    ▼
                              tealdeer (moteur tldr)
                              └── TEALDEER_CONFIG_DIR=~/.config/tldrhc/
                                    └── custom_pages_dir → pages runtime
```

## Format listing (`_listing.md`)

2 colonnes, largeur fixe : nom (22 chars, préfixe `hermes`) + description (95 chars, tronquée).

```
TLDRHC — Hermes CLI Commands
════════════════════════════════════════════════════════════════════════════════

> 14 Hermes CLI commands — tldrhc <command> for details.

hermes auth            Manage OAuth credentials for Codex/Nous/Anthropic
hermes backup          Create a zip archive of your entire Hermes configuration, skills, sessions, and data
hermes checkpoints     Manage the filesystem checkpoint store
hermes dashboard       Launch the Hermes Agent web dashboard for managing config, API keys, and sessions
hermes doctor          Diagnose issues with Hermes Agent setup
hermes import          Extract a previously created Hermes backup into your Hermes home directory
hermes portal          Nous Portal status, subscription link, and Tool Gateway routing
hermes secrets         Pull API keys from an external secret manager instead of storing them
hermes security        On-demand vulnerability scan against OSV.dev
hermes sessions        Browse and manage sessions: export, prune, rename, delete, etc
hermes setup           Configure Hermes Agent with an interactive wizard
hermes status          Display status of Hermes Agent components: agent, auth, platform, etc
hermes update          Pull the latest code changes and reinstall dependencies
hermes version         Show Hermes-Agent version information
```

Tri alphabétique. Pas de catégories.

## Format page (`.page.md`)

```
# hc-backup

> Create a zip archive of your entire Hermes configuration, skills, sessions,
> and data (excludes the hermes-agent codebase)
> Syntax: hermes backup [options]

- Full backup to ~/hermes-backup-*.zip:

`hermes backup`

- Full backup to specific path:

`hermes backup -o /tmp/hermes.zip`

- Quick state-only snapshot:

`hermes backup --quick`

- Quick snapshot with label:

`hermes backup --quick --label "pre-upgrade"`
```

Voir `tldrhc_pages_style_guide.md` pour les règles détaillées.



## Exemples (`examples.yaml`)

- 14 commandes avec exemples
- 2-5 exemples par commande
- Max 5 exemples
- Format : `{desc, cmd}` avec placeholders `{{value}}`

## Mise à jour

`update.sh` vérifie la cohérence entre `examples.yaml` et les commandes actuelles.
Aucun fichier n'est modifié automatiquement. L'humain agit sur le rapport.

## Distribution

- `install.sh` : copie wrapper + pages + config
- README.md : documentation utilisateur
