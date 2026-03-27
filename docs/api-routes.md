# API Routes — Documentation Frontend

Base URL : `http://localhost:8000` (dev)

---

## Clients `/clients`

### GET /clients/
Liste tous les clients.

**Réponse 200**
```json
[
  {
    "id": 1,
    "name": "Jean Dupont",
    "entreprise": "Dupont SARL",
    "email": "jean@dupont.fr",
    "adresse": "12 rue de la Paix, Paris"
  }
]
```

---

### GET /clients/{client_id}
Récupère un client par son ID.

**Réponse 200** — objet `ClientResponse`

**Erreurs**
- `404` — Client not found

---

### POST /clients/
Crée un nouveau client.

**Body (JSON)**
```json
{
  "name": "Jean Dupont",
  "entreprise": "Dupont SARL",
  "email": "jean@dupont.fr",
  "adresse": "12 rue de la Paix, Paris"
}
```
Tous les champs sont **requis** et ne peuvent pas être vides.

**Réponse 201** — objet `ClientResponse`

---

### PUT /clients/{client_id}
Met à jour un client (mise à jour partielle supportée).

**Body (JSON)** — tous les champs sont optionnels
```json
{
  "name": "Jean Dupont",
  "entreprise": "Nouvelle SARL",
  "email": "nouveau@email.fr",
  "adresse": "42 avenue Victor Hugo"
}
```

**Réponse 200** — objet `ClientResponse` mis à jour

**Erreurs**
- `404` — Client not found

---

### DELETE /clients/{client_id}
Supprime un client.

**Query param requis** : `?confirme=true`

```
DELETE /clients/3?confirme=true
```

**Réponse 204** — corps vide

**Erreurs**
- `400` — confirmation manquante
- `404` — Client not found

---

## Services `/services`

### GET /services/
Liste tous les services.

**Réponse 200**
```json
[
  {
    "service_id": 1,
    "service_nom": "Développement web",
    "service_prixHeure": "85.00",
    "service_description": "Développement frontend et backend"
  }
]
```

---

### GET /services/{service_id}
Récupère un service par son ID.

**Réponse 200** — objet `ServiceResponse`

**Erreurs**
- `404` — Service introuvable

---

### POST /services/
Crée un nouveau service.

**Body (JSON)**
```json
{
  "nom": "Développement web",
  "prix_heure": 85.00
}
```

| Champ | Type | Règles |
|-------|------|--------|
| `nom` | string | requis, non vide |
| `prix_heure` | decimal | requis, > 0 |

**Réponse 201** — objet `ServiceResponse`

---

### PUT /services/{service_id}
Met à jour un service (mise à jour partielle supportée).

**Body (JSON)** — tous les champs sont optionnels
```json
{
  "nom": "Consulting",
  "prix_heure": 100.00
}
```

**Réponse 200** — objet `ServiceResponse` mis à jour

**Erreurs**
- `404` — Service introuvable

---

### DELETE /services/{service_id}
Supprime un service.

**Query param requis** : `?confirme=true`

```
DELETE /services/5?confirme=true
```

**Réponse 204** — corps vide

**Erreurs**
- `400` — confirmation manquante
- `404` — Service introuvable

---

## Factures `/invoices`

### GET /invoices/
Liste toutes les factures. Peut être filtré par utilisateur.

**Query param optionnel** : `?user_id=1`

**Réponse 200**
```json
[
  {
    "invoice_id": 1,
    "user_id": 1,
    "client_id": 2,
    "invoice_price": 1250.00,
    "invoice_date": "2026-03-27",
    "invoice_state": "draft",
    "item_ids": [1, 3, 5]
  }
]
```

---

### GET /invoices/{invoice_id}
Récupère une facture par son ID.

**Réponse 200** — objet `InvoiceRead`

**Erreurs**
- `404` — facture introuvable

---

### POST /invoices/
Crée une nouvelle facture.

**Body (JSON)**
```json
{
  "user_id": 1,
  "client_id": 2,
  "invoice_price": 1250.00,
  "invoice_date": "2026-03-27",
  "item_ids": [1, 3, 5]
}
```

| Champ | Type | Règles |
|-------|------|--------|
| `user_id` | int | requis |
| `client_id` | int | requis |
| `invoice_price` | float | requis |
| `invoice_date` | date (YYYY-MM-DD) | requis |
| `item_ids` | int[] | requis |

**Réponse 201** — objet `InvoiceRead`

---

### PUT /invoices/{invoice_id}
Met à jour une facture (mise à jour partielle supportée).

**Body (JSON)** — tous les champs sont optionnels
```json
{
  "invoice_price": 1500.00,
  "invoice_date": "2026-04-01",
  "invoice_state": "sent",
  "item_ids": [1, 2]
}
```

`invoice_state` valeurs possibles : `draft` | `sent` | `paid` | `cancelled`

> Fournir `item_ids` **remplace** tous les items existants de la facture.

**Réponse 200** — objet `InvoiceRead` mis à jour

**Erreurs**
- `404` — facture introuvable

---

### DELETE /invoices/{invoice_id}
Supprime une facture.

**Réponse 204** — corps vide

**Erreurs**
- `404` — facture introuvable

---

## Résumé des routes

| Méthode | Endpoint | Description | Status |
|---------|----------|-------------|--------|
| GET | `/clients/` | Liste les clients | 200 |
| GET | `/clients/{id}` | Récupère un client | 200 |
| POST | `/clients/` | Crée un client | 201 |
| PUT | `/clients/{id}` | Met à jour un client | 200 |
| DELETE | `/clients/{id}?confirme=true` | Supprime un client | 204 |
| GET | `/services/` | Liste les services | 200 |
| GET | `/services/{id}` | Récupère un service | 200 |
| POST | `/services/` | Crée un service | 201 |
| PUT | `/services/{id}` | Met à jour un service | 200 |
| DELETE | `/services/{id}?confirme=true` | Supprime un service | 204 |
| GET | `/invoices/` | Liste les factures | 200 |
| GET | `/invoices/{id}` | Récupère une facture | 200 |
| POST | `/invoices/` | Crée une facture | 201 |
| PUT | `/invoices/{id}` | Met à jour une facture | 200 |
| DELETE | `/invoices/{id}` | Supprime une facture | 204 |
