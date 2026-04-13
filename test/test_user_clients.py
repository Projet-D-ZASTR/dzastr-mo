def test_lier_user_client(client):
    client.post(
        "/clients/",
        json={
            "name": "Alice",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue",
        },
    )
    res = client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 1})
    assert res.status_code == 201
    data = res.json()
    assert data["User_Id"] == 1
    assert data["Client_Id"] == 1


def test_lier_user_client_doublon(client):
    client.post(
        "/clients/",
        json={
            "name": "Alice",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue",
        },
    )
    client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 1})
    res = client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 1})
    assert res.status_code == 409


def test_lier_user_client_inexistant(client):
    res = client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 999})
    assert res.status_code == 404


def test_clients_par_user(client):
    client.post(
        "/clients/",
        json={
            "name": "Alice",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue",
        },
    )
    client.post(
        "/clients/",
        json={
            "name": "Bob",
            "entreprise": "Corp",
            "email": "bob@corp.com",
            "adresse": "2 rue",
        },
    )
    client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 1})
    client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 2})
    res = client.get("/user-clients/1")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_clients_par_user_vide(client):
    res = client.get("/user-clients/999")
    assert res.status_code == 200
    assert res.json() == []


def test_users_par_client(client):
    client.post(
        "/clients/",
        json={
            "name": "Alice",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue",
        },
    )
    client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 1})
    client.post("/user-clients/", json={"User_Id": 2, "Client_Id": 1})
    res = client.get("/user-clients/client/1")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_delier_user_client(client):
    client.post(
        "/clients/",
        json={
            "name": "Alice",
            "entreprise": "Acme",
            "email": "alice@acme.com",
            "adresse": "1 rue",
        },
    )
    client.post("/user-clients/", json={"User_Id": 1, "Client_Id": 1})
    res = client.delete("/user-clients/1/1")
    assert res.status_code == 204
    assert client.get("/user-clients/1").json() == []


def test_delier_user_client_inexistant(client):
    res = client.delete("/user-clients/999/999")
    assert res.status_code == 404
