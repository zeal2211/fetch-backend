from django.test import TestCase, Client
import json

class ReceiptProcessorTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_receipt_processing(self):
        response = self.client.post(
            '/receipts/process',
            json.dumps({
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                    },{
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                    },{
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                    },{
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                    }
                ],
                "total": "9.00"
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
        self.assertEqual(points_data['points'], 109)
