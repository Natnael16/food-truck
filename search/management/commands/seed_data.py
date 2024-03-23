import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from foodTruck.db_connection import db
from search.utils import parse_open_hours

food_truck_collection = db['food_truck']
food_collection = db['food']

class Command(BaseCommand):
    help = 'Seeds the food truck data from a CSV file'

    def handle(self, *args, **options):
        food_truck_collection.delete_many({})
        food_collection.delete_many({})
        
        csv_file_path = 'data/food-truck-data.csv'
        foods_set = set()
        
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_items = str(row['FoodItems']).strip().split(':') if row['FoodItems'] else []
                for food in food_items:
                    if food.title() not in foods_set: # O(1) opperation since it is checking in set
                        foods_set.add(food.title())
                        food_collection.insert_one({'name': food.strip().title()})
                data = {
                    'applicant': str(row['Applicant']),
                    'facility_type': str(row['FacilityType']) if row['FacilityType'] else 'Unknown',
                    'location_description': str(row['LocationDescription']),
                    'address': str(row['Address']),
                    'status': str(row['Status']),
                    'food_items': food_items, 
                    'approved_at': datetime.strptime(str(row['Approved']), '%m/%d/%Y %I:%M:%S %p') if row['Approved'] else None,
                    'location': {'type': 'Point', 'coordinates': [float(row['Longitude']), float(row['Latitude'])]},  # GeoJSON format for coordinates
                    'open_hours' : parse_open_hours(row['dayshours'])
                }
                food_truck_collection.insert_one(data)
        
        self.stdout.write(self.style.SUCCESS('Data seeded successfully'))