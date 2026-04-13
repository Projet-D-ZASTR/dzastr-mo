INVOICE_PAYLOAD = {
    "User_Id": 1,
    "Client_Id": 1,
    "Facture_Prix": 150.0,
    "Facture_Date": "2024-01-15",
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
    assert data["User_Id"] == 1
    assert data["Client_Id"] == 1
    assert data["Facture_Prix"] == 150.0
    assert data["Facture_Date"] == "2024-01-15"
    assert data["Facture_State"] == "draft"
    assert data["item_ids"] == [1, 2]


def test_lister_invoices(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    client.post("/invoices/", json={**INVOICE_PAYLOAD, "User_Id": 2})
    res = client.get("/invoices/")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_lister_invoices_par_user(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    client.post("/invoices/", json={**INVOICE_PAYLOAD, "User_Id": 2})
    res = client.get("/invoices/?User_Id=1")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["User_Id"] == 1


def test_obtenir_invoice(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.get("/invoices/1")
    assert res.status_code == 200
    assert res.json()["Facture_Id"] == 1


def test_obtenir_invoice_inexistante(client):
    res = client.get("/invoices/999")
    assert res.status_code == 404


def test_modifier_invoice_prix(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.put("/invoices/1", json={"Facture_Prix": 200.0})
    assert res.status_code == 200
    assert res.json()["Facture_Prix"] == 200.0


def test_modifier_invoice_state(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.put("/invoices/1", json={"Facture_State": "sent"})
    assert res.status_code == 200
    assert res.json()["Facture_State"] == "sent"


def test_modifier_invoice_items(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.put("/invoices/1", json={"item_ids": [3, 4, 5]})
    assert res.status_code == 200
    assert res.json()["item_ids"] == [3, 4, 5]


def test_modifier_invoice_inexistante(client):
    res = client.put("/invoices/999", json={"Facture_Prix": 100.0})
    assert res.status_code == 404


def test_supprimer_invoice(client):
    client.post("/invoices/", json=INVOICE_PAYLOAD)
    res = client.delete("/invoices/1")
    assert res.status_code == 204
    assert client.get("/invoices/1").status_code == 404


def test_supprimer_invoice_inexistante(client):
    res = client.delete("/invoices/999")
    assert res.status_code == 404
