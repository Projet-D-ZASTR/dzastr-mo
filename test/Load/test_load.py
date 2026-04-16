"""
Load test for dzastr-mo API using Locust.

Requirements:
    pip install locust

Usage:
    # Headless (CI / quick run)
    locust -f test/Load/test_load.py \
        --headless -u 50 -r 5 --run-time 60s \
        --host http://localhost:8000

    # Interactive web UI
    locust -f test/Load/test_load.py --host http://localhost:8000

Environment variables (all optional — defaults shown):
    SERVICE_TOKEN   token sent in x-service-token header  (default: "test-token")
    BEARER_TOKEN    JWT sent as Authorization: Bearer ...  (default: "test-token")
    TARGET_USER_ID  User_Id used when creating invoices    (default: 1)
"""

import os
import random

from locust import HttpUser, between, task

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "test-token")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "test-token")
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID", "1"))


def _headers() -> dict:
    return {
        "x-service-token": SERVICE_TOKEN,
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json",
    }


class DzastrUser(HttpUser):
    """Simulates a typical API consumer hitting clients, services and invoices."""

    wait_time = between(0.5, 2)

    # ------------------------------------------------------------------ #
    # Clients                                                              #
    # ------------------------------------------------------------------ #

    @task(3)
    def list_clients(self):
        self.client.get("/clients/", headers=_headers(), name="/clients/ [GET]")

    @task(2)
    def create_and_delete_client(self):
        payload = {
            "user_id": TARGET_USER_ID,
            "name": f"Load Client {random.randint(1, 9999)}",
            "entreprise": "Acme Corp",
            "email": f"load{random.randint(1, 9999)}@example.com",
            "adresse": "123 Load St",
        }
        resp = self.client.post(
            "/clients/", json=payload, headers=_headers(), name="/clients/ [POST]"
        )
        if resp.status_code == 201:
            client_id = resp.json().get("Client_Id")
            if client_id:
                self.client.delete(
                    f"/clients/{client_id}?confirme=true",
                    headers=_headers(),
                    name="/clients/{id} [DELETE]",
                )

    @task(2)
    def get_client(self):
        # Attempt a well-known id; 404 is an expected outcome under load
        client_id = random.randint(1, 20)
        self.client.get(
            f"/clients/{client_id}",
            headers=_headers(),
            name="/clients/{id} [GET]",
        )

    @task(1)
    def update_client(self):
        client_id = random.randint(1, 20)
        payload = {"name": f"Updated {random.randint(1, 9999)}"}
        self.client.put(
            f"/clients/{client_id}",
            json=payload,
            headers=_headers(),
            name="/clients/{id} [PUT]",
        )

    # ------------------------------------------------------------------ #
    # Services                                                             #
    # ------------------------------------------------------------------ #

    @task(3)
    def list_services(self):
        self.client.get("/services/", headers=_headers(), name="/services/ [GET]")

    @task(2)
    def create_and_delete_service(self):
        payload = {
            "user_id": TARGET_USER_ID,
            "nom": f"Service {random.randint(1, 9999)}",
            "prix_heure": round(random.uniform(10, 500), 2),
        }
        resp = self.client.post(
            "/services/", json=payload, headers=_headers(), name="/services/ [POST]"
        )
        if resp.status_code == 201:
            service_id = resp.json().get("Service_Id")
            if service_id:
                self.client.delete(
                    f"/services/{service_id}?confirme=true",
                    headers=_headers(),
                    name="/services/{id} [DELETE]",
                )

    @task(1)
    def get_service(self):
        service_id = random.randint(1, 20)
        self.client.get(
            f"/services/{service_id}",
            headers=_headers(),
            name="/services/{id} [GET]",
        )

    # ------------------------------------------------------------------ #
    # Invoices                                                             #
    # ------------------------------------------------------------------ #

    @task(3)
    def list_invoices(self):
        self.client.get("/invoices/", headers=_headers(), name="/invoices/ [GET]")

    @task(3)
    def list_invoices_by_user(self):
        self.client.get(
            f"/invoices/?User_Id={TARGET_USER_ID}",
            headers=_headers(),
            name="/invoices/?User_Id [GET]",
        )

    @task(2)
    def create_and_delete_invoice(self):
        from datetime import date

        payload = {
            "User_Id": TARGET_USER_ID,
            "Client_Id": random.randint(1, 10),
            "Facture_Prix": round(random.uniform(100, 5000), 2),
            "Facture_Date": date.today().isoformat(),
            "item_ids": [],
        }
        resp = self.client.post(
            "/invoices/", json=payload, headers=_headers(), name="/invoices/ [POST]"
        )
        if resp.status_code == 201:
            invoice_id = resp.json().get("Facture_Id")
            if invoice_id:
                self.client.delete(
                    f"/invoices/{invoice_id}",
                    headers=_headers(),
                    name="/invoices/{id} [DELETE]",
                )

    @task(1)
    def get_invoice(self):
        invoice_id = random.randint(1, 50)
        self.client.get(
            f"/invoices/{invoice_id}",
            headers=_headers(),
            name="/invoices/{id} [GET]",
        )
