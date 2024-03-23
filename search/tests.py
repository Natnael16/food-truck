from django.test import TestCase, Client
from unittest.mock import patch
from .views import food_truck_collection
from .serializers import FoodTruckSerializer

class NearByFoodTrucksTest(TestCase):
    def setUp(self):
        self.mock_return_value = {
                    'applicant': 'mock',
                    'facility_type': 'Truck',
                    'location_description': 'mock location description',
                    'address': "mock address",
                    'status': "Approved",
                    'food_items': [], 
                    'approved_at': None,
                    'location': {'type': 'Point', 'coordinates': [0, 0]},  # GeoJSON format for coordinates
                    'open_hours' : {}
                }
        self.client = Client()

    @patch.object(food_truck_collection, 'find')
    def test_get_nearby_foodtrucks_should_be_successfull(self, mock_find):
        # Mock the MongoDB find method
        mock_find.return_value = [
            self.mock_return_value
            ]

        response = self.client.get('http://127.0.0.1:8000/api/foodtruck/nearby/', {'latitude': 0, 'longitude': 0, 'radius': 1000})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {
            'count': 1,
            'data': FoodTruckSerializer(mock_find.return_value, many=True).data
        }
        self.assertEqual(response.json(), expected_data)
    
    @patch.object(food_truck_collection, 'find')
    def test_get_nearby_foodtrucks_should_fail_with_invalid_parameter(self, mock_find):
        # Mock the MongoDB find method
        mock_find.return_value = [
            self.mock_return_value
            ]

        response = self.client.get('http://127.0.0.1:8000/api/foodtruck/nearby/', {'latitude': -95, 'longitude': 0, 'radius': 1000}) #having invalid latitude to make it fail

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 400)
        
        
class GetAllFoodTrucksTest(TestCase):
    def setUp(self):
        self.mock_return_value = {
                    'applicant': 'mock',
                    'facility_type': 'Truck',
                    'location_description': 'mock location description',
                    'address': "mock address",
                    'status': "Approved",
                    'food_items': [], 
                    'approved_at': None,
                    'location': {'type': 'Point', 'coordinates': [0, 0]},  # GeoJSON format for coordinates
                    'open_hours' : {}
                }
        self.client = Client()
        
    @patch.object(food_truck_collection, 'find')
    def test_get_all_food_trucks_success(self, mock_find):
        # Mock the MongoDB find method
        mock_find.return_value = [
            self.mock_return_value
        ]

        response = self.client.get('/api/foodtruck/all/')

        self.assertEqual(response.status_code, 200)

        expected_data = {
            'count': 1,
            'data': mock_find.return_value
        }
        self.assertEqual(response.json(), expected_data)
 
 
class SearchFoodTrucksTest(TestCase):
    def setUp(self):
        self.mock_return_value = [{
            'applicant': 'mock',
            'facility_type': 'Truck',
            'location_description': 'mock location description',
            'address': "mock address",
            'status': "Approved",
            'food_items': [], 
            'approved_at': None,
            'location': {'type': 'Point', 'coordinates': [0, 0]},  # GeoJSON format for coordinates
            'open_hours' : {}
        }]
        self.client = Client()
        
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_success(self, mock_aggregate):
        # Mock the MongoDB aggregate method
        mock_aggregate.return_value = self.mock_return_value

        response = self.client.get('/api/foodtruck/search/')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {
            'count': 1,
            'data': self.mock_return_value
        }
        self.assertEqual(response.json(), expected_data)
    def test_search_food_trucks_success_with_appropriate_location_params(self, mock_aggregate):
        # Mock the MongoDB aggregate method
        mock_aggregate.return_value = self.mock_return_value

        response = self.client.get('/api/foodtruck/search/', {'latitude': 0, 'longitude': 0, 'radius': 50})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {
            'count': 1,
            'data': self.mock_return_value
        }
        self.assertEqual(response.json(), expected_data)
    
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_invalid_location_type(self, mock_aggregate):
        # Mock the MongoDB aggregate method
        mock_aggregate.return_value = self.mock_return_value

        # Send request with invalid latitude and longitude
        response = self.client.get('/api/foodtruck/search/', {'latitude': 'invalid', 'longitude': 'invalid'})

        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check the error message in the response
        self.assertIn('invalid location filter parameter', response.json()['error_message'])
        
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_invalid_location_numbers(self, mock_aggregate):
        # Mock the MongoDB aggregate method
        mock_aggregate.return_value = self.mock_return_value

        # Send request with invalid latitude and longitude
        response = self.client.get('/api/foodtruck/search/', {'latitude': 50, 'longitude': 300})

        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check the error message in the response
        self.assertIn('invalid location filter parameter', response.json()['error_message'])
    
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_no_results(self, mock_aggregate):
        # Mock the MongoDB aggregate method to return an empty list
        mock_aggregate.return_value = []

        # Send request with valid parameters but no matching results
        response = self.client.get('/api/foodtruck/search/', {'q': 'nonexistent'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the count is 0
        self.assertEqual(response.json()['count'], 0)