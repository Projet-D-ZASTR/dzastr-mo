# Explication de la syntaxe route.py

## 1. Les imports

```python
from fastapi import APIRouter, Depends, HTTPException, status
```

| Import | Rôle |
|---|---|
| `APIRouter` | Groupe les routes (équivalent de `express.Router()` en Node) |
| `Depends` | Injection de dépendances (ex: la session DB) |
| `HTTPException` | Renvoie une erreur HTTP avec un message |
| `status` | Constantes lisibles : `status.HTTP_201_CREATED` vaut `201` |

```python
from pydantic import BaseModel, field_validator
```

| Import | Rôle |
|---|---|
| `BaseModel` | Définit la forme des données JSON entrants/sortants |
| `field_validator` | Valide un champ spécifique |

---

## 2. Le router

```python
router = APIRouter(prefix="/services", tags=["services"])
```

Toutes les routes de ce fichier auront automatiquement `/services` comme préfixe.
`tags` sert à grouper dans la documentation automatique générée par FastAPI.

---

## 3. Les schémas Pydantic

### Schéma de création (champs requis)

```python
class ServiceCreate(BaseModel):
    nom: str
    prix_heure: Decimal
```

FastAPI lit le JSON de la requête et le convertit en cet objet.
Si un champ manque ou est du mauvais type → erreur **422** automatique.

### Schéma de modification (champs optionnels)

```python
class ServiceUpdate(BaseModel):
    nom: str | None = None
    prix_heure: Decimal | None = None
```

`str | None = None` → le champ est facultatif, permet une mise à jour partielle.

### Validation d'un champ

```python
@field_validator("nom")
@classmethod
def nom_non_vide(cls, v):   # v = la valeur du champ
    if not v.strip():
        raise ValueError("Le label ne peut pas être vide")
    return v.strip()
```

Valide le champ après la conversion de type. `v` est la valeur reçue.

### Schéma de réponse

```python
class ServiceResponse(BaseModel):
    id: int
    nom: str
    prix_heure: Decimal
    description: str | None

    model_config = {"from_attributes": True}
```

`from_attributes: True` permet à Pydantic de lire un objet SQLAlchemy directement (sinon il n'accepte que des dicts).

---

## 4. Les routes

### Création — POST

```python
@router.post("/", response_model=ServiceResponse, status_code=201)
def creer_service(data: ServiceCreate, db: Session = Depends(get_db)):
```

- `@router.post("/")` — écoute `POST /services/`
- `data: ServiceCreate` — FastAPI parse et valide le body JSON automatiquement
- `db: Session = Depends(get_db)` — FastAPI appelle `get_db()` et injecte la session DB

```python
db.add(service)      # prépare l'insertion
db.commit()          # exécute le SQL
db.refresh(service)  # recharge depuis la DB (récupère l'id généré)
```

### Modification — PUT

```python
@router.put("/{service_id}", response_model=ServiceResponse)
def modifier_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)):
```

- `{service_id}` dans l'URL → lu automatiquement comme paramètre `int`
- Seuls les champs envoyés sont mis à jour (les autres restent inchangés)

### Suppression — DELETE

```python
@router.delete("/{service_id}", status_code=204)
def supprimer_service(service_id: int, confirme: bool = False, db: Session = Depends(get_db)):
```

- `confirme: bool = False` → lu depuis le query param `?confirme=true`
- Sans confirmation → erreur **400**

---

## 5. Flux d'une requête

```
Requête JSON → Pydantic valide → fonction route → SQLAlchemy → PostgreSQL
                                                        ↓
                                          Pydantic formate → Réponse JSON
```

---

## 6. Structure du projet

```
dzastr-mo/
├── main.py              # point d'entrée FastAPI
├── config.py            # connexion PostgreSQL
└── src/
    ├── models/
    │   ├── base.py      # Base SQLAlchemy partagée
    │   ├── services.py  # modèle Service
    └── route/
        └── services.py  # routes CRUD services
```
