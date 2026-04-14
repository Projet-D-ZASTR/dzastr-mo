def test_lister_services_vide(client):
    res = client.get("/services/")
    assert res.status_code == 200
    assert res.json() == []


def test_creer_service(client):
    res = client.post(
        "/services/",
        json={
            "Service_Name": "Dev web",
            "Service_PriceHour": 75.0,
            "Service_UserId": 1,
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["Service_Name"] == "Dev web"
    assert float(data["Service_PriceHour"]) == 75.0
    assert data["Service_Id"] == 1
    assert data["Service_UserId"] == 1


def test_creer_service_nom_vide(client):
    res = client.post(
        "/services/",
        json={"Service_Name": "  ", "Service_PriceHour": 75.0, "Service_UserId": 1},
    )
    assert res.status_code == 422


def test_creer_service_prix_nul(client):
    res = client.post(
        "/services/",
        json={"Service_Name": "Dev", "Service_PriceHour": 0, "Service_UserId": 1},
    )
    assert res.status_code == 422


def test_creer_service_prix_negatif(client):
    res = client.post(
        "/services/",
        json={"Service_Name": "Dev", "Service_PriceHour": -10.0, "Service_UserId": 1},
    )
    assert res.status_code == 422


def test_obtenir_service(client):
    client.post(
        "/services/",
        json={
            "Service_Name": "Dev web",
            "Service_PriceHour": 75.0,
            "Service_UserId": 1,
        },
    )
    res = client.get("/services/1")
    assert res.status_code == 200
    assert res.json()["Service_Name"] == "Dev web"
    assert res.json()["Service_UserId"] == 1


def test_obtenir_service_inexistant(client):
    res = client.get("/services/999")
    assert res.status_code == 404


def test_modifier_service_nom(client):
    client.post(
        "/services/",
        json={
            "Service_Name": "Dev web",
            "Service_PriceHour": 75.0,
            "Service_UserId": 1,
        },
    )
    res = client.put("/services/1", json={"Service_Name": "Dev mobile"})
    assert res.status_code == 200
    assert res.json()["Service_Name"] == "Dev mobile"
    assert float(res.json()["Service_PriceHour"]) == 75.0


def test_modifier_service_prix(client):
    client.post(
        "/services/",
        json={
            "Service_Name": "Dev web",
            "Service_PriceHour": 75.0,
            "Service_UserId": 1,
        },
    )
    res = client.put("/services/1", json={"Service_PriceHour": 90.0})
    assert res.status_code == 200
    assert float(res.json()["Service_PriceHour"]) == 90.0


def test_modifier_service_inexistant(client):
    res = client.put("/services/999", json={"Service_Name": "Dev"})
    assert res.status_code == 404


def test_supprimer_service_sans_confirmation(client):
    client.post(
        "/services/",
        json={
            "Service_Name": "Dev web",
            "Service_PriceHour": 75.0,
            "Service_UserId": 1,
        },
    )
    res = client.delete("/services/1")
    assert res.status_code == 400


def test_supprimer_service(client):
    client.post(
        "/services/",
        json={
            "Service_Name": "Dev web",
            "Service_PriceHour": 75.0,
            "Service_UserId": 1,
        },
    )
    res = client.delete("/services/1?confirme=true")
    assert res.status_code == 204
    assert client.get("/services/1").status_code == 404


def test_supprimer_service_inexistant(client):
    res = client.delete("/services/999?confirme=true")
    assert res.status_code == 404
