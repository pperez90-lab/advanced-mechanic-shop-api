import unittest

from app import create_app
from app.models import db, Mechanic


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.mechanic = Mechanic(
                name="Mech One",
                email="mech1@example.com",
                phone="123-123-1234",
                salary=50000.0
            )
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id

        self.client = self.app.test_client()

    def test_create_mechanic(self):
        payload = {
            "name": "Mech Two",
            "email": "mech2@example.com",
            "phone": "999-999-9999",
            "salary": 60000.0
        }
        response = self.client.post("/mechanics/", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_mechanic(self):
        response = self.client.get(f"/mechanics/{self.mechanic_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_mechanic_not_found(self):
        response = self.client.get("/mechanics/9999")
        self.assertEqual(response.status_code, 404)

    def test_get_mechanics_by_ticket_count(self):
        response = self.client.get("/mechanics/by-ticket-count")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
