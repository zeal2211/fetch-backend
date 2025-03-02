from django.test import TestCase, Client
import json

class ReceiptProcessorTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_receipt_processing(self):
        response = self.client.post(
            '/receipts/process',
            json.dumps({
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
                ],
                "total": "35.35"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('id', data)

        # Fetch points
        receipt_id = data['id']
        response = self.client.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(response.status_code, 200)

        points_data = response.json()
        self.assertEqual(points_data['points'], 28)
