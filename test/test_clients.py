def test_lister_clients_vide(client):
    res = client.get("/clients/")
    assert res.status_code == 200
    assert res.json() == []


def test_creer_client(client):
    res = client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "Alice Dupont",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue de la Paix",
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["Client_Name"] == "Alice Dupont"
    assert data["Client_Entreprise"] == "Acme"
    assert data["Client_Email"] == "alice@acme.com"
    assert data["Client_Address"] == "1 rue de la Paix"


def test_creer_client_nom_vide(client):
    res = client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "  ",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue de la Paix",
        },
    )
    assert res.status_code == 422


def test_creer_client_email_vide(client):
    res = client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "Alice",
            "entreprise": "Acme",
            "email": "  ",
            "adresse": "1 rue de la Paix",
        },
    )
    assert res.status_code == 422


def test_obtenir_client(client):
    client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "Alice Dupont",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue de la Paix",
        },
    )
    res = client.get("/clients/1")
    assert res.status_code == 200
    assert res.json()["Client_Name"] == "Alice Dupont"


def test_obtenir_client_inexistant(client):
    res = client.get("/clients/999")
    assert res.status_code == 404


def test_modifier_client(client):
    client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "Alice Dupont",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue de la Paix",
        },
    )
    res = client.put("/clients/1", json={"name": "Alice Martin"})
    assert res.status_code == 200
    assert res.json()["Client_Name"] == "Alice Martin"


def test_modifier_client_inexistant(client):
    res = client.put("/clients/999", json={"name": "Bob"})
    assert res.status_code == 404


def test_supprimer_client_sans_confirmation(client):
    client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "Alice Dupont",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue de la Paix",
        },
    )
    res = client.delete("/clients/1")
    assert res.status_code == 400


def test_supprimer_client(client):
    client.post(
        "/clients/",
        json={
            "user_id": 1,
            "name": "Alice Dupont",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue de la Paix",
        },
    )
    res = client.delete("/clients/1?confirme=true")
    assert res.status_code == 204
    assert client.get("/clients/1").status_code == 404


def test_supprimer_client_inexistant(client):
    res = client.delete("/clients/999?confirme=true")
    assert res.status_code == 404
