# Ruff — Linter & Formatter Python

Ruff remplace à lui seul **Flake8 (+ plugins), Black, isort, pyupgrade, pydocstyle et autoflake**, avec des performances **10-100x supérieures**.

Sources : [Doc officielle](https://github.com/astral-sh/ruff) · [Blog Stéphane Robert](https://blog.stephane-robert.info/docs/developper/programmation/python/ruff/)

---

## Installation

La méthode recommandée est **uv** :

```bash
uv tool install ruff@latest  # global
uv add --dev ruff            # dans le projet
```

Autres options :

```bash
pip install ruff
pipx install ruff

# Standalone (macOS/Linux)
curl -LsSf https://astral.sh/ruff/install.sh | sh
```

---

## Les règles (rule sets)

Ruff intègre **800+ règles**. Par défaut seules `E4`, `E7`, `E9` et `F` sont actives.

| Préfixe | Origine | Ce qu'elles vérifient |
|---------|---------|----------------------|
| `E` | pycodestyle | Erreurs de style (espaces, indentation) |
| `W` | pycodestyle | Avertissements de style |
| `F` | Pyflakes | Erreurs logiques (variables non utilisées, imports manquants) |
| `I` | isort | Organisation des imports |
| `B` | flake8-bugbear | Bugs potentiels et mauvaises pratiques |
| `UP` | pyupgrade | Syntaxe obsolète à moderniser |
| `SIM` | flake8-simplify | Code qui peut être simplifié |
| `D` | pydocstyle | Docstrings manquantes ou mal formatées |
| `N` | pep8-naming | Conventions de nommage |
| `S` | flake8-bandit | Problèmes de sécurité |

> En activant `preview = true`, Ruff étend les règles par défaut pour inclure `B`, `UP`, `RUF` et plus.

---

## Configuration du projet (`pyproject.toml`)

Le fichier de config peut être `pyproject.toml`, `ruff.toml` ou `.ruff.toml`.

Config actuelle du projet :

```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
]
ignore = [
    "E501", # line too long (géré par le formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Config complète avec toutes les options utiles :

```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "N", "S"]
ignore = ["E501"]

# Autoriser l'auto-fix sur toutes les règles activées
fixable = ["ALL"]
unfixable = []

# Ignorer des règles par fichier
per-file-ignores = { "tests/**" = ["S101"] }

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

---

## Commandes

```bash
# Linter tout le projet
ruff check .

# Corriger automatiquement ce qui est auto-fixable
ruff check --fix .

# Corriger + fixes "unsafe" (ex: UP042 StrEnum)
ruff check --fix --unsafe-fixes .

# Activer les règles en preview
ruff check --preview .

# Cibler des règles précises sans modifier pyproject.toml
ruff check --select F401 --select F403 .

# Passer une option à la volée
ruff check --config "lint.per-file-ignores = {'tests/*.py' = ['S101']}" .

# Formatter le code (équivalent Black)
ruff format .

# Vérifier le format sans modifier (CI)
ruff format --check .
```

---

## Ignorer une règle ponctuellement

```python
import os  # noqa: F401
```

Plusieurs règles :

```python
from config import engine  # noqa: E402, F401
```

---

## Intégration pre-commit

> Depuis la v0.5.0, l'id du hook linter est `ruff-check` (et non plus `ruff`).

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.8
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
```

---

## Intégration GitHub Actions

```yaml
name: Ruff
on: [push, pull_request]
jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/ruff-action@v3
```

---

## Intégration VS Code

Installer l'extension **Ruff** (astral-sh.ruff-vscode), puis dans `settings.json` :

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  }
}
```

---

## Erreurs rencontrées dans ce projet

| Code | Fichier | Problème | Fix appliqué |
|------|---------|----------|--------------|
| `E402` | `main.py` | Imports après `load_dotenv()` | `# noqa: E402` — intentionnel |
| `I001` | plusieurs | Imports non triés | Auto-fix |
| `UP042` | `invoices.py`, `schemas/invoices.py` | `class X(str, enum.Enum)` | → `class X(StrEnum)` |
| `UP006` | `invoices_route.py`, `schemas/invoices.py` | `List[int]` déprécié | → `list[int]` |
| `UP045` | `invoices_route.py`, `schemas/invoices.py` | `Optional[X]` déprécié | → `X \| None` |
| `W292` | `src/models/client.py` | Pas de newline en fin de fichier | Auto-fix |
| `W293` | `src/models/client.py` | Ligne vide avec espaces | Auto-fix |
