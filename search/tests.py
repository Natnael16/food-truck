from django.test import TestCase, Client
from unittest.mock import patch
from .views import food_truck_collection
from .serializers import FoodTruckSerializer
from .utils import parse_open_hours, validate_location_params

class NearByFoodTrucksTest(TestCase):
    def setUp(self):
        # Mock data for FoodTruck document
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

        # Make GET request to the endpoint with valid parameters
        response = self.client.get('/api/foodtruck/nearby/', {'latitude': 0, 'longitude': 0, 'radius': 1000})

        # Assert that the response status code is 200 (OK)
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

        # Make GET request to the endpoint with invalid latitude
        response = self.client.get('/api/foodtruck/nearby/', {'latitude': -95, 'longitude': 0, 'radius': 1000})

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

class GetAllFoodTrucksTest(TestCase):
    def setUp(self):
        # Mock data for FoodTruck document
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

        # Make GET request to the endpoint
        response = self.client.get('/api/foodtruck/all/')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {
            'count': 1,
            'data': mock_find.return_value
        }
        self.assertEqual(response.json(), expected_data)
 
 
class SearchFoodTrucksTest(TestCase):
    def setUp(self):
        # Mock data for FoodTruck document
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

        # Make GET request to the endpoint
        response = self.client.get('/api/foodtruck/search/')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the response data
        expected_data = {
            'count': 1,
            'data': self.mock_return_value
        }
        self.assertEqual(response.json(), expected_data)
        
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_success_with_appropriate_location_params(self, mock_aggregate):
        # Mock the MongoDB aggregate method
        mock_aggregate.return_value = self.mock_return_value

        # Make GET request to the endpoint with valid location parameters
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

        # Make GET request to the endpoint with invalid latitude and longitude
        response = self.client.get('/api/foodtruck/search/', {'latitude': 'invalid', 'longitude': 'invalid'})

        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check the error message in the response
        self.assertIn('invalid location filter parameter', response.json()['error_message'])
        
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_invalid_location_numbers(self, mock_aggregate):
        # Mock the MongoDB aggregate method
        mock_aggregate.return_value = self.mock_return_value

        # Make GET request to the endpoint with latitude and longitude out of range
        response = self.client.get('/api/foodtruck/search/', {'latitude': 50, 'longitude': 300})

        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check the error message in the response
        self.assertIn('invalid location filter parameter', response.json()['error_message'])
    
    @patch.object(food_truck_collection, 'aggregate')
    def test_search_food_trucks_no_results(self, mock_aggregate):
        # Mock the MongoDB aggregate method to return an empty list
        mock_aggregate.return_value = []

        # Make GET request to the endpoint with a search query that yields no results
        response = self.client.get('/api/foodtruck/search/', {'q': 'nonexistent'})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the count is 0
        self.assertEqual(response.json()['count'], 0)        
        
class TestLocationValidation(TestCase):
    def test_valid_location_params(self):
        # Test with valid parameters
        self.assertTrue(validate_location_params(37.7749, -122.4194, 1000))

    def test_invalid_latitude(self):
        # Test with invalid latitude
        self.assertFalse(validate_location_params(100, -122.4194, 1000))

    def test_invalid_longitude(self):
        # Test with invalid longitude
        self.assertFalse(validate_location_params(37.7749, -200, 1000))

    def test_invalid_radius(self):
        # Test with invalid radius
        self.assertFalse(validate_location_params(37.7749, -122.4194, "not_a_number"))

class TestOpenHoursParsing(TestCase):
    def test_valid_open_hours(self):
        # Test with valid open hours string
        open_hours_str = "Mo-Th:11AM-5PM; Fr:10AM-6PM"
        expected_result = {
            "Monday": [{"start_time": "11AM", "end_time": "5PM"}],
            "Tuesday": [{"start_time": "11AM", "end_time": "5PM"}],
            "Wednesday": [{"start_time": "11AM", "end_time": "5PM"}],
            "Thursday": [{"start_time": "11AM", "end_time": "5PM"}],
            "Friday": [{"start_time": "10AM", "end_time": "6PM"}]
        }
        self.assertEqual(parse_open_hours(open_hours_str), expected_result)
        
    def test_parse_open_hours_test_cases(self):
        # Representative test cases covering different formats and scenarios
        test_cases = [
            ("Mo-Fr:3PM-4PM", {"Monday": [{"start_time": "3PM", "end_time": "4PM"}], 
                               "Tuesday": [{"start_time": "3PM", "end_time": "4PM"}], 
                               "Wednesday": [{"start_time": "3PM", "end_time": "4PM"}], 
                               "Thursday": [{"start_time": "3PM", "end_time": "4PM"}], 
                               "Friday": [{"start_time": "3PM", "end_time": "4PM"}]}),
            ("Mo-Fr:6AM-7AM/11AM-12PM", {"Monday": [{"start_time": "6AM", "end_time": "7AM"}, {"start_time": "11AM", "end_time": "12PM"}], 
                                         "Tuesday": [{"start_time": "6AM", "end_time": "7AM"}, {"start_time": "11AM", "end_time": "12PM"}], 
                                         "Wednesday": [{"start_time": "6AM", "end_time": "7AM"}, {"start_time": "11AM", "end_time": "12PM"}], 
                                         "Thursday": [{"start_time": "6AM", "end_time": "7AM"}, {"start_time": "11AM", "end_time": "12PM"}], 
                                         "Friday": [{"start_time": "6AM", "end_time": "7AM"}, {"start_time": "11AM", "end_time": "12PM"}]}),
            ("Su/We/Sa:11AM-3PM", {"Sunday": [{"start_time": "11AM", "end_time": "3PM"}], 
                                   "Wednesday": [{"start_time": "11AM", "end_time": "3PM"}], 
                                   "Saturday": [{"start_time": "11AM", "end_time": "3PM"}]}),
            # Add more representative test cases as needed
        ]

        for input_str, expected_output in test_cases:
            with self.subTest(input_str=input_str):
                self.assertEqual(parse_open_hours(input_str), expected_output)

    def test_invalid_open_hours(self):
        # Test with invalid open hours string
        open_hours_str = "Invalid format"
        self.assertEqual(parse_open_hours(open_hours_str), {})

        # Test with empty string
        open_hours_str = ""
        self.assertEqual(parse_open_hours(open_hours_str), {})