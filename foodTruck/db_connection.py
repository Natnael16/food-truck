from pymongo import MongoClient


url = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'

db_client = MongoClient(url)

db = db_client['food_truck_finder']

db['food_truck'].create_index({"location": '2dsphere'})