import math
import csv
from datetime import datetime
from . import utils
from . import db_connection

food_truck_collection = db_connection.db['food_truck']

def seed_data():
    # check if the data has been seeded
    collection_size = food_truck_collection.count_documents({})
    if collection_size != 0:
        return
    # Read the CSV file into a DataFrame
    csv_file_path = 'data/food-truck-data.csv'
    
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = {
                    'applicant': str(row['Applicant']),
                    'facility_type': str(row['FacilityType']),
                    'location_description': str(row['LocationDescription']),
                    'address': str(row['Address']),
                    'status': str(row['Status']),
                    'food_items': str(row['FoodItems']).split(':') if row['FoodItems'] else [],  # Convert to list
                    'approved_at': datetime.strptime(str(row['Approved']), '%m/%d/%Y %I:%M:%S %p') if row['Approved'] else None,
                    'location': {'type': 'Point', 'coordinates': [float(row['Longitude']), float(row['Latitude'])]},  # GeoJSON format for coordinates
                    'open_hours' : utils.parse_open_hours(row['dayshours'])
                }
            food_truck_collection.insert_one(data)
        

    print('Data seeded successfully')
