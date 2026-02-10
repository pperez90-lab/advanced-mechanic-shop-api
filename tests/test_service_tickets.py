import unittest

from app import create_app
from app.models import db, Customer, Mechanic, Inventory


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Ticket User",
                email="ticket@example.com",
                phone="111-222-3333",
                password="ticketpw"
            )
            self.mechanic = Mechanic(
                name="Mech Ticket",
                email="mech.ticket@example.com",
                phone="222-333-4444",
                salary=70000.0
            )
            self.inventory = Inventory(
                name="Spark Plug",
                price=8.0
            )

            db.session.add_all([self.customer, self.mechanic, self.inventory])
            db.session.commit()

            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id
            self.inventory_id = self.inventory.id

        self.client = self.app.test_client()

    def test_create_ticket(self):
        payload = {
            "VIN": "1ABCDEF1234567890",
            "service_date": "2025-01-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        }
        response = self.client.post("/service-tickets/", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_duplicate_vin(self):
        payload = {
            "VIN": "DUPVIN123",
            "service_date": "2025-01-01",
            "service_desc": "Initial",
            "customer_id": self.customer_id
        }
        first = self.client.post("/service-tickets/", json=payload)
        self.assertEqual(first.status_code, 201)
        second = self.client.post("/service-tickets/", json=payload)
        self.assertEqual(second.status_code, 400)

    def test_assign_mechanic_to_ticket(self):
        payload = {
            "VIN": "ASSIGNVIN",
            "service_date": "2025-01-01",
            "service_desc": "Check engine",
            "customer_id": self.customer_id
        }
        ticket_resp = self.client.post("/service-tickets/", json=payload)
        ticket_id = ticket_resp.json["id"]

        response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{self.mechanic_id}"
        )
        self.assertEqual(response.status_code, 200)

    def test_add_part_to_ticket(self):
        payload = {
            "VIN": "PARTVIN",
            "service_date": "2025-01-01",
            "service_desc": "Spark plug replacement",
            "customer_id": self.customer_id
        }
        ticket_resp = self.client.post("/service-tickets/", json=payload)
        ticket_id = ticket_resp.json["id"]

        response = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/{self.inventory_id}"
        )
        self.assertEqual(response.status_code, 200)

        response2 = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/{self.inventory_id}"
        )
        self.assertEqual(response2.status_code, 400)
