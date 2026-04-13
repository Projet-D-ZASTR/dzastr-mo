INVOICE_PAYLOAD = {
    "user_id": 1,
    "client_id": 1,
    "invoice_price": 150.0,
    "invoice_date": "2024-01-15",
    "item_ids": [1, 2],
}


def test_lister_invoices_vide(client):
    res = client.get("/invoices/")
    assert res.status_code == 200
    assert res.json() == []


def test_creer_invoice(client):
    res = client.post("/invoices/", json=INVOICE_PAYLOAD)
    assert res.status_code == 201
    data = res.json()
    assert data["user_id"] == 1
    assert data["client_id"] == 1
    assert data["invoice_price"] == 150.0
    assert data["invoice_date"] == "2024-01-15"
    assert data["invoice_state"] == "draft"
    assert data["item_ids"] == [1, 2]


def test_lister_invoices(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    client.post("/invoices/", json={**INVOICE_PAYLOAD, "user_id": 2})
    res = client.get("/invoices/")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_lister_invoices_par_user(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    client.post("/invoices/", json={**INVOICE_PAYLOAD, "user_id": 2})
    res = client.get("/invoices/?user_id=1")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["user_id"] == 1


def test_obtenir_invoice(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.get("/invoices/1")
    assert res.status_code == 200
    assert res.json()["invoice_id"] == 1


def test_obtenir_invoice_inexistante(client):
    res = client.get("/invoices/999")
    assert res.status_code == 404


def test_modifier_invoice_prix(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.put("/invoices/1", json={"invoice_price": 200.0})
    assert res.status_code == 200
    assert res.json()["invoice_price"] == 200.0


def test_modifier_invoice_state(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.put("/invoices/1", json={"invoice_state": "sent"})
    assert res.status_code == 200
    assert res.json()["invoice_state"] == "sent"


def test_modifier_invoice_items(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.put("/invoices/1", json={"item_ids": [3, 4, 5]})
    assert res.status_code == 200
    assert res.json()["item_ids"] == [3, 4, 5]


def test_modifier_invoice_inexistante(client):
    res = client.put("/invoices/999", json={"invoice_price": 100.0})
    assert res.status_code == 404


def test_supprimer_invoice(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.delete("/invoices/1")
    assert res.status_code == 204
    assert client.get("/invoices/1").status_code == 404


def test_supprimer_invoice_inexistante(client):
    res = client.delete("/invoices/999")
    assert res.status_code == 404
