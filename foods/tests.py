from django.test import TestCase, Client
from unittest.mock import patch
from .views import food_collection

class GetAllFoodsTest(TestCase):
    """
    Test case for retrieving all foods.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.mock_return_value = {'name': 'mock food'}
        self.client = Client()
        
    @patch.object(food_collection, 'find')
    def test_get_all_foods_success(self, mock_find):
        """
        Test retrieving all foods successfully.
        """
        # Mock the MongoDB find method
        mock_find.return_value = [self.mock_return_value]

        # Send GET request to the endpoint
        response = self.client.get('/api/foods/search/')

        # Assert response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {'count': 1, 'data': mock_find.return_value}
        self.assertEqual(response.json(), expected_data)
        
    @patch.object(food_collection, 'find')
    def test_get_all_foods_empty(self, mock_find):
        """
        Test retrieving all foods successfully.
        """
        # Mock the MongoDB find method
        mock_find.return_value = []

        # Send GET request to the endpoint
        response = self.client.get('/api/foods/search/')

        # Assert response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {'count': 0, 'data': []}
        self.assertEqual(response.json(), expected_data)

