import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from foodTruck.db_connection import db
from search.utils import parse_open_hours

# Accessing MongoDB collections
food_truck_collection = db['food_truck']
food_collection = db['food']

class Command(BaseCommand):
    # Description of the command for manage.py help text
    help = 'Seeds the food truck data from a CSV file'

    def handle(self, *args, **options):
        # Clear existing data in collections
        food_truck_collection.delete_many({})
        food_collection.delete_many({})
        
        # Path to the CSV file containing food truck data
        csv_file_path = 'data/food-truck-data.csv'
        # Set to keep track of unique food items
        foods_set = set()
        
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Split food items by ':' and strip leading/trailing whitespace
                food_items = str(row['FoodItems']).strip().split(':') if row['FoodItems'] else []
                # Iterate over food items and add to food collection if not already present
                for food in food_items:
                    if food.title() not in foods_set:
                        foods_set.add(food.title())
                        food_collection.insert_one({'name': food.strip().title()})
                
                # Construct data object for food truck document
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
                # Insert food truck data into MongoDB
                food_truck_collection.insert_one(data)
        
        # Display success message
        self.stdout.write(self.style.SUCCESS('Data seeded successfully'))
