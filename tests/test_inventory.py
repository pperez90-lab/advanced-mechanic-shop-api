import unittest

from app import create_app
from app.models import db, Inventory


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.part = Inventory(
                name="Brake Pad",
                price=50.0
            )
            db.session.add(self.part)
            db.session.commit()
            self.part_id = self.part.id

        self.client = self.app.test_client()

    def test_create_inventory_item(self):
        payload = {
            "name": "Oil Filter",
            "price": 15.5
        }
        response = self.client.post("/inventory/", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_inventory(self):
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_inventory_item(self):
        payload = {
            "name": "Brake Pad",
            "price": 55.0
        }
        response = self.client.put(f"/inventory/{self.part_id}", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_inventory_item_not_found(self):
        response = self.client.delete("/inventory/9999")
        self.assertEqual(response.status_code, 404)
