import unittest

from app import create_app
from app.models import db, Customer


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # seed one customer
            self.customer = Customer(
                name="Seed User",
                email="seed@example.com",
                phone="123-456-7890",
                password="seedpw"
            )
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id

        self.client = self.app.test_client()

    # helper
    def _login_and_get_token(self):
        credentials = {
            "email": "seed@example.com",
            "password": "seedpw"
        }
        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        return response.json["token"]

    def test_create_customer(self):
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "999-999-9999",
            "password": "password123"
        }
        # matches @customers_bp.route("/", methods=['POST'])
        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "John Doe")

    def test_create_customer_duplicate_email(self):
        payload = {
            "name": "Another",
            "email": "seed@example.com",  # already exists
            "phone": "000-000-0000",
            "password": "pass"
        }
        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_customers_paginated(self):
        response = self.client.get("/customers/?page=1&per_page=10")
        self.assertEqual(response.status_code, 200)
        self.assertIn("customers", response.json)
        self.assertIsInstance(response.json["customers"], list)

    def test_login_customer(self):
        token = self._login_and_get_token()
        self.assertIsInstance(token, str)

    def test_invalid_login_customer(self):
        credentials = {
            "email": "bad@example.com",
            "password": "badpw"
        }
        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("message"), "Invalid email or password!")

    def test_update_customer_with_token(self):
        token = self._login_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "name": "Updated Name",
            "email": "seed@example.com",
            "phone": "123-456-7890",
            "password": "seedpw"
        }
        # matches @customers_bp.route("/", methods=['PUT'])
        response = self.client.put("/customers/", json=payload, headers=headers)
        # NOTE: because route signature is def update_customer(customer_id),
        # this may still error at runtime until routes.py is fixed.
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_with_token(self):
        token = self._login_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        # matches @customers_bp.route("/", methods=['DELETE'])
        response = self.client.delete("/customers/", headers=headers)
        # same note: route expects customer_id argument even though URL has none.
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
