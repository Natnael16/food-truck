from django.test import TestCase, Client
from unittest.mock import patch
from .views import food_collection
# Create your tests here.
class GetAllFoodTrucksTest(TestCase):
    def setUp(self):
        self.mock_return_value = {
                    'name' : 'mock food'
                }
        self.client = Client()
        
    @patch.object(food_collection, 'find')
    def test_get_all_foods_success(self, mock_find):
        # Mock the MongoDB find method
        mock_find.return_value = [
            self.mock_return_value
        ]

        response = self.client.get('/api/foods/search/')

        self.assertEqual(response.status_code, 200)

        expected_data = {
            'count': 1,
            'data': mock_find.return_value
        }
        self.assertEqual(response.json(), expected_data)