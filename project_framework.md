# tldrhc — Project Framework

## Objectif

Un `tldr` pour Hermes CLI. L'utilisateur tape `tldrhc backup` et voit la page d'aide de `hermes backup` au format OG tldr. Il tape `tldrhc` et voit la liste des commandes disponibles.

`tldr cp` continue de fonctionner pour les commandes Linux. Les deux cohabitent via `TEALDEER_CONFIG_DIR` séparé.

**Public cible :** Utilisateurs Hermes Agent en CLI.

## Architecture

```
tealdeer (Rust, 2MB)
   └─ TEALDEER_CONFIG_DIR=~/.config/tldrhc/   ← config séparée
        └─ custom_pages_dir → ~/.local/share/tldrhc/pages/
              ├── _listing.md                 ← listing 2 colonnes
              └── hc-backup.page.md           ← page individuelle

wrapper ~/.local/bin/tldrhc (bash)
   ├─ `tldrhc`         → cat _listing.md
   └─ `tldrhc backup`  → TEALDEER_CONFIG_DIR=... tldr hc-backup

générateurs (Python)
   ├─ generate_listing.py  → _listing.md
   └─ generate_pages.py    → hc-*.page.md (×14)
        └─ sources.py      ← module partagé (YAML only)
```

## Fichiers et répertoires

```
~/.hermes/tldr-hermes-cli/            ← Projet (sources)
├── generate_listing.py               ← Listing 2 colonnes
├── generate_pages.py                 ← Pages .page.md
├── sources.py                        ← Module partagé (YAML loading)
├── update.sh                         ← Regénère tout + rapport diff
├── install.sh                        ← Installation one-liner
├── tldrhc                            ← Wrapper bash
├── config.toml                       ← Patron config tealdeer
├── inclusions.yaml                    ← 14 commandes opt-in
├── descriptions.yaml                 ← Descriptions officielles + syntaxe
├── examples.yaml                     ← Exemples OG tldr
├── .gitignore
├── README.md                         ← Documentation utilisateur
├── project_framework.md              ← Ce fichier
├── data_architecture.md              ← Architecture des données
├── tldrhc_pages_style_guide.md       ← Règles de format des pages
└── reports/                          ← Rapports de diff (générés)

~/.local/bin/tldrhc                   ← Wrapper installé (PATH)
~/.config/tldrhc/config.toml          ← Config tealdeer runtime
~/.local/share/tldrhc/pages/          ← Pages runtime (hc-*.page.md)
```

## Principaux scripts

| Script | Rôle |
|--------|------|
| `update.sh` | Vérifie les sources, génère listing + pages, copie runtime, produit rapport diff |
| `generate_listing.py` | Lit inclusions.yaml + descriptions.yaml, produit _listing.md (2 colonnes, tri alphabétique) |
| `generate_pages.py` | Lit descriptions.yaml + examples.yaml, produit 14 hc-*.page.md (OG tldr) |
| `install.sh` | Copie wrapper dans PATH, pages dans share/, config dans .config/ |

## Mise à jour

Quand Hermes change (nouvelles commandes, descriptions modifiées) :

```bash
cd ~/.hermes/tldr-hermes-cli && ./update.sh
```

Le script `update.sh` :

1. **Vérification** — confirme que les 6 sources existent (sources.py, generate_listing.py, generate_pages.py, inclusions.yaml, descriptions.yaml, examples.yaml)
2. **Listing** — exécute `generate_listing.py` → `pages/_listing.md`
3. **Pages** — exécute `generate_pages.py` → `pages/hc-*.page.md` (14 fichiers)
4. **Nettoyage** — supprime les pages orphelines (commandes retirées de inclusions.yaml)
5. **Diff** — compare `examples.yaml` avec `get_commands()` ; signale les nouvelles commandes sans exemples et les entrées orphelines
6. **Copie runtime** — copie `_listing.md` + `hc-*.page.md` vers `~/.local/share/tldrhc/pages/` et `tldrhc` vers `~/.local/bin/tldrhc`

**Règle fondamentale :** les exemples sont créés et révisés manuellement par le mainteneur, sans automatisation ni IA.

## Installation

```bash
cd ~/.hermes/tldr-hermes-cli && bash install.sh
```

Le script `install.sh` :

1. **Wrapper** — copie `tldrhc` vers `~/.local/bin/tldrhc` et le rend exécutable
2. **Pages** — copie les fichiers `*.page.md` et `_listing.md` de `pages/` vers `~/.local/share/tldrhc/pages/`
3. **Config** — crée `~/.config/tldrhc/config.toml` avec `custom_pages_dir` pointant vers les pages runtime
4. **PATH** — ajoute `~/.local/bin` au PATH dans `.bashrc` si pas déjà présent

Prérequis : `tldr` (tealdeer), `python3` + `pyyaml`.

## Contraintes de conception

- **Pas de scraping** — toutes les données viennent de YAML manuels.
- **Pas de catégories** — listing plat, tri alphabétique.
- **14 commandes seulement** — le dashboard couvre le reste.
- **sources.py sans cache** — chaque appel lit le fichier YAML. Ajouter une commande = effet immédiat.

## Pièges connus

### Alias bash périmé après modification

Après toute modification du wrapper (`tldrhc`), le développeur DOIT exécuter `source ~/.bashrc` (ou ouvrir un nouveau terminal).

**Vérification :** `type tldrhc` — si le chemin affiché n'est pas celui attendu, la session n'est pas à jour.

### Pages nommées `hc-*.page.md`

Le wrapper mappe `tldrhc backup` → `tldr hc-backup`. Les pages sont préfixées `hc-` pour éviter les collisions avec les pages Linux standard de tealdeer. Ne pas renommer les fichiers sans mettre à jour le wrapper.

### `TEALDEER_CONFIG_DIR` doit être configuré

Le wrapper utilise `TEALDEER_CONFIG_DIR=~/.config/tldrhc/` pour isoler la config tealdeer. Sans cette variable, `tldr` utilise sa config globale qui peut ne pas avoir `custom_pages_dir` défini. Si les pages ne s'affichent pas, vérifier `~/.config/tldrhc/config.toml`.

### Ajouter une commande = 3 fichiers YAML à éditer

Pour ajouter une commande aux pages tldrhc :
1. `inclusions.yaml` — mettre `nom: true`
2. `descriptions.yaml` — ajouter `short:` et `syntax:`
3. `examples.yaml` — ajouter les exemples (optionnel mais recommandé)
4. Lancer `./update.sh`

### Langue

Les descriptions et les exemples sont en anglais (extraites du `hermes <cmd> --help` ou de la doc officielle Hermes). Le wrapper, les messages et les commentaires du projet sont également en anglais.

## Sources de données

Voir `data_architecture.md` pour la description complète des 3 sources canoniques :
inclusions.yaml, descriptions.yaml, examples.yaml.
