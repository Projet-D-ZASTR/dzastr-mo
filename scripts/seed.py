"""
Script de seed pour générer des données factices en local.

Usage:
    python scripts/seed.py
"""

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import random

from config import SessionLocal
from src.models.client import Client
from src.models.invoices import Invoice, InvoiceItem, InvoiceState
from src.models.services import Service

N_CLIENTS = 20
N_SERVICES = 20
N_INVOICES = 50


def seed():
    db = SessionLocal()
    try:
        from src.models.user_stub import UserStub

        USER_IDS = [u.User_Id for u in db.query(UserStub.User_Id).all()]
        if not USER_IDS:
            print("Aucun user trouvé en DB. Crée d'abord des users via dzastr-auth.")
            return
        print(f"Users trouvés : {USER_IDS}")
        # ── Clients ────────────────────────────────────────────────────────
        clients = []
        for i in range(1, N_CLIENTS + 1):
            client = Client(
                User_Id=random.choice(USER_IDS),
                Client_Name=f"Client {i}",
                Client_Entreprise=f"Entreprise {i} SARL",
                Client_Email=f"client{i}@example.com",
                Client_Address=f"{i} rue de la Paix, Paris",
            )
            db.add(client)
            clients.append(client)

        db.flush()
        print(f"✓ {N_CLIENTS} clients créés")

        # ── Services ───────────────────────────────────────────────────────
        service_names = [
            "Développement web",
            "Design UI/UX",
            "Conseil stratégique",
            "Audit SEO",
            "Rédaction",
            "Formation",
            "Support technique",
            "Maintenance",
            "Intégration API",
            "Marketing digital",
        ]
        services = []
        for i in range(1, N_SERVICES + 1):
            service = Service(
                User_Id=random.choice(USER_IDS),
                Service_Name=f"{random.choice(service_names)} {i}",
                Service_PriceHour=round(random.uniform(50, 500), 2),
                Service_Description=f"Description du service {i}",
            )
            db.add(service)
            services.append(service)

        db.flush()
        print(f"✓ {N_SERVICES} services créés")

        # ── Invoices ───────────────────────────────────────────────────────
        states = list(InvoiceState)
        for i in range(N_INVOICES):
            client = random.choice(clients)
            invoice = Invoice(
                User_Id=client.User_Id,
                Client_Id=client.Client_Id,
                Facture_Prix=round(random.uniform(100, 5000), 2),
                Facture_Date=date.today() - timedelta(days=random.randint(0, 365)),
                Facture_State=random.choice(states),
            )
            db.add(invoice)
            db.flush()

            for _ in range(random.randint(0, 3)):
                db.add(InvoiceItem(Facture_Id=invoice.Facture_Id, Nombre_Id=random.randint(1, 10)))

        db.commit()
        print(f"✓ {N_INVOICES} factures créées")
        print("\nSeed terminé avec succès.")

    except Exception as e:
        db.rollback()
        print(f"Erreur : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    
